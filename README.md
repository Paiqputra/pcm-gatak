# Website Pimpinan Cabang Muhammadiyah (PCM) Gatak

Website profil, informasi dakwah, warta kegiatan, susunan pengurus majelis, daftar ranting, dan amal usaha pendidikan untuk **Pimpinan Cabang Muhammadiyah (PCM) Gatak**, Kecamatan Gatak, Kabupaten Sukoharjo, Jawa Tengah.

Proyek ini dibangun menggunakan **Django 6.x**, **Python 3.13**, dan package manager **uv** untuk memenuhi tugas mata kuliah **Pemrograman Web berbasis Framework (TIF1336)**, Program Studi Informatika, Fakultas Komunikasi dan Informatika, Universitas Muhammadiyah Surakarta.

---

## Identitas Kelompok & Mahasiswa

* **Mata Kuliah:** Pemrograman Web berbasis Framework (TIF1336)
* **Program Studi:** Informatika
* **Perguruan Tinggi:** Universitas Muhammadiyah Surakarta

### Tabel Pembagian Tugas & Kontribusi Anggota

---

## Identitas Organisasi

* **Nama Organisasi:** Pimpinan Cabang Muhammadiyah Gatak
* **Nama Singkat:** PCM Gatak
* **Wilayah:** Kecamatan Gatak, Kabupaten Sukoharjo, Jawa Tengah
* **Alamat Sekretariat:** Jogahan, Trangsan, Gatak, Sukoharjo, Jawa Tengah
* **Status Kepengurusan:** Periode Muktamar ke-48 (2022–2027)
  * **Ketua:** Drs. H. Rombe Mustajab, M.Hum.
  * **Sekretaris:** Drs. Shodiq Purnomo, M.M.

---

## Teknologi yang Digunakan

* **Bahasa & Framework:** Python 3.13, Django 6.1
* **Package Manager:** [uv](https://docs.astral.sh/uv/) (menggunakan `pyproject.toml` dan `uv.lock`)
* **Frontend:** Django Templates (Server-Side Rendering), Bootstrap 5, Bootstrap Icons, Custom CSS
* **Database:** SQLite (Development lokal) & PostgreSQL 17 (Docker & Production)
* **Web Server & Statics:** Gunicorn & WhiteNoise
* **Containerization:** Docker & Docker Compose (Multi-stage build, non-root user)

---

## Struktur Folder Proyek

```text
pcm-gatak/
├── config/                  # Pengaturan utama project Django (settings, urls, wsgi, asgi)
├── website/                 # Aplikasi utama website
│   ├── management/
│   │   └── commands/
│   │       └── seed_pcm.py  # Management command seeder data riil
│   ├── migrations/          # File migrasi database
│   ├── forms.py             # ModelForm untuk kontak & validasi
│   ├── models.py            # 9 Model data utama + Majelis & SumberInformasi
│   ├── tests.py             # Automated unit tests
│   ├── urls.py              # URL routing app dengan namespace 'website'
│   └── views.py             # View controllers & paginasi
├── templates/               # Template Django HTML (SSR)
│   ├── base.html            # Base template induk (header, navbar, footer)
│   ├── 404.html             # Halaman error 404 custom
│   └── website/             # Template setiap halaman publik
├── static/                  # Aset statis (CSS, JS, logo PCM)
│   ├── css/style.css
│   └── img/logo-pcm.png
├── media/                   # Direktori berkas & foto upload
├── .env.example             # Contoh environment variable
├── Dockerfile               # Konfigurasi container Docker
├── compose.yaml             # Docker Compose (service web & PostgreSQL 17)
├── pyproject.toml           # Definisi dependensi uv
├── uv.lock                  # Lockfile uv
└── README.md
```

---

## Fitur & Halaman Website

1. **Beranda (`/`):** Hero banner, kartu statistik riil (14 Ranting PRM, 23 Unit AUM Pendidikan, 9 Majelis), warta terkini, agenda terdekat, preview AUM.
2. **Profil (`/profil/`):** Latar belakang historis Muhammadiyah di Sukoharjo (sumber PDM), transparansi sejarah khusus, visi & misi.
3. **Pimpinan (`/pimpinan/`):** Pimpinan harian (Ketua & Sekretaris periode 2022–2027) serta susunan 9 Majelis pembantu pimpinan berdasarkan SK resmi bertanggal 16 Oktober 2023.
4. **Ranting (`/ranting/`):** Daftar 14 Pimpinan Ranting Muhammadiyah (PRM) se-Kecamatan Gatak dalam tabel responsif dan kartu mobile. Nomor kontak pribadi pengurus disembunyikan demi privasi.
5. **Amal Usaha (`/amal-usaha/`):** 23 unit AUM pendidikan dikelompokkan dalam 5 kategori: PAUD/TK (12 unit), MIM (6 unit), SMP (2 unit), Pesantren MBS (2 unit), dan SMA (1 unit).
6. **Berita (`/berita/` & `/berita/<slug>/`):** Warta kegiatan terverifikasi dengan **fitur pencarian kata kunci terpadu** (`/berita/?q=...`), paginasi 6 artikel per halaman, detail berita, dan tautan artikel asli. Berita draf atau bertanggal masa depan otomatis merespons HTTP 404.
7. **Agenda (`/agenda/`):** Jadwal kegiatan yang dipisahkan antara agenda mendatang dan agenda yang telah terlaksana.
8. **Unduhan (`/unduhan/`):** Pusat unduh berkas publikasi dan dokumen resmi.
9. **Kontak (`/kontak/`):** Alamat sekretariat resmi dan formulir pesan masyarakat tersimpan ke database dengan notifikasi Django Messages.
10. **Sumber Informasi (`/sumber-informasi/`):** Halaman transparansi yang merinci seluruh dokumen internal dan tautan website publik yang digunakan beserta tanggal akses.
11. **Dashboard Admin (`/admin/`):** Panel "Admin Website PCM Gatak" dengan aturan singleton pada profil dan readonly pada pesan masuk.
12. **Otomatisasi CI/CD:** GitHub Actions workflow yang otomatis menjalankan seluruh unit test pada setiap `git push` ke repositori.

---

## Panduan Menjalankan di Lokal (Development)

### 1. Prasyarat
* Python 3.12+ (disarankan Python 3.13)
* Package manager `uv` ([Instalasi uv](https://docs.astral.sh/uv/getting-started/installation/))

### 2. Langkah Instalasi

```bash
# Clone repository
git clone https://github.com/Paiqputra/pcm-gatak.git
cd pcm-gatak

# Sinkronisasi dependensi virtual environment dengan uv
uv sync

# Salin konfigurasi environment variable
copy .env.example .env

# Jalankan migrasi database
uv run python manage.py migrate

# Isi database dengan data riil PCM Gatak
uv run python manage.py seed_pcm

# Jalankan server development
uv run python manage.py runserver
```

Akses website di browser: **`http://127.0.0.1:8000/`**

### 3. Menjalankan Automated Unit Tests

```bash
uv run python manage.py test
```

---

## Menjalankan dengan Docker & PostgreSQL

Pastikan Docker Desktop sudah aktif di perangkat Anda:

```bash
# Build dan jalankan container web + database PostgreSQL 17
docker compose up --build

# Buka tab terminal baru untuk menjalankan seeder data
docker compose exec web uv run python manage.py seed_pcm
```

Aplikasi dapat diakses langsung pada: **`http://localhost:8000/`**

---

## Transparansi Sumber Data & Tanggal Akses

Seluruh data dihimpun secara etis tanpa mengarang informasi:

| No | Nama Dokumen / Sumber | Jenis Sumber | Informasi yang Digunakan | Tanggal Akses |
|---|---|---|---|---|
| 1 | `1-SK PIMPINAN CABANG MAJELIS.docx` | Dokumen Internal | Susunan pengurus 9 Majelis Pembantu Pimpinan (SK 16 Oktober 2023) | 16 November 2026 |
| 2 | `KETUA PRM SE GATAK.docx` | Dokumen Internal | Daftar 14 Pimpinan Ranting Muhammadiyah (PRM) se-Kecamatan Gatak | 16 November 2026 |
| 3 | `Amal usaha yang dimiliki.docx` | Dokumen Internal | Inventarisasi 23 unit AUM bidang pendidikan (PAUD/TK, MIM, SMP, MBS, SMA) | 16 November 2026 |
| 4 | `alamat PCM.docx` | Dokumen Internal | Alamat sekretariat resmi di Jogahan, Trangsan, Gatak, Sukoharjo | 16 November 2026 |
| 5 | `SK Pendirian PCM Gatak.pdf` | Dokumen Internal | Legalitas pendirian cabang | 16 November 2026 |
| 6 | [PDM Sukoharjo](https://pdmsukoharjo.or.id/tentang-kami/) | Website Resmi | Latar belakang sejarah Muhammadiyah di Sukoharjo & status cabang perintis | 16 November 2026 |
| 7 | [LPCR PP Muhammadiyah](https://lpcr.or.id/sinergi-dakwah-pcm-dan-pca-gatak-menggembirakan-dan-mencerahkan-umat/) | Website Resmi | Warta pengajian rutin Ahad pagi PCM & PCA di MBS Gatak | 16 November 2026 |
| 8 | [Berita UAD](https://news.uad.ac.id/pcm-gatak-sukoharjo-kunjungi-uad-perkuat-nilai-islam-dan-kemuhammadiyahan/) | Media Kampus | Pembinaan 160 guru dan karyawan sekolah Muhammadiyah PCM Gatak di UAD | 16 November 2026 |
| 9 | [Muhammadiyah Solo](https://muhammadiyahsolo.com/20261013/ums-hadirkan-pakar-bangladesh-dalam-pelatihan-herbal-di-gatak-17839) | Media Berita | Pelatihan herbal PCA Gatak bersama UMS dan kehadiran pengurus PCM Gatak | 16 November 2026 |

---

## Atribusi & Hak Cipta
* **Logo Resmi Muhammadiyah:** Pimpinan Cabang Muhammadiyah.
* **Lisensi Atribusi:** Lisensi CC BY-SA 4.0 sesuai ketentuan penggunaan publik persyarikatan.
* **Keterangan Tugas:** *"Website ini dibuat untuk tugas kuliah Pemrograman Web berbasis Framework (TIF1336), bukan website resmi PCM Gatak."*
