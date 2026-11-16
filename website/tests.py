"""
Automated unit tests untuk website PCM Gatak.
Mata Kuliah: Pemrograman Web berbasis Framework (TIF1336)
"""

from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import (
    ProfilOrganisasi,
    Pimpinan,
    Ranting,
    AmalUsaha,
    Berita,
    Agenda,
    Dokumen,
    PesanMasuk,
    TautanTerkait,
)


class PCMWebsiteTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Buat profil organisasi
        self.profil = ProfilOrganisasi.objects.create(
            nama="Pimpinan Cabang Muhammadiyah Gatak",
            nama_singkat="PCM Gatak",
            tagline="Membangun Umat, Menguatkan Persyarikatan",
            tentang="Tentang PCM Gatak...",
            sejarah="Sejarah PCM Gatak...",
            visi="Visi PCM Gatak...",
            misi="Misi 1\nMisi 2\nMisi 3",
            alamat_sekretariat="Gatak, Sukoharjo",
            telepon="Belum tersedia",
            email="pcmgatak@example.com",
            jumlah_anggota_ktam="Belum tersedia"
        )

        # Buat berita terbit
        self.berita_terbit = Berita.objects.create(
            judul="Berita Terbit PCM Gatak",
            ringkasan="Ringkasan berita terbit.",
            isi="Isi lengkap berita yang sudah dipublikasikan.",
            status_terbit="terbit",
            tanggal_terbit=timezone.now() - timedelta(days=1),
        )

        # Buat berita draf
        self.berita_draf = Berita.objects.create(
            judul="Berita Draf Rahasia",
            ringkasan="Ringkasan berita draf.",
            isi="Isi berita draf yang belum boleh tayang.",
            status_terbit="draf",
            tanggal_terbit=timezone.now(),
        )

        # Buat berita terjadwal di masa depan (belum boleh tayang)
        self.berita_masa_depan = Berita.objects.create(
            judul="Berita Terbit Masa Depan",
            ringkasan="Ringkasan.",
            isi="Isi masa depan.",
            status_terbit="terbit",
            tanggal_terbit=timezone.now() + timedelta(days=5),
        )

        # Buat ranting, pimpinan, amal usaha, agenda, tautan
        self.pimpinan = Pimpinan.objects.create(
            nama="Drs. H. Shodiq",
            jabatan="Ketua PCM Gatak",
            periode="2022–2027",
            urutan_tampil=1
        )
        self.ranting = Ranting.objects.create(
            nama_ranting="PRM Trangsan",
            ketua="Belum tersedia",
            alamat="Trangsan, Gatak"
        )
        self.aum = AmalUsaha.objects.create(
            nama="MI Muhammadiyah Trangsan",
            bidang="pendidikan",
            deskripsi="Sekolah dasar unggulan",
            alamat="Trangsan"
        )
        self.agenda = Agenda.objects.create(
            nama_kegiatan="Pengajian Rutin Ahad Pagi",
            waktu_mulai=timezone.now() + timedelta(days=2),
            tempat="Masjid Gatak"
        )
        self.tautan = TautanTerkait.objects.create(
            nama="PP Muhammadiyah",
            url="https://muhammadiyah.or.id",
            urutan=1
        )

    # ------------------------------------------------------------------------
    # Test 1: Semua halaman publik merespons HTTP 200
    # ------------------------------------------------------------------------
    def test_semua_halaman_publik_status_200(self):
        urls = [
            reverse('website:beranda'),
            reverse('website:profil'),
            reverse('website:pimpinan'),
            reverse('website:ranting'),
            reverse('website:amal_usaha'),
            reverse('website:berita_daftar'),
            reverse('website:agenda'),
            reverse('website:unduhan'),
            reverse('website:kontak'),
            reverse('website:sumber_informasi'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f"URL {url} harus merespons status HTTP 200, namun didapatkan {response.status_code}"
            )

    # ------------------------------------------------------------------------
    # Test 2: Detail berita terbit dapat diakses (HTTP 200)
    # ------------------------------------------------------------------------
    def test_detail_berita_terbit_dapat_diakses(self):
        url = reverse('website:berita_detail', kwargs={'slug': self.berita_terbit.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.berita_terbit.judul)

    # ------------------------------------------------------------------------
    # Test 3: Berita draf dan berita masa depan harus menghasilkan HTTP 404
    # ------------------------------------------------------------------------
    def test_berita_draf_dan_masa_depan_menghasilkan_404(self):
        # Berita draf -> 404
        url_draf = reverse('website:berita_detail', kwargs={'slug': self.berita_draf.slug})
        response_draf = self.client.get(url_draf)
        self.assertEqual(response_draf.status_code, 404)

        # Berita masa depan -> 404
        url_future = reverse('website:berita_detail', kwargs={'slug': self.berita_masa_depan.slug})
        response_future = self.client.get(url_future)
        self.assertEqual(response_future.status_code, 404)

    # ------------------------------------------------------------------------
    # Test 4: Form kontak menyimpan pesan ke database & menampilkan notifikasi
    # ------------------------------------------------------------------------
    def test_form_kontak_menyimpan_pesan(self):
        url = reverse('website:kontak')
        data = {
            'nama': "Ahmad Dahlan",
            'email': "ahmad@example.com",
            'subjek': "Pertanyaan Amal Usaha",
            'pesan': "Bagaimana cara mendaftar santri baru di madrasah Muhammadiyah?",
        }
        pesan_awal = PesanMasuk.objects.count()
        response = self.client.post(url, data, follow=True)

        # Harus redirect ke kontak dan status 200
        self.assertEqual(response.status_code, 200)
        # Jumlah pesan masuk bertambah 1
        self.assertEqual(PesanMasuk.objects.count(), pesan_awal + 1)
        # Verifikasi data tersimpan
        pesan_terbaru = PesanMasuk.objects.latest('waktu_kirim')
        self.assertEqual(pesan_terbaru.nama, "Ahmad Dahlan")
        self.assertEqual(pesan_terbaru.email, "ahmad@example.com")
        self.assertFalse(pesan_terbaru.sudah_dibaca)

    # ------------------------------------------------------------------------
    # Test 5: Profil organisasi hanya boleh memiliki satu record (Singleton)
    # ------------------------------------------------------------------------
    def test_profil_organisasi_singleton_dan_tidak_bisa_dihapus(self):
        # Mencegah pembuatan record kedua
        dengan_record_kedua = ProfilOrganisasi(
            nama="PCM Duplikat",
            nama_singkat="PCM Duplikat",
            tagline="Tagline",
            tentang="Tentang",
            sejarah="Sejarah",
            visi="Visi",
            misi="Misi",
            alamat_sekretariat="Alamat",
        )
        with self.assertRaises(ValidationError):
            dengan_record_kedua.save()

        # Mencegah penghapusan profil
        with self.assertRaises(ValidationError):
            self.profil.delete()

    # ------------------------------------------------------------------------
    # Test 6: Custom Manager Berita hanya menampilkan berita terbit di masa lalu
    # ------------------------------------------------------------------------
    def test_custom_manager_berita_terbit(self):
        qs = Berita.objects.terbit()
        self.assertIn(self.berita_terbit, qs)
        self.assertNotIn(self.berita_draf, qs)
        self.assertNotIn(self.berita_masa_depan, qs)

    # ------------------------------------------------------------------------
    # Test 7: Pembuatan slug otomatis dan tetap unik jika judul sama
    # ------------------------------------------------------------------------
    def test_slug_unik_otomatis(self):
        berita_kembar_1 = Berita.objects.create(
            judul="Kegiatan Tabligh Akbar Gatak",
            ringkasan="Ringkasan 1",
            isi="Isi 1",
            status_terbit="terbit"
        )
        berita_kembar_2 = Berita.objects.create(
            judul="Kegiatan Tabligh Akbar Gatak",
            ringkasan="Ringkasan 2",
            isi="Isi 2",
            status_terbit="terbit"
        )
        self.assertNotEqual(berita_kembar_1.slug, berita_kembar_2.slug)
        self.assertTrue(berita_kembar_2.slug.startswith("kegiatan-tabligh-akbar-gatak"))
