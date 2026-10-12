---
title: Profil Tim dan Pembagian Peran
subtitle: Proyek Firmware Mobil RC IoT
kicker: Tugas 1 — Bobot 5%
course: Application Project II
lecturer: Jozua Ferjanus Palandi
team: Ecayci Lover
author: Faiz Ramadhan (241111011), Dico Havianto (241111017)
repo: https://github.com/Faeest/rc-iot-car
date: 2026
---

# Profil Tim dan Pembagian Peran

## Anggota dan Peran

| Nama | NIM | Peran |
|------|-----|-------|
| Dico Havianto | 241111017 | Product Owner |
| Faiz Ramadhan | 241111011 | Scrum Master + Developer |

> Tim beranggotakan 2 orang, sehingga peran **Scrum Master** dan **Developer**
> dirangkap oleh Faiz Ramadhan.

## Visi Proyek

> Menghadirkan mobil RC yang dapat dikendalikan secara nirkabel dan aman, dengan
> biaya rendah, melalui firmware yang andal di atas Arduino Uno.

Mengembangkan perangkat lunak (firmware) untuk mobil RC berbasis IoT menggunakan
mikrokontroler **Arduino Uno** dengan **Arduino Shield V5.0** sebagai perluasan pin,
serta **Motor Driver L298N** untuk mengendalikan 2 motor DC, sehingga mobil dapat
dikendalikan secara nirkabel melalui **Bluetooth**.

Ruang lingkup pengembangan kode:

- Kontrol gerak dasar: maju dan mundur (serta pengembangan arah lain bila diperlukan).
- Kontrol arah dan kecepatan motor melalui pin IN1–IN4 dan PWM pada ENA/ENB L298N.
- Kendali nirkabel melalui **Bluetooth (modul HC-05)** yang terpasang pada konektor
  Bluetooth di Arduino Shield V5.0.
- Pembacaan **sensor ultrasonic**.

Hardware (Arduino Uno, Arduino Shield V5.0, Motor Driver L298N, 2 motor DC, modul
Bluetooth HC-05, sensor ultrasonic, baterai) sudah tersedia dan berfungsi; fokus tugas
ini adalah pengembangan kode-nya.

## Pembagian Tanggung Jawab

- **Product Owner (Dico Havianto):** menentukan prioritas fitur, menjaga visi proyek,
  dan memvalidasi hasil terhadap kebutuhan pengguna.
- **Scrum Master (Faiz Ramadhan):** memfasilitasi proses kerja tim dan menghilangkan
  hambatan.
- **Developer (Faiz Ramadhan):** menulis dan menguji firmware.

## Kesepakatan Kerja Tim

| Aspek | Kesepakatan |
|-------|-------------|
| Ritme kerja | Sprint mingguan, diakhiri demo singkat di mobil sungguhan |
| Definisi selesai (*Definition of Done*) | Kode ter-compile untuk board Arduino Uno **dan** teruji di hardware |
| Repositori | Semua kode dan dokumen masuk ke GitHub; commit berpesan deskriptif |
| Kredensial | Tidak ada SSID/password/PIN yang di-commit (`secrets.h` di-gitignore) |
| Komunikasi | Diskusi harian singkat; hambatan langsung dilaporkan ke Scrum Master |

## Tautan Repositori GitHub

<https://github.com/Faeest/rc-iot-car>
