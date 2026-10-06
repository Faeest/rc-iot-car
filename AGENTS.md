# AGENTS.md

## What this repo is

Firmware for an **IoT RC car** — drives 2 DC motors through an **L298N** motor driver,
controlled over Bluetooth and WiFi from an **ESP32**.
This is the code-development part of an already-working hardware build.

**Do NOT assume this is a web app.** The course ("Application Project II", 2 SKS, semester 5,
dosen: Jozua Ferjanus Palandi) advertises itself as Laravel Livewire. It is not — there is no
PHP/Laravel here. Scope is embedded firmware only.

- Course team: **Ecayci Lover**
  - Faiz Ramadhan (241111011) — Scrum Master + Developer
  - Dico Havianto (241111017) — Product Owner
- Repo: https://github.com/Faeest
- Deliverables are graded as part of the course; docs are written in Indonesian.

## Hardware

- Main board: **ESP32** — has built-in WiFi + Bluetooth, so no external wireless module.
- Motor driver: **L298N**. Two DC motors, one per channel:

  | Signal | Meaning |
  |--------|---------|
  | IN1, IN2 | direction of Motor A |
  | IN3, IN4 | direction of Motor B |
  | ENA | PWM enable for Motor A |
  | ENB | PWM enable for Motor B |
  | OUT1/OUT2, OUT3/OUT4 | motor outputs |
  | 12V | external motor supply |
  | 5V, GND | logic supply / ground |

- Motors: 2× DC motor. **External supply is required** — the ESP32 cannot power the motors.
- Course guide material also covers Arduino Uno + Arduino Shield V5.0; that is course
  context only. This project's board is the **ESP32**.

## Toolchain

- **Arduino IDE**, sketches are `.ino` (not PlatformIO, not ESP-IDF).
- Target board: **ESP32** — requires the Espressif ESP32 board package installed via
  Arduino IDE Boards Manager. "Arduino Uno" is the wrong board target.
- Build / flash: Arduino IDE toolbar (Verify / Upload). There is **no CLI build, no test
  runner, no CI** — do not invent `npm`/`pytest`/`make` commands.
- "Testing" = flash to the physical car and exercise it over Bluetooth/WiFi. State clearly
  when a change is unverified on hardware.

## Layout

- `firmware/rc_car/rc_car.ino` — the Arduino sketch (folder name must match sketch name).
- `firmware/README.md` — hardware TODO list (pin map, protocol, modes).
- `firmware/secrets.h` — WiFi/BLE credentials, **gitignored**. `secrets.example.h` is the template.
- `docs/` — course deliverables (team profile, reports). Indonesian prose.

## Gotchas

- **Never commit WiFi SSID/password or Bluetooth keys.** Put them in `firmware/secrets.h`
  (gitignored) and `#include` it.
- ESP32 logic is **3.3V**; L298N is designed around 5V logic. 3.3V is usually read as HIGH,
  but treat ENA/ENB PWM as needing verification on the bench.
- **Common ground** between the ESP32 and the L298N is mandatory, and motors must run from
  the external supply, never from the ESP32.
- ESP32 WiFi and Bluetooth share the radio — don't assume both run at full rate at once.
- Pin map, PWM values, and command protocol are **not yet fixed** — see `firmware/README.md`.
  Confirm real wiring before hardcoding pins.
- Docs and code comments are Indonesian; keep new docs consistent.

## Course deliverables

- `docs/tugas-1-profil-tim.md` — Tugas 1 (5%): team profile, roles, project vision.
