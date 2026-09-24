// The smallest firmware a rig can test.
//
// It answers the two questions every firmware on a rig answers -- `info`
// (who are you, are you alive) and `echo` (is the serial path clean) -- and
// one of its own, `sum`, which is the thing under test here. Newline-
// delimited JSON both ways: one command object per line in, one event
// object per line out. The rig's board client (alteriom_hil.protocol) reads
// exactly this framing, and the suite in tests/ drives it.
//
// host -> board:  {"cmd":"info"}
//                 {"cmd":"echo","text":"..."}
//                 {"cmd":"sum","a":20,"b":22}
//                 {"cmd":"reset"}
// board -> host:  {"evt":"boot",...}  once per start
//                 {"evt":"info",...}  {"evt":"echo",...}  {"evt":"sum","value":42}
//                 {"evt":"error","error":"bad json"}  for a line that was not a command
//
// Replace `sum` with what your firmware does; keep `info` and the framing.
#include <Arduino.h>
#include <ArduinoJson.h>
#if defined(ESP8266)
#include <ESP8266WiFi.h>
#else
#include <WiFi.h>
#endif

#ifndef EXAMPLE_FAMILY
#define EXAMPLE_FAMILY "unknown"
#endif
// The commit this image was built from, stamped in by scripts/build_bundle.py,
// so a board can say which build it runs and the rig can hold it to the one
// it flashed.
#ifndef EXAMPLE_COMMIT
#define EXAMPLE_COMMIT "unknown"
#endif

// A whole line of JSON. The rig's serial check sends a kilobyte, so the
// buffer has room for one and the console is opened with room for more.
constexpr size_t kLineMax = 1024;

String line;
String bootId;

// ---- framing -----------------------------------------------------------------

void emit(JsonDocument &doc) {
  String out;
  serializeJson(doc, out);
  Serial.println(out);
  Serial.flush();
}

void emitError(const char *error) {
  JsonDocument doc;
  doc["evt"] = "error";
  doc["error"] = error;
  emit(doc);
}

// ---- what the rig asks of every firmware ---------------------------------------

void replyInfo() {
  JsonDocument doc;
  doc["evt"] = "info";
  doc["family"] = EXAMPLE_FAMILY;
  doc["commit"] = EXAMPLE_COMMIT;
  doc["bootId"] = bootId;
  doc["uptimeMs"] = millis();
  doc["freeHeap"] = ESP.getFreeHeap();
  doc["mac"] = WiFi.macAddress();
  emit(doc);
}

void replyEcho(JsonDocument &cmd) {
  // Returned byte for byte: anything the UART mangles shows as a difference
  // the host can print, not as a missing reply.
  const char *text = cmd["text"] | "";
  JsonDocument doc;
  doc["evt"] = "echo";
  doc["text"] = text;
  doc["len"] = strlen(text);
  emit(doc);
}

// ---- what this firmware does ---------------------------------------------------

void replySum(JsonDocument &cmd) {
  const long a = cmd["a"] | 0L;
  const long b = cmd["b"] | 0L;
  JsonDocument doc;
  doc["evt"] = "sum";
  doc["a"] = a;
  doc["b"] = b;
  doc["value"] = a + b;
  emit(doc);
}

// ---- dispatch ------------------------------------------------------------------

void handle(const String &raw) {
  JsonDocument cmd;
  if (deserializeJson(cmd, raw) != DeserializationError::Ok) {
    // The exact words the rig resends on: a parse failure says the command
    // did not run, which makes resending it safe.
    emitError("bad json");
    return;
  }
  const char *name = cmd["cmd"] | "";
  if (strcmp(name, "info") == 0) {
    replyInfo();
  } else if (strcmp(name, "echo") == 0) {
    replyEcho(cmd);
  } else if (strcmp(name, "sum") == 0) {
    replySum(cmd);
  } else if (strcmp(name, "reset") == 0) {
    JsonDocument doc;
    doc["evt"] = "resetting";
    doc["bootId"] = bootId;
    emit(doc);
    delay(100);
    ESP.restart();
  } else {
    String message = String("unknown cmd ") + name;
    emitError(message.c_str());
  }
}

void pump() {
  while (Serial.available()) {
    const char c = static_cast<char>(Serial.read());
    if (c == '\r') continue;
    if (c == '\n') {
      String raw = line;
      line = "";
      raw.trim();
      if (raw.length() > 0) handle(raw);
      continue;
    }
    if (line.length() >= kLineMax) {
      // Say so rather than acting on half a command.
      line = "";
      emitError("frame dropped: line too long");
      continue;
    }
    line += c;
  }
}

void setup() {
  // Room for a whole line and then some, set before the port opens: a
  // console whose buffer is smaller loses the end of a long command before
  // this sketch is ever scheduled.
  Serial.setRxBufferSize(kLineMax + 512);
  Serial.begin(115200);
  delay(200);
  line.reserve(kLineMax + 1);
  // A new id every boot, so a reset is provable: the host compares the id it
  // had with the one it gets.
  char buffer[9];
  snprintf(buffer, sizeof(buffer), "%08lx",
           static_cast<unsigned long>(ESP.getCycleCount() ^ micros() ^ (uint32_t)ESP.getFreeHeap()));
  bootId = buffer;
  // A station, never an access point: a board that brought up an AP would
  // change what every other board on the rig can see.
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  JsonDocument doc;
  doc["evt"] = "boot";
  doc["family"] = EXAMPLE_FAMILY;
  doc["commit"] = EXAMPLE_COMMIT;
  doc["bootId"] = bootId;
  emit(doc);
}

void loop() {
  pump();
  delay(2);
}
