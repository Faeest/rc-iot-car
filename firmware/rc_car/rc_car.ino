/*
 * rc_car.ino — Firmware mobil RC IoT (Arduino Uno + Arduino Shield V5.0 + L298N)
 * Tim: Ecayci Lover — Faiz Ramadhan (241111011), Dico Havianto (241111017)
 *
 * SKELETON. Pin dan nilai PWM di bawah BELUM diverifikasi terhadap wiring asli.
 * Isi nilai [TBD] setelah mengecek hardware. Lihat firmware/README.md.
 *
 * CATATAN: PWM di Arduino Uno hanya lewat analogWrite() pada pin 3, 5, 6, 9, 10, 11.
 * Jangan pakai ledcSetup/ledcWrite (itu khusus ESP32, tidak akan ter-compile di Uno).
 */

#include "secrets.h"

// ---------------------------------------------------------------------------
// PIN — TODO: isi sesuai wiring asli.
// ENA/ENB WAJIB di pin PWM Uno: 3, 5, 6, 9, 10, atau 11.
// Hindari pin yang sudah dipakai Arduino Shield V5.0.
// ---------------------------------------------------------------------------
#define PIN_IN1  -1  // [TBD] arah Motor A
#define PIN_IN2  -1  // [TBD] arah Motor A
#define PIN_IN3  -1  // [TBD] arah Motor B
#define PIN_IN4  -1  // [TBD] arah Motor B
#define PIN_ENA  -1  // [TBD] PWM Motor A (harus pin PWM Uno)
#define PIN_ENB  -1  // [TBD] PWM Motor B (harus pin PWM Uno)

// ---------------------------------------------------------------------------
// KONFIGURASI
// ---------------------------------------------------------------------------
#define SPEED_DEFAULT  200  // [TBD] 0..255

// ---------------------------------------------------------------------------
// KONTROL MOTOR
// ---------------------------------------------------------------------------
void motorA(int speed) {          // speed: -255..255
  bool forward = speed >= 0;
  int pwm = forward ? speed : -speed;
  digitalWrite(PIN_IN1, forward ? HIGH : LOW);
  digitalWrite(PIN_IN2, forward ? LOW : HIGH);
  analogWrite(PIN_ENA, pwm);
}

void motorB(int speed) {
  bool forward = speed >= 0;
  int pwm = forward ? speed : -speed;
  digitalWrite(PIN_IN3, forward ? HIGH : LOW);
  digitalWrite(PIN_IN4, forward ? LOW : HIGH);
  analogWrite(PIN_ENB, pwm);
}

void stopAll() {
  motorA(0);
  motorB(0);
}

void moveForward(int speed) {
  motorA(speed);
  motorB(speed);
}

void moveBackward(int speed) {
  motorA(-speed);
  motorB(-speed);
}

// ---------------------------------------------------------------------------
// PERINTAH — TODO: sesuaikan protokol
// ---------------------------------------------------------------------------
void handleCommand(char c) {
  switch (c) {
    case 'F': moveForward(SPEED_DEFAULT); break;  // maju
    case 'B': moveBackward(SPEED_DEFAULT); break; // mundur
    case 'S': stopAll(); break;                   // stop
    default: break;
  }
}

// ---------------------------------------------------------------------------
// TRANSPORT — TODO: implementasi Bluetooth dan WiFi
// Modul Bluetooth/WiFi dipasang di konektor Arduino Shield V5.0.
// Keduanya umumnya berkomunikasi lewat Serial.
// ---------------------------------------------------------------------------
void setupBluetooth() {
  // [TBD] modul apa (HC-05/HC-06/dll) dan lewat Serial mana?
}

void setupWiFi() {
  // [TBD] modul apa, AP atau STA? Gunakan WIFI_SSID / WIFI_PASSWORD dari secrets.h
}

// ---------------------------------------------------------------------------
void setup() {
  Serial.begin(9600);

  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_IN3, OUTPUT);
  pinMode(PIN_IN4, OUTPUT);
  pinMode(PIN_ENA, OUTPUT);
  pinMode(PIN_ENB, OUTPUT);

  stopAll();

  setupBluetooth();
  setupWiFi();
}

void loop() {
  // [TBD] baca perintah dari Bluetooth / WiFi lalu panggil handleCommand()
}
