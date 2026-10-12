---
title: Software Requirements Specification
subtitle: Sistem Kontrol Mobil RC IoT Berbasis Arduino Uno
kicker: Tugas 2 — Bobot 5%
course: Application Project II
lecturer: Jozua Ferjanus Palandi
team: Ecayci Lover
author: Faiz Ramadhan (241111011), Dico Havianto (241111017)
repo: https://github.com/Faeest/rc-iot-car
date: 2026
---

# Software Requirements Specification (SRS)

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

Dokumen ini merupakan *Software Requirements Specification* (SRS) untuk **Sistem
Kontrol Mobil RC IoT** yang dikembangkan oleh tim **Ecayci Lover**. Dokumen
menjabarkan kebutuhan fungsional, kebutuhan non-fungsional, serta pemodelan
*use case* sebagai acuan tunggal bagi pengembang dalam menulis dan menguji
firmware. Dokumen ditulis mengikuti struktur umum IEEE 830 yang disederhanakan
agar sesuai dengan skala proyek mata kuliah.

### 1.2 Ruang Lingkup Produk

Produk yang dibangun adalah **firmware** yang berjalan pada mikrokontroler
**Arduino Uno** yang dipasangkan **Arduino Shield V5.0**, dan mengendalikan
**2 (dua) motor DC** melalui **motor driver L298N**. Mobil dikendalikan secara
nirkabel melalui **Bluetooth (modul HC-05)** dan dilengkapi **sensor ultrasonic**
untuk membaca jarak objek di depan mobil.

Fokus pengembangan adalah **perangkat lunak (firmware)**. Perangkat keras
(Arduino Uno, Shield V5.0, L298N, 2 motor DC, HC-05, sensor ultrasonic, dan
baterai) sudah tersedia dan berfungsi.

### 1.3 Definisi, Akronim, dan Singkatan

| Istilah | Keterangan |
|---------|------------|
| **Firmware** | Perangkat lunak yang ditanamkan pada mikrokontroler (sketch `.ino`) |
| **PWM** | *Pulse Width Modulation* — teknik mengatur kecepatan motor via `analogWrite()` |
| **L298N** | Modul *dual H-bridge* sebagai driver 2 motor DC |
| **HC-05** | Modul Bluetooth klasik (SPP) untuk komunikasi serial nirkabel |
| **Ultrasonic** | Sensor jarak HC-SR04-class (pin Trig & Echo) |
| **E-Stop** | *Emergency Stop* — perintah menghentikan seluruh motor seketika |
| **UML** | *Unified Modeling Language* — notasi pemodelan *use case* |
| **SRS** | *Software Requirements Specification* |

### 1.4 Referensi

1. `AGENTS.md` — konteks proyek dan batasan teknis repositori.
2. `firmware/README.md` — daftar TODO pin map, protokol perintah, dan mode.
3. `docs/tugas-1-profil-tim.md` — profil tim dan visi proyek.
4. Datasheet Arduino Uno (ATmega328P) dan modul L298N.

### 1.5 Ikhtisar Dokumen

Bagian 2 menjelaskan gambaran umum produk. Bagian 3 memuat kebutuhan fungsional,
Bagian 4 kebutuhan non-fungsional, dan Bagian 5 memuat pemodelan *use case*
(diagram beserta deskripsi rinci). Bagian 6 menjelaskan antarmuka dan protokol
perintah, sedangkan Bagian 7 memuat batasan dan asumsi.

## 2. Deskripsi Umum

### 2.1 Perspektif Produk

Sistem merupakan produk mandiri (*stand-alone embedded system*) yang tidak
bergantung pada server. Mobil berkomunikasi langsung (*point-to-point*) dengan
aplikasi kontrol pengguna melalui Bluetooth. Arsitektur tingkat tinggi:

```
[Aplikasi Kontrol Pengguna]  (smartphone / PC)
            |
            |  Bluetooth (SPP, HC-05)
            v
+---------------------------------------------------+
|             ARDUINO UNO + SHIELD V5.0             |
|                                                   |
|  Firmware: parsing perintah -> kontrol motor      |
|            baca sensor ultrasonic -> laporan      |
+---------------------------------------------------+
        |                              |
        | PWM + arah (IN1-IN4, ENA/ENB) | Trig / Echo
        v                              v
   [ MOTOR DRIVER L298N ]        [ SENSOR ULTRASONIC ]
        |                              |
        v                          (jarak objek)
   [ 2x MOTOR DC ]  <- [ BATERAI 3.2V + SUPLAI EKSTERNAL ]
```

### 2.2 Fungsi Produk

1. **Koneksi** — menyediakan jalur komunikasi Bluetooth antara pengguna dan mobil.
2. **Kontrol gerak** — mengendalikan arah gerak (maju, mundur, belok kiri/kanan).
3. **Kontrol kecepatan** — mengatur kecepatan motor melalui PWM.
4. **Berhenti darurat** — menghentikan seluruh motor seketika (*E-Stop*).
5. **Mode hindari rintangan** — mobil otomatis berhenti/menghindar saat ada rintangan.
6. **Telemetri jarak** — mengirimkan hasil pembacaan sensor ultrasonic ke pengguna.

### 2.3 Karakteristik Pengguna

| Pengguna | Karakteristik |
|----------|---------------|
| Pengguna umum | Dapat mengoperasikan smartphone, tanpa pengetahuan teknis khusus |
| Pengembang | Memahami dasar mikrokontroler, rangkaian, dan bahasa C/C++ Arduino |

### 2.4 Batasan (Constraints)

- **Mikrokontroler:** Arduino Uno (ATmega328P) — **32 KB flash / 2 KB SRAM**;
  tidak boleh menggunakan pustaka besar.
- **Logika 5V.** Tidak boleh menulis kode khusus 3.3V.
- **PWM** hanya tersedia di pin **3, 5, 6, 9, 10, 11** dan hanya melalui
  `analogWrite()`. Fungsi `ledcSetup`/`ledcWrite` (khusus ESP32) **tidak boleh** dipakai.
- **Komponen yang tidak dipakai:** I2C, sensor infrared (IR), dan LCD — tidak
  boleh ditambahkan kode/pin/pustaka untuk ketiganya.
- **Kredensial** (PIN Bluetooth, bila ada) tidak boleh di-commit ke repositori;
  disimpan di `secrets.h` yang di-*gitignore*.
- **Daya:** motor wajib disuplai dari sumber eksternal; GND Arduino dan L298N
  harus disatukan.

### 2.5 Asumsi dan Ketergantungan

- Modul Bluetooth yang dipakai adalah **HC-05** (sesuai kit).
- Kit **belum menyediakan modul WiFi**; kebutuhan WiFi bersifat opsional dan
  menunggu konfirmasi lingkup dari dosen (lihat Bagian 7).
- Nilai pin, baud rate, dan nilai PWM final ditentukan saat integrasi hardware
  dan dicatat di `firmware/README.md`.

## 3. Kebutuhan Fungsional

Kode: **FR-xx**. Prioritas memakai skala **MoSCoW** (*Must / Should / Could*).

| Kode | Kebutuhan | Prioritas |
|------|-----------|-----------|
| **FR-01** | Sistem harus menyediakan koneksi Bluetooth dan menerima perintah dari aplikasi pengguna. | <span class="badge must">Must</span> |
| **FR-02** | Sistem harus dapat menggerakkan mobil **maju** dan **mundur**. | <span class="badge must">Must</span> |
| **FR-03** | Sistem harus dapat membelokkan mobil **ke kiri** dan **ke kanan**. | <span class="badge must">Must</span> |
| **FR-04** | Sistem harus dapat menghentikan seluruh motor melalui perintah **stop**. | <span class="badge must">Must</span> |
| **FR-05** | Sistem harus dapat mengatur **kecepatan** motor melalui nilai PWM (0–255). | <span class="badge should">Should</span> |
| **FR-06** | Sistem harus dapat mengaktifkan **mode hindari rintangan** secara otomatis. | <span class="badge should">Should</span> |
| **FR-07** | Sistem harus membaca **jarak** dari sensor ultrasonic. | <span class="badge must">Must</span> |
| **FR-08** | Sistem harus mengirimkan **data jarak** hasil pembacaan ke aplikasi pengguna. | <span class="badge should">Should</span> |
| **FR-09** | Sistem harus menghentikan motor seketika saat perintah **E-Stop** diterima. | <span class="badge must">Must</span> |
| **FR-10** | Sistem harus **mengabaikan perintah tidak dikenal** tanpa mengubah kondisi motor. | <span class="badge must">Must</span> |
| **FR-11** | Sistem harus menghentikan motor secara **aman** jika koneksi Bluetooth terputus. | <span class="badge should">Should</span> |
| **FR-12** | Sistem harus mengirimkan **status/konfirmasi** perintah yang diterima. | <span class="badge could">Could</span> |

### 3.1 Rincian Kebutuhan Fungsional Utama

**FR-02 / FR-03 — Kontrol Gerak.** Sistem mengendalikan arah putaran tiap motor
dengan mengatur pin arah (`IN1`–`IN4`) pada L298N. Gerak maju dan mundur
menggerakkan kedua motor secara sinkron; belok kiri/kanan dicapai dengan
membalik arah salah satu motor.

**FR-05 — Kontrol Kecepatan.** Kecepatan diatur melalui `analogWrite()` pada pin
`ENA`/`ENB`. Nilai 0 berarti berhenti dan 255 berarti kecepatan maksimum. Nilai
default kecepatan ditetapkan pada konstanta `SPEED_DEFAULT`.

**FR-06 / FR-07 — Hindari Rintangan.** Saat mode ini aktif, sistem membaca jarak
dari sensor ultrasonic secara berkala; apabila jarak kurang dari ambang batas,
sistem menghentikan atau membelokkan mobil untuk mencegah tabrakan.

**FR-09 — E-Stop.** Perintah E-Stop harus diproses dengan prioritas tertinggi dan
langsung memanggil prosedur penghentian seluruh motor.

## 4. Kebutuhan Non-Fungsional

Kode: **NFR-xx**.

| Kode | Kategori | Kebutuhan |
|------|----------|-----------|
| **NFR-01** | Kinerja | Sistem merespons perintah gerak dalam **< 200 ms** sejak perintah diterima. |
| **NFR-02** | Kinerja | Loop utama berjalan tanpa *blocking delay* panjang agar kontrol tetap responsif. |
| **NFR-03** | Keandalan | Motor berhenti otomatis saat koneksi Bluetooth terputus. |
| **NFR-04** | Keandalan | Perintah tak dikenal tidak menyebabkan perilaku tak terduga. |
| **NFR-05** | Efisiensi Sumber Daya | Penggunaan flash **< 60%** dan SRAM **< 60%** dari kapasitas Arduino Uno. |
| **NFR-06** | Portabilitas | Firmware dikompilasi untuk *board* **Arduino Uno** melalui Arduino IDE. |
| **NFR-07** | Keamanan | Kredensial tidak disimpan di dalam repositori (di-gitignore). |
| **NFR-08** | Kemudahan Perawatan | Kode termodulasi (fungsi kontrol motor, transport, dan sensor terpisah). |
| **NFR-09** | Kegunaan | Protokol perintah sederhana (1 karakter per perintah) agar mudah diuji. |
| **NFR-10** | Dokumentasi | Setiap pin, nilai PWM, dan perintah didokumentasikan di `firmware/README.md`. |

## 5. Pemodelan Use Case

### 5.1 Diagram Use Case

Berikut adalah diagram *use case* sistem. Aktor utama adalah **Pengguna**;
**Sensor Ultrasonik** diperlakukan sebagai aktor pendukung (*supporting actor*)
karena menyediakan data jarak bagi sistem.

![Diagram Use Case Sistem Kontrol Mobil RC IoT](assets/usecase-diagram.svg)

### 5.2 Daftar Use Case

| Kode | Use Case | Aktor | Prioritas |
|------|----------|-------|-----------|
| **UC-01** | Menghubungkan ke Mobil | Pengguna | Must |
| **UC-02** | Mengendalikan Gerak Mobil | Pengguna | Must |
| **UC-03** | Mengatur Kecepatan | Pengguna | Should |
| **UC-04** | Menghentikan Mobil (E-Stop) | Pengguna | Must |
| **UC-05** | Mengaktifkan Mode Hindari Rintangan | Pengguna | Should |
| **UC-06** | Memantau Jarak Ultrasonik | Pengguna, Sensor Ultrasonik | Must |

### 5.3 Relasi Antar Use Case

- **UC-05 «include» UC-06** — mengaktifkan mode hindari rintangan selalu
  memerlukan pembacaan jarak ultrasonic.
- **UC-04 «extend» UC-02** — penghentian darurat (E-Stop) memperluas skenario
  pengendalian gerak ketika dibutuhkan.

### 5.4 Deskripsi Rinci Use Case

#### UC-01 — Menghubungkan ke Mobil

| Atribut | Keterangan |
|---------|------------|
| **Aktor** | Pengguna |
| **Prakondisi** | Mobil menyala dan modul HC-05 dalam kondisi *pairing*. |
| **Pascakondisi** | Koneksi Bluetooth terbentuk dan siap menerima perintah. |
| **Skenario utama** | 1) Pengguna mengaktifkan Bluetooth. 2) Pengguna memilih perangkat mobil. 3) Koneksi terbentuk. 4) Sistem siap menerima perintah. |
| **Skenario alternatif** | 3a) Koneksi gagal → pengguna mengulang proses *pairing*. |

#### UC-02 — Mengendalikan Gerak Mobil

| Atribut | Keterangan |
|---------|------------|
| **Aktor** | Pengguna |
| **Prakondisi** | Koneksi Bluetooth aktif (UC-01). |
| **Pascakondisi** | Mobil bergerak sesuai arah yang diperintahkan. |
| **Skenario utama** | 1) Pengguna menekan tombol arah. 2) Aplikasi mengirim perintah. 3) Sistem menetapkan pin arah motor. 4) Motor bergerak. |
| **Skenario alternatif** | 3a) Perintah tidak dikenal → sistem mengabaikan (FR-10). 3b) Koneksi terputus → sistem menghentikan motor (FR-11). |

#### UC-03 — Mengatur Kecepatan

| Atribut | Keterangan |
|---------|------------|
| **Aktor** | Pengguna |
| **Prakondisi** | Mobil dalam keadaan bergerak atau siap bergerak. |
| **Pascakondisi** | Nilai PWM motor berubah sesuai pilihan pengguna. |
| **Skenario utama** | 1) Pengguna menggeser pengatur kecepatan. 2) Aplikasi mengirim nilai. 3) Sistem memanggil `analogWrite()` pada ENA/ENB. 4) Kecepatan motor berubah. |

#### UC-04 — Menghentikan Mobil (E-Stop)

| Atribut | Keterangan |
|---------|------------|
| **Aktor** | Pengguna |
| **Prakondisi** | Mobil sedang bergerak. |
| **Pascakondisi** | Seluruh motor berhenti. |
| **Skenario utama** | 1) Pengguna menekan tombol E-Stop. 2) Sistem memanggil prosedur penghentian. 3) Seluruh motor berhenti. |
| **Catatan** | Diperlakukan sebagai *extend* terhadap UC-02 dan diproses dengan prioritas tertinggi. |

#### UC-05 — Mengaktifkan Mode Hindari Rintangan

| Atribut | Keterangan |
|---------|------------|
| **Aktor** | Pengguna |
| **Prakondisi** | Koneksi aktif dan sensor ultrasonic berfungsi. |
| **Pascakondisi** | Mobil berhenti/menghindar otomatis saat mendeteksi rintangan. |
| **Skenario utama** | 1) Pengguna mengaktifkan mode. 2) Sistem membaca jarak (UC-06). 3) Jika jarak < ambang, sistem menghentikan/membelokkan mobil. 4) Jika aman, mobil melanjutkan gerak. |
| **Relasi** | **«include»** UC-06. |

#### UC-06 — Memantau Jarak Ultrasonik

| Atribut | Keterangan |
|---------|------------|
| **Aktor** | Pengguna, Sensor Ultrasonik |
| **Prakondisi** | Sensor ultrasonic terpasang dan terhubung. |
| **Pascakondisi** | Nilai jarak diperoleh dan (bila diminta) dikirim ke pengguna. |
| **Skenario utama** | 1) Sistem memicu pin Trig. 2) Sistem mengukur durasi pantulan pada pin Echo. 3) Sistem menghitung jarak. 4) Sistem mengirim/menggunakan nilai jarak. |
| **Skenario alternatif** | 3a) Pembacaan tidak valid → sistem mengabaikan nilai tersebut. |

## 6. Antarmuka dan Protokol Perintah

### 6.1 Antarmuka Komunikasi

Komunikasi menggunakan **Bluetooth SPP** melalui modul HC-05 yang diakses
sebagai *serial port*. Setiap perintah direpresentasikan sebagai **satu karakter**.

### 6.2 Rancangan Protokol Perintah (draft)

| Perintah | Karakter | Aksi |
|----------|----------|------|
| Maju | `F` | Kedua motor maju |
| Mundur | `B` | Kedua motor mundur |
| Kiri | `L` | Belok kiri |
| Kanan | `R` | Belok kanan |
| Stop | `S` | Kedua motor berhenti |
| E-Stop | `X` | Hentikan seluruh motor seketika |
| Mode hindari | `A` | Aktif/nonaktif mode hindari rintangan |

> Nilai final protokol (termasuk baud rate dan pin) masih berstatus `[TBD]` dan
> akan difinalkan saat integrasi hardware. Rancangan ini menjadi acuan awal.

### 6.3 Antarmuka Perangkat Keras

| Antarmuka | Pin / Sinyal | Keterangan |
|-----------|--------------|------------|
| Motor A | `IN1`, `IN2`, `ENA` | Arah + PWM motor kiri |
| Motor B | `IN3`, `IN4`, `ENB` | Arah + PWM motor kanan |
| Bluetooth | Serial (HC-05) | RX/TX modul pada konektor shield |
| Ultrasonic | `Trig`, `Echo` | Pemicu dan pembacaan pantulan |

## 7. Batasan dan Asumsi Tambahan

1. **WiFi belum tersedia.** Kit hanya menyertakan HC-05; belum ada modul WiFi.
   Kebutuhan WiFi bersifat **opsional** dan menunggu konfirmasi lingkup.
2. **Daya.** L298N membutuhkan suplai motor sekitar 5–12 V, sedangkan baterai kit
   **3.2 V**; kesesuaian daya perlu diverifikasi agar motor dapat bergerak.
3. **Pin belum final.** Pin map, nilai PWM, dan perilaku ultrasonic masih
   berstatus `[TBD]` (lihat `firmware/README.md`).

## 8. Matriks Keterlacakan (Traceability)

| Use Case | Kebutuhan Fungsional Terkait |
|----------|------------------------------|
| UC-01 | FR-01 |
| UC-02 | FR-02, FR-03, FR-10 |
| UC-03 | FR-05 |
| UC-04 | FR-04, FR-09 |
| UC-05 | FR-06, FR-11 |
| UC-06 | FR-07, FR-08 |

---

*Dokumen ini disusun oleh tim Ecayci Lover untuk mata kuliah Application Project II.*
