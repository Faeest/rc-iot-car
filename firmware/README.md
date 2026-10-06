# Firmware — IoT RC Car

Sketch Arduino (`.ino`) untuk mengendalikan mobil RC lewat Bluetooth dan WiFi.
Papan utama: **ESP32**. Motor driver: **L298N** (2 motor DC).

## Struktur

- `rc_car/rc_car.ino` — sketch utama (nama folder harus sama dengan nama sketch).
- `secrets.example.h` — template kredensial; salin jadi `secrets.h` (di-gitignore).

## TODO — konfirmasi sebelum hardcoding

Nilai-nilai di bawah **belum pasti** dan harus dicek ke wiring/hardware asli:

- Pin ESP32 → L298N:
  - `IN1` / `IN2` (arah Motor A): `[TBD]`
  - `IN3` / `IN4` (arah Motor B): `[TBD]`
  - `ENA` / `ENB` (PWM): `[TBD]` — pastikan pin mendukung PWM ESP32.
- Nilai PWM (frekuensi, resolusi LEDC): `[TBD]`
- Mode Bluetooth: BLE atau Bluetooth klasik (SPP)? `[TBD]`
- Mode WiFi: AP (ESP32 jadi hotspot) atau STA (nyambung ke WiFi yang ada)? `[TBD]`
- Protokol perintah (mis. `F` maju, `B` mundur, `S` berhenti): `[TBD]`
- Kecepatan motor (nilai PWM default): `[TBD]`

## Referensi L298N

| Pin | Deskripsi |
|-----|-----------|
| IN1 & IN2 | arah putaran Motor A |
| IN3 & IN4 | arah putaran Motor B |
| ENA | enable PWM Motor A |
| ENB | enable PWM Motor B |
| OUT1 & OUT2 | output Motor A |
| OUT3 & OUT4 | output Motor B |
| 12V | input daya motor (suplai eksternal) |
| 5V | daya logika IC L298N |
| GND | ground |

Catatan: motor **wajib** disuplai dari sumber eksternal, dan GND ESP32 harus disatukan
dengan GND L298N.

## Cara build & flash

1. Install board package ESP32 (Espressif) lewat Boards Manager.
2. Buka `firmware/rc_car/rc_car.ino` di Arduino IDE.
3. Pilih board **ESP32**.
4. Verify → Upload.
5. Uji langsung di mobil.
