#!/usr/bin/env python3
"""Build the bundle a rig flashes: one merged image per family, and the
manifest that names them.

    python scripts/build_bundle.py --out hil-artifacts [--target esp32 ...]

For each family: `pio run -e <family>`, then the bootloader, partition table,
OTA selector and application merged at their offsets into one
`flash-image.bin` (the ESP8266 is one image already). Then `manifest.json`,
schema 2, with this project's revision key -- `esp32_rig_example_sha`, the
commit the build resolved to -- which is what a run is named by and what the
rig holds a bundle to. The rig re-hashes every file before it flashes.

Needs `platformio` and `esptool` on the path (`python -m pip install
platformio esptool`). About a hundred lines, and yours to change.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVISION_KEY = "esp32_rig_example_sha"
PRODUCER = "esp32-rig-example"

# Silicon facts, the same as every producer's: the esptool chip name, the
# PlatformIO board, where the bootloader goes, and which layout the family has.
TARGETS = {
    "esp32": {"chip": "esp32", "board": "esp32dev", "bootloader": "0x1000", "layout": "esp32"},
    "esp32-c3": {"chip": "esp32c3", "board": "esp32-c3-devkitm-1", "bootloader": "0x0", "layout": "esp32"},
    "esp32-s3": {"chip": "esp32s3", "board": "esp32-s3-devkitc-1", "bootloader": "0x0", "layout": "esp32"},
    "esp8266": {"chip": "esp8266", "board": "nodemcuv2", "bootloader": "0x0", "layout": "esp8266"},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def commit() -> str:
    """The commit this bundle is built from: what the rig names the run by."""
    found = os.environ.get("GITHUB_SHA", "").strip()
    if not found:
        done = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True)
        found = done.stdout.strip() if done.returncode == 0 else ""
    if len(found) != 40:
        raise RuntimeError("cannot determine the commit: run from a git checkout, or set GITHUB_SHA")
    return found.lower()


def boot_app0() -> Path:
    """The fixed OTA-data image the Arduino core ships."""
    core = Path(os.environ.get("PLATFORMIO_CORE_DIR") or Path.home() / ".platformio")
    found = sorted(core.glob("packages/framework-arduinoespressif32*/tools/partitions/boot_app0.bin"))
    if not found:
        raise FileNotFoundError(f"boot_app0.bin was not installed under {core}")
    return found[0]


def build(out_dir: Path, names: list[str]) -> Path:
    pio = shutil.which("pio") or shutil.which("platformio")
    if not pio:
        raise FileNotFoundError("pio is not on PATH (python -m pip install platformio)")
    revision = commit()
    out_dir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, EXAMPLE_COMMIT=revision)
    targets: dict = {}
    for name in names:
        target = TARGETS[name]
        print(f"==> {PRODUCER} {revision[:9]} {name} ({target['board']})")
        subprocess.run([pio, "run", "-d", str(ROOT), "-e", name], check=True, env=env)
        built = ROOT / ".pio" / "build" / name
        target_dir = out_dir / name
        target_dir.mkdir(parents=True, exist_ok=True)
        if target["layout"] == "esp8266":
            components = {"firmware.bin": built / "firmware.bin"}
            segments = {"firmware.bin": "0x0"}
        else:
            components = {
                "bootloader.bin": built / "bootloader.bin",
                "partitions.bin": built / "partitions.bin",
                "boot_app0.bin": boot_app0(),
                "firmware.bin": built / "firmware.bin",
            }
            segments = {"bootloader.bin": target["bootloader"], "partitions.bin": "0x8000",
                        "boot_app0.bin": "0xe000", "firmware.bin": "0x10000"}
        for filename, source in components.items():
            if not source.is_file():
                raise FileNotFoundError(f"missing build component: {source}")
            shutil.copy2(source, target_dir / filename)
        merged = target_dir / "flash-image.bin"
        if target["layout"] == "esp8266":
            shutil.copy2(target_dir / "firmware.bin", merged)
        else:
            merge = [sys.executable, "-m", "esptool", "--chip", target["chip"], "merge-bin", "-o", str(merged)]
            for filename, offset in segments.items():
                merge.extend((offset, str(target_dir / filename)))
            subprocess.run(merge, check=True)
        files = {path.name: {"sha256": sha256(path), "size": path.stat().st_size}
                 for path in sorted(target_dir.glob("*.bin"))}
        targets[name] = {
            "platformio_env": name, "board": target["board"], "chip": target["chip"],
            "flash_offset": "0x0", "image": f"{name}/flash-image.bin",
            "sha256": files["flash-image.bin"]["sha256"], "files": files, "segments": segments,
        }
    manifest = out_dir / "manifest.json"
    manifest.write_text(json.dumps({
        "schema": 2,
        "producer": PRODUCER,
        REVISION_KEY: revision,
        "targets": targets,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"bundle: {manifest}")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=Path("hil-artifacts"))
    parser.add_argument("--target", action="append", choices=sorted(TARGETS),
                        help="a family to build (default: all of them)")
    args = parser.parse_args(argv)
    build(args.out, args.target or sorted(TARGETS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
