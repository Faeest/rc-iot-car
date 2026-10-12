---
tugas: TUGAS 1
title: Profil Tim dan Pembagian Peran
course: Application Project II
lecturer: Jozua Ferjanus Palandi
team: Ecayci Lover
author: Faiz Ramadhan (241111011), Dico Havianto (241111017)
prodi: Program Studi Informatika
fakultas: Fakultas Sains dan Teknologi
university: Universitas Bhinneka Nusantara
city: Malang
year: "2026"
---

# Profil Tim dan Pembagian Peran

## 1. Pendahuluan

Dokumen ini memuat profil tim **Ecayci Lover** beserta pembagian peran dan
tanggung jawab dalam pelaksanaan proyek mata kuliah Application Project II.
Dokumen juga menjelaskan visi proyek yang akan dikembangkan serta kesepakatan
kerja yang menjadi acuan seluruh anggota tim selama pengerjaan berlangsung.

## 2. Profil Tim

Tim Ecayci Lover beranggotakan dua orang mahasiswa Program Studi Informatika,
Fakultas Sains dan Teknologi, Universitas Bhinneka Nusantara. Susunan anggota
beserta perannya disajikan pada Tabel 2.1.

Tabel 2.1 Susunan Anggota dan Peran Tim
{: .table-caption }

| Nama | NIM | Peran |
|------|-----|-------|
| Dico Havianto | 241111017 | Product Owner |
| Faiz Ramadhan | 241111011 | Scrum Master dan Developer |

Oleh karena tim hanya beranggotakan dua orang, peran *Scrum Master* dan
*Developer* dirangkap oleh satu orang, yaitu Faiz Ramadhan. Pembagian ini
dilakukan agar seluruh peran dalam kerangka kerja Scrum tetap terisi tanpa
menambah beban administrasi yang tidak perlu.

## 3. Visi Proyek

Visi proyek ini adalah **menghadirkan mobil RC yang dapat dikendalikan secara
nirkabel dan aman dengan biaya rendah, melalui firmware yang andal di atas
mikrokontroler Arduino Uno**.

Untuk mewujudkan visi tersebut, tim mengembangkan perangkat lunak (firmware)
mobil RC berbasis IoT menggunakan mikrokontroler **Arduino Uno** dengan
**Arduino Shield V5.0** sebagai perluasan pin, serta **Motor Driver L298N**
untuk mengendalikan dua motor DC. Mobil dikendalikan secara nirkabel melalui
**Bluetooth**. Ruang lingkup pengembangan kode meliputi:

1. kontrol gerak dasar, yaitu maju dan mundur, serta pengembangan arah lain bila
   diperlukan;
2. kontrol arah dan kecepatan motor melalui pin IN1–IN4 dan PWM pada ENA/ENB
   L298N;
3. kendali nirkabel melalui Bluetooth menggunakan modul HC-05 yang terpasang
   pada konektor Bluetooth di Arduino Shield V5.0; dan
4. pembacaan sensor ultrasonic untuk mendukung fungsi keselamatan.

Perangkat keras yang digunakan, yaitu Arduino Uno, Arduino Shield V5.0, Motor
Driver L298N, dua motor DC, modul Bluetooth HC-05, sensor ultrasonic, dan
baterai, telah tersedia dan berfungsi. Dengan demikian, fokus pekerjaan tim
adalah pengembangan perangkat lunaknya.

## 4. Pembagian Tanggung Jawab

Setiap peran memiliki tanggung jawab yang jelas agar pekerjaan dapat berjalan
tanpa tumpang tindih. Uraian tanggung jawab masing-masing peran disajikan pada
Tabel 4.1.

Tabel 4.1 Uraian Tanggung Jawab Tiap Peran
{: .table-caption }

| Peran | Pemegang Peran | Tanggung Jawab |
|-------|----------------|----------------|
| Product Owner | Dico Havianto | Menentukan prioritas fitur, menjaga visi proyek, dan memvalidasi hasil terhadap kebutuhan pengguna |
| Scrum Master | Faiz Ramadhan | Memfasilitasi proses kerja tim dan menghilangkan hambatan yang muncul |
| Developer | Faiz Ramadhan | Menulis, menguji, dan memelihara firmware |

## 5. Kesepakatan Kerja Tim

Agar proses kerja berjalan konsisten, tim menyepakati sejumlah aturan kerja
sebagaimana disajikan pada Tabel 5.1.

Tabel 5.1 Kesepakatan Kerja Tim
{: .table-caption }

| Aspek | Kesepakatan |
|-------|-------------|
| Ritme kerja | Sprint mingguan, diakhiri demonstrasi singkat pada mobil sesungguhnya |
| Definisi selesai | Kode berhasil dikompilasi untuk board Arduino Uno dan telah diuji pada perangkat keras |
| Repositori | Seluruh kode dan dokumen disimpan pada GitHub dengan pesan commit yang deskriptif |
| Kredensial | Tidak ada SSID, kata sandi, atau PIN yang di-commit; disimpan pada berkas `secrets.h` yang diabaikan Git |
| Komunikasi | Diskusi harian singkat; hambatan langsung dilaporkan kepada Scrum Master |

## 6. Repositori Proyek

Seluruh hasil pekerjaan tim, baik kode maupun dokumen, disimpan pada repositori
GitHub berikut:

<https://github.com/Faeest/rc-iot-car>

## 7. Penutup

Dokumen profil tim ini menjadi acuan awal pelaksanaan proyek. Dengan pembagian
peran dan kesepakatan kerja yang jelas, tim diharapkan dapat menyelesaikan
pengembangan firmware mobil RC IoT secara terarah, terukur, dan tepat waktu.
