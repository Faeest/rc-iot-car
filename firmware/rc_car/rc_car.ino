/*
 * rc_car.ino — Firmware mobil RC IoT (ESP32 + Motor Driver L298N)
 * Tim: Ecayci Lover — Faiz Ramadhan (241111011), Dico Havianto (241111017)
 *
 * SKELETON. Pin dan nilai PWM di bawah BELUM diverifikasi terhadap wiring asli.
 * Isi nilai [TBD] setelah mengecek hardware. Lihat firmware/README.md.
 */

#include "secrets.h"

// ---------------------------------------------------------------------------
// PIN — TODO: isi sesuai wiring asli. Gunakan pin ESP32 yang mendukung PWM
// untuk ENA/ENB.
// ---------------------------------------------------------------------------
#define PIN_IN1  -1  // [TBD] arah Motor A
#define PIN_IN2  -1  // [TBD] arah Motor A
#define PIN_IN3  -1  // [TBD] arah Motor B
#define PIN_IN4  -1  // [TBD] arah Motor B
#define PIN_ENA  -1  // [TBD] PWM Motor A
#define PIN_ENB  -1  // [TBD] PWM Motor B

// ---------------------------------------------------------------------------
// KONFIGURASI PWM — TODO: sesuaikan
// ---------------------------------------------------------------------------
#define PWM_FREQ       5000
#define PWM_RESOLUTION 8
#define PWM_CH_A       0
#define PWM_CH_B       1
#define SPEED_DEFAULT  200  // [TBD] 0..255

// ---------------------------------------------------------------------------
// KONTROL MOTOR
// ---------------------------------------------------------------------------
void motorA(int speed) {          // speed: -255..255
  bool forward = speed >= 0;
  int pwm = forward ? speed : -speed;
  digitalWrite(PIN_IN1, forward ? HIGH : LOW);
  digitalWrite(PIN_IN2, forward ? LOW : HIGH);
  ledcWrite(PWM_CH_A, pwm);
}

void motorB(int speed) {
  bool forward = speed >= 0;
  int pwm = forward ? speed : -speed;
  digitalWrite(PIN_IN3, forward ? HIGH : LOW);
  digitalWrite(PIN_IN4, forward ? LOW : HIGH);
  ledcWrite(PWM_CH_B, pwm);
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
// ---------------------------------------------------------------------------
void setupBluetooth() {
  // [TBD] BLE atau Bluetooth klasik (SPP)?
}

void setupWiFi() {
  // [TBD] AP atau STA? Gunakan WIFI_SSID / WIFI_PASSWORD dari secrets.h
}

// ---------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);

  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_IN3, OUTPUT);
  pinMode(PIN_IN4, OUTPUT);

  ledcSetup(PWM_CH_A, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(PIN_ENA, PWM_CH_A);
  ledcSetup(PWM_CH_B, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(PIN_ENB, PWM_CH_B);

  stopAll();

  setupBluetooth();
  setupWiFi();
}

void loop() {
  // [TBD] baca perintah dari Bluetooth / WiFi lalu panggil handleCommand()
}
