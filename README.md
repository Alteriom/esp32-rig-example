# esp32-rig-example

The smallest project an [Alteriom HIL rig](https://alteriom.github.io/esp32-rig/)
can run: a firmware that answers the rig, a suite of three tests, and the
workflow that builds the bundle the rig flashes. Fork it and replace `sum`
with what your firmware does.

```
src/main.cpp                 the firmware: info, echo, sum, reset — newline JSON over serial
platformio.ini               one environment per family: esp32, esp32-c3, esp32-s3, esp8266
scripts/build_bundle.py      pio run per family, merge into one image each, write manifest.json
tests/                       pytest, using the rig's `bank` fixture; one row per board
.github/workflows/hil.yml    builds the bundle, uploads it as `hil-artifacts`; optional hand-over
.github/workflows/suite.yml  runs the suite against the rig's simulator on every push
```

## On a rig

1. Give the rig a GitHub token that can read this repository and its
   Actions artifacts (**Settings → Rig → GitHub**).
2. **Settings → Projects → Add project**, paste this repository's URL,
   **Look it up**, **Add**. The defaults are this project's: suite in
   `tests`, workflow `.github/workflows/hil.yml`, artifact `hil-artifacts`,
   revision key `git_sha`. (A rig from release 1.0.177 on ships this project
   already, under **Rig example**: skip to step 3.)
3. On the project's page, **Get firmware from GitHub**. The rig takes the
   newest bundle this repository's HIL workflow built.
4. **Runs → New run**, this project, that bundle, **Run**. Three green rows
   per board.

## What the rig expects of a firmware

Newline-delimited JSON over the board's serial port. `{"cmd":"info"}` is
answered with `{"evt":"info","family":…,"bootId":…,…}`, a start is announced
with `{"evt":"boot",…}`, and a line that is not a command is answered
`{"evt":"error","error":"bad json"}`. Past that, the commands are yours; the
suite drives them through the rig's board client
(`send_cmd_awaiting`, `wait_for`, `ensure_responsive`, `hard_reset`).

## What the rig expects of a bundle

A directory with `manifest.json` (schema 2) and one merged image per family;
the manifest's revision key holds the commit. `scripts/build_bundle.py`
writes exactly that. The rig re-hashes every file before it flashes.

## Building it yourself

```bash
python -m pip install platformio esptool
python scripts/build_bundle.py --out hil-artifacts --target esp32
```

And the suite, against the rig's simulator, with the rig's packages
installed from a [rig release](https://github.com/Alteriom/esp32-rig/releases):

```bash
ALTERIOM_HIL_MODE=sim python -m pytest tests -q
```

Apache-2.0.
