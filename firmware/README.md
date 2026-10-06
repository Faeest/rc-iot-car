# Firmware — IoT RC Car

Sketch Arduino (`.ino`) untuk mengendalikan mobil RC lewat Bluetooth dan WiFi.
Papan utama: **Arduino Uno + Arduino Shield V5.0**. Motor driver: **L298N** (2 motor DC).

## Struktur

- `rc_car/rc_car.ino` — sketch utama (nama folder harus sama dengan nama sketch).
- `rc_car/secrets.example.h` — template kredensial; salin jadi
  `rc_car/secrets.h` (di-gitignore). File harus ada di dalam folder sketch
  karena Arduino IDE hanya meng-compile file di dalam folder sketch.

## TODO — konfirmasi sebelum hardcoding

Nilai-nilai di bawah **belum pasti** dan harus dicek ke wiring/hardware asli:

- Pin Arduino Uno → L298N:
  - `IN1` / `IN2` (arah Motor A): `[TBD]`
  - `IN3` / `IN4` (arah Motor B): `[TBD]`
  - `ENA` / `ENB` (PWM): `[TBD]` — **wajib** di pin PWM Uno: 3, 5, 6, 9, 10, 11.
- Kecepatan motor (nilai PWM default): `[TBD]`
- Modul Bluetooth: **HC-05** (sudah pasti) — konektor mana di shield, dan baud rate-nya? `[TBD]`
- Fungsi sensor ultrasonic (mis. deteksi rintangan / ukur jarak): `[TBD]`
- Pin Trig/Echo ultrasonic: `[TBD]`
- Protokol perintah (mis. `F` maju, `B` mundur, `S` berhenti): `[TBD]`

## Komponen yang TIDAK dipakai

Jangan tambahkan kode/pin/library untuk: **I2C, sensor infrared (IR), dan LCD**.
Sensor yang dipakai hanya **ultrasonic**.

## Catatan WiFi

Kit hanya menyertakan modul **HC-05 (Bluetooth)** — tidak ada modul WiFi.
Perlu dikonfirmasi apakah WiFi benar-benar masuk scope.

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

Catatan: motor **wajib** disuplai dari sumber eksternal, dan GND Arduino Uno harus
disatukan dengan GND L298N.

## Catatan PWM (penting)

Arduino Uno **tidak** punya `ledcSetup` / `ledcWrite` (itu khusus ESP32). Gunakan
`analogWrite()`, dan hanya pada pin **3, 5, 6, 9, 10, 11**.

## Cara build & flash

### Cek compile tanpa hardware (arduino-cli)

```bash
# butuh rc_car/secrets.h (salin dari secrets.example.h; di-gitignore)
arduino-cli compile --fqbn arduino:avr:uno firmware/rc_car
```

### Lewat Arduino IDE

1. Buka `firmware/rc_car/rc_car.ino` di Arduino IDE.
2. Pilih board **Arduino Uno**.
3. Verify → Upload.
4. Uji langsung di mobil.
