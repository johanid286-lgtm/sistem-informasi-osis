# Aplikasi Manajemen Kegiatan

## Deskripsi Aplikasi
Aplikasi Manajemen Kegiatan ini adalah aplikasi berbasis web yang memudahkan pengelolaan data kegiatan, mulai dari menambah, menampilkan, hingga menghapus kegiatan dengan mudah dan efisien. Aplikasi ini cocok digunakan untuk organisasi, sekolah, atau kelompok yang ingin mengatur kegiatan secara terstruktur.

## Cara Aplikasi Dibangun
Aplikasi dibangun menggunakan bahasa pemrograman Python dengan framework Flask sebagai backend. Database yang digunakan adalah SQLite, sebuah database file ringan dan mudah digunakan. Frontend menggunakan template HTML yang dirender oleh Flask untuk menampilkan data dan form input.

## Fitur-Fitur
- Menampilkan daftar kegiatan lengkap dengan detail nama, tanggal, dan deskripsi.
- Menambah kegiatan baru melalui form input yang mudah digunakan.
- Menghapus kegiatan dengan tombol hapus dan konfirmasi penghapusan untuk mencegah kesalahan.
- Navigasi yang sederhana dan user-friendly.

## Teknologi yang Digunakan
- Python 3.x
- Flask (Web framework)
- SQLite (Database ringan berbasis file)
- HTML (Template rendering)

## Struktur Proyek dan Penjelasan Isi File
```
/project_root
│
├── app.py                  # File utama aplikasi Flask yang berisi route dan logika backend
├── database.db             # File database SQLite untuk menyimpan data kegiatan
├── requirements.txt        # Daftar paket Python yang dibutuhkan (misal flask)
├── /templates              # Folder berisi file template HTML
│   └── manajemen_kegiatan.html  # Template halaman daftar kegiatan dengan tombol hapus
└── /static                 # Folder untuk file statis seperti CSS, JS, gambar (jika ada)
```

## Cara Instalasi dan Menjalankan Aplikasi
1. Pastikan Python 3 sudah terinstall di komputer Anda.
2. Clone atau download repository ini ke komputer Anda.
3. (Opsional) Buat virtual environment dan aktifkan:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```
4. Install dependencies yang diperlukan:
   ```bash
   pip install flask
   ```
5. Jalankan aplikasi Flask:
   ```bash
   flask run
   ```
6. Buka browser dan akses alamat berikut:
   ```
   http://localhost:5000/manajemen_kegiatan
   ```

## Tujuan Kedepan
- Menambahkan fitur edit kegiatan.
- Menambahkan autentikasi user untuk keamanan akses.
- Meningkatkan tampilan dengan CSS framework seperti Bootstrap.
- Migrasi ke database yang lebih kuat seperti PostgreSQL.
- Menyediakan REST API untuk integrasi dengan aplikasi lain.

## Cara Terhubung ke Web
Aplikasi berjalan sebagai server web Flask pada port 5000 secara default. Anda dapat mengaksesnya melalui browser dengan alamat `http://localhost:5000/manajemen_kegiatan`. Jika ingin diakses dari perangkat lain di jaringan yang sama, pastikan server berjalan pada IP yang bisa diakses dan port 5000 dibuka di firewall.

## Tujuan Aplikasi
Aplikasi ini bertujuan untuk memudahkan pengelolaan kegiatan secara terstruktur dan efisien, mengurangi penggunaan metode manual yang memakan waktu dan rentan kesalahan, serta membantu pengguna dalam memantau dan mengatur kegiatan dengan mudah dan cepat.
