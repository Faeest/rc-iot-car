# AGENTS.md

## What this repo is

Firmware for an **IoT RC car** — drives 2 DC motors through an **L298N** motor driver,
controlled over Bluetooth and WiFi from an **Arduino Uno + Arduino Shield V5.0**.
This is the code-development part of an already-working hardware build.

**Do NOT assume this is a web app.** The course ("Application Project II", 2 SKS, semester 5,
dosen: Jozua Ferjanus Palandi) advertises itself as Laravel Livewire. It is not — there is no
PHP/Laravel here. Scope is embedded firmware only.

- Course team: **Ecayci Lover**
  - Faiz Ramadhan (241111011) — Scrum Master + Developer
  - Dico Havianto (241111017) — Product Owner
- Repo: https://github.com/Faeest/rc-iot-car
- Deliverables are graded as part of the course; docs are written in Indonesian.

## Hardware

- Main board: **Arduino Uno** (ATmega328P, AVR, 5V logic).
- Expansion: **Arduino Shield V5.0** — required because the Uno has too few pins.
  Breaks out Analog I/O (A0–A5), Digital I/O (D0–D13), External Power, SD/SPI, Ultrasonic,
  a **Bluetooth connector**, a **Wireless connector**, LCD (parallel & serial), and I2C.
  The `SEL` jumper selects the VCC source feeding the I/O headers.
- The Uno has **no built-in WiFi or Bluetooth** — wireless comes from modules plugged into
  the shield's Bluetooth / Wireless connectors. **Module models are not yet confirmed.**
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

- Motors: 2× DC motor. **External supply is required** — the Uno cannot power the motors.

## Toolchain

- **Arduino IDE**, sketches are `.ino` (not PlatformIO, not ESP-IDF).
- Target board: **Arduino Uno** (AVR). The Uno is 5V logic — do not write 3.3V-only code.
- Build / flash: Arduino IDE toolbar (Verify / Upload). There is **no CLI build, no test
  runner, no CI** — do not invent `npm`/`pytest`/`make` commands.
- "Testing" = flash to the physical car and exercise it over Bluetooth/WiFi. State clearly
  when a change is unverified on hardware.

## Gotchas

- **PWM on the Uno is `analogWrite()` only.** `ledcSetup` / `ledcWrite` / `ledcAttachPin`
  are **ESP32-only** and will NOT compile here. `analogWrite` works only on pins
  **3, 5, 6, 9, 10, 11** — route ENA/ENB there.
- **Tight resources:** ATmega328P has 32 KB flash / 2 KB SRAM. Avoid large buffers and
  heavy libraries; watch the "Low memory available" warning.
- **Never commit WiFi SSID/password or Bluetooth keys.** Put them in
  `firmware/rc_car/secrets.h` (gitignored) and `#include` it.
- **Common ground** between the Uno and the L298N is mandatory, and motors must run from
  the external supply, never from the Uno.
- The shield already claims pins (SPI/SD, LCD, connector headers). Don't assign a pin the
  shield is using.
- Pin map, PWM values, wireless module models, and command protocol are **not yet fixed** —
  see `firmware/README.md`. Confirm real wiring before hardcoding pins.
- Docs and code comments are Indonesian; keep new docs consistent.

## Layout

- `firmware/rc_car/rc_car.ino` — the Arduino sketch. Arduino IDE only compiles files
  **inside the sketch folder**, so every file the sketch needs (including `secrets.h`)
  must live in `firmware/rc_car/`, not in `firmware/`.
- `firmware/rc_car/secrets.h` — WiFi/BLE credentials, **gitignored**.
  `firmware/rc_car/secrets.example.h` is the template.
- `firmware/README.md` — hardware TODO list (pin map, protocol, modes).
- `docs/` — course deliverables (team profile, reports). Indonesian prose.

## Course deliverables

- `docs/tugas-1-profil-tim.md` — Tugas 1 (5%): team profile, roles, project vision.
