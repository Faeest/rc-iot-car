# Firmware — IoT RC Car

Sketch Arduino (`.ino`) untuk mengendalikan mobil RC lewat Bluetooth dan WiFi.
Papan utama: **Arduino Uno + Arduino Shield V5.0**.

## TODO — konfirmasi sebelum hardcoding

Nilai-nilai di bawah **belum pasti** dan harus dicek ke wiring/hardware asli:

- Model motor driver (mis. L298N / L293D / TB6612 / driver di shield): `[TBD]`
- Pin Arduino → motor driver (IN1, IN2, ENA, dst.) — hindari pin yang sudah dipakai shield: `[TBD]`
- Nilai PWM (frekuensi, resolusi) di Arduino Uno: `[TBD]`
- Modul Bluetooth (mis. HC-05 / HC-06) + konektor yang dipakai di shield: `[TBD]`
- Modul wireless untuk WiFi (mis. ESP8266 / ESP32) + konektornya: `[TBD]`
- Mode WiFi: AP (modul jadi hotspot) atau STA (nyambung ke WiFi yang ada)? `[TBD]`
- Protokol perintah (mis. `F`, `B`, `S`): `[TBD]`

> Konflik yang perlu dipastikan: catatan awal menyebut mobil memakai **ESP32**, tetapi panduan
> mata kuliah menyebut **Arduino Uno + Shield V5.0** sebagai papan utama. Pastikan dulu apakah
> ESP32 adalah modul WiFi yang ditancapkan ke shield, atau board terpisah.

## Secrets

WiFi SSID/password jangan di-commit. Salin `secrets.example.h` menjadi `secrets.h`
dan isi nilainya; `secrets.h` sudah masuk `.gitignore`.

## Cara build & flash

1. Buka folder `firmware/` di Arduino IDE.
2. Pilih board **Arduino Uno**.
3. Verify → Upload.
4. Uji langsung di mobil.
