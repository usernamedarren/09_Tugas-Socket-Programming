# Aplikasi Ruang Obrolan Pribadi

Proyek ini adalah aplikasi ruang obrolan berbasis UDP, memungkinkan pengguna untuk terhubung ke server, bertukar pesan, dan mempertahankan riwayat obrolan. Pesan ditampilkan dalam antarmuka ruang obrolan dan pesan yang telah dikirim disimpan untuk sesi berikutnya.

## Fitur

- **Koneksi Server-Klien**: Server UDP mengelola beberapa klien, memungkinkan banyak klien untuk bergabung dengan ruang obrolan menggunakan autentikasi IP dan kata sandi.
- **Perlindungan Kata Sandi**: Klien harus memasukkan kata sandi yang benar untuk bergabung dengan ruang obrolan.
- **Nama Pengguna Unik**: Setiap klien memasukkan nama pengguna unik yang diverifikasi oleh server.
- **Riwayat Obrolan**: Riwayat obrolan disimpan dalam `archive.csv` dan muncul kembali saat pengguna bergabung kembali ke ruang obrolan yang sama.

## Struktur Proyek
client.py (Program untuk klien terhubung ke ruang obrolan)
server.py (Program untuk memulai server dan mengelola klien)
storage.py (Mengelola penyimpanan riwayat obrolan)
archive.csv (Menyimpan riwayat obrolan ruang)

## Repository
https://github.com/usernamedarren/Socket-Programming

## Cara Penggunaan
**Langkah 1 : Memulai Server**
- Jalankan program server dengan ketikkan syntax berikut di terminal:
    python server.py
- Sebuah jendela GUI akan terbuka. Masukkan:
    - Alamat IP: Alamat IP server.
    - Port: Port untuk menghubungkan (misalnya, 8080).
    - Kata Sandi: Kata sandi yang harus dimasukkan klien untuk masuk ke ruang obrolan.
    - Klik Start Server untuk mulai menerima klien yang ingin terhubung.

**Langkah 2: Memulai Klien**
- Jalankan program klien dengan ketikkan syntax berikut di terminal:
    python client.py
- Beberapa jendela prompt akan memandu Anda untuk memasukkan:
    - IP Server: Masukkan alamat IP server.
    - Port Server: Masukkan port server yang sedang terhubung (misalnya, 8080).
    - Kata Sandi: Masukkan kata sandi server.
    - Nama Pengguna: Masukkan nama pengguna yang unik.
    - Setelah terhubung, akan ditampilkan riwayat obrolan bila ada dan memungkinkan Anda untuk mengirim pesan dengan mengetik di kolom input dan menekan tombol Kirim atau Enter.

**Keluar dari Obrolan**
-  Untuk keluar dari obrolan, ketik exit di kolom pesan dan kirim. Ini akan memutuskan koneksi klien dari server.

## Pemecahan Masalah
- Server Tidak Bisa Dimulai: Pastikan IP dan port tersedia dan valid. Alamat IP bisa diatur ke 0.0.0.0 untuk terhubung pada semua antarmuka yang tersedia.
- Masalah Kata Sandi: Pastikan kata sandi yang dimasukkan klien sesuai dengan kata sandi server.
- Masalah Jaringan: Pastikan server dan klien berada di jaringan yang sama atau gunakan VPN untuk pengujian lokal.
- File CSV Tidak Ditemukan: archive.csv akan dibuat secara otomatis saat pesan pertama kali disimpan.