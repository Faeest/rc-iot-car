# Tugas 1 — Profil Tim dan Pembagian Peran

**Mata Kuliah:** Application Project II
**Dosen Pengampu:** Jozua Ferjanus Palandi
**Nama Tim:** Ecayci Lover
**Bobot:** 5% (Tugas)

## Anggota dan Peran

| Nama | NIM | Peran |
|------|-----|-------|
| Dico Havianto | 241111017 | Product Owner |
| Faiz Ramadhan | 241111011 | Scrum Master + Developer |

## Visi Proyek

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

> Catatan: tim hanya beranggotakan 2 orang, sehingga peran Scrum Master dan Developer
> dirangkap oleh Faiz Ramadhan.

## Tautan Repositori GitHub

https://github.com/Faeest/rc-iot-car
