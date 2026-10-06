# AGENTS.md

## What this repo is

Firmware for an **IoT RC car** — controls a motor driver over Bluetooth and WiFi.
This is the code-development part of an already-working hardware build.

**Do NOT assume this is a web app.** The course ("Application Project II", 2 SKS, semester 5,
dosen: Jozua Ferjanus Palandi) advertises itself as Laravel Livewire. It is not — there is no
PHP/Laravel here. Scope is embedded firmware only.

- Course team: **Ecayci Lover**
  - Faiz Ramadhan (241111011) — Scrum Master + Developer
  - Dico Havianto (241111017) — Product Owner
- Deliverables are graded as part of the course; docs are written in Indonesian.

## Hardware (per course guide)

- Main board: **Arduino Uno**.
- Pin expansion: **Arduino Shield V5.0** — required because the Uno has too few pins.
  - Breaks out Analog I/O (A0–A5), Digital I/O (D0–D13), External Power, SD/SPI,
    Ultrasonic, a **Bluetooth connector**, a **Wireless connector**, LCD (parallel & serial),
    and I2C.
  - The `SEL` jumper selects the VCC source feeding the I/O headers.
- The Uno has **no built-in WiFi/Bluetooth**; wireless comes from modules attached to the
  shield's Bluetooth / Wireless connectors.

> OPEN QUESTION — reconcile before hardcoding anything: an earlier note said the car uses
> **ESP32**, but the course guide says the main board is **Arduino Uno + Shield V5.0**.
> Is the ESP32 a separate board, or the WiFi module plugged into the shield's wireless
> connector?

## Toolchain

- **Arduino IDE**, sketches are `.ino` (not PlatformIO, not ESP-IDF).
- Target board: **Arduino Uno** (AVR) — respect its tight RAM/flash budget and pin count.
- Build / flash: Arduino IDE toolbar (Verify / Upload). There is **no CLI build, no test
  runner, no CI** — do not invent `npm`/`pytest`/`make` commands.
- "Testing" = flash to the physical car and exercise it over Bluetooth/WiFi. State clearly
  when a change is unverified on hardware.

## Layout

- `firmware/` — Arduino `.ino` sketch(es) + `secrets.h` (gitignored, see below).
- `docs/` — course deliverables (team profile, reports). Indonesian prose.

## Gotchas

- **Never commit WiFi SSID/password or Bluetooth keys.** Put them in `firmware/secrets.h`
  (gitignored) and `#include` it. `secrets.example.h` holds the placeholder version.
- Uno is 5V logic; some Bluetooth/WiFi modules are 3.3V — check levels before wiring, and
  don't assume a module tolerates 5V.
- The shield already claims pins (SPI/SD, LCD, connector headers). Don't assign a pin the
  shield is using.
- Motor driver model, GPIO pin map, and PWM setup are **not yet fixed** — see
  `firmware/README.md`. Confirm real wiring before hardcoding pins.
- Docs and code comments are Indonesian; keep new docs consistent.

## Course deliverables

- `docs/tugas-1-profil-tim.md` — Tugas 1 (5%): team profile, roles, project vision.
