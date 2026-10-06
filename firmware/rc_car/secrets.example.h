// Salin file ini menjadi `secrets.h` lalu isi nilainya.
// `secrets.h` di-gitignore — JANGAN commit kredensial asli.
#pragma once

// HC-05: nama yang muncul saat pairing dan PIN/passkey-nya.
#define BT_NAME    "RC-CAR"
#define BT_PASSKEY "1234"

// WiFi hanya bila memang dipakai (kit saat ini belum ada modul WiFi).
#define WIFI_SSID     "isi-ssid-di-sini"
#define WIFI_PASSWORD "isi-password-di-sini"
