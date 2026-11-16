"""Model data untuk website Pimpinan Cabang Muhammadiyah (PCM) Gatak."""

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class ProfilOrganisasi(models.Model):
    """
    Model Profil Organisasi (Singleton Pattern).
    Hanya boleh ada 1 record dan tidak boleh dihapus.
    """
    nama = models.CharField(
        max_length=200,
        default="Pimpinan Cabang Muhammadiyah Gatak",
        verbose_name="Nama Organisasi"
    )
    nama_singkat = models.CharField(
        max_length=50,
        default="PCM Gatak",
        verbose_name="Nama Singkat"
    )
    tagline = models.CharField(
        max_length=255,
        default="Membangun Umat, Menguatkan Persyarikatan",
        verbose_name="Tagline",
        help_text="Tagline desain website, bukan visi resmi organisasi."
    )
    tentang = models.TextField(verbose_name="Tentang PCM Gatak")
    sejarah = models.TextField(verbose_name="Sejarah & Latar Belakang")
    sejarah_khusus = models.TextField(
        default="Informasi sejarah khusus PCM Gatak belum tersedia.",
        verbose_name="Sejarah Khusus PCM Gatak"
    )
    visi = models.TextField(
        default="Belum tersedia data resmi",
        verbose_name="Visi"
    )
    misi = models.TextField(
        default="Belum tersedia data resmi",
        verbose_name="Misi",
        help_text="Tuliskan butir-butir misi. Pisahkan setiap misi dengan baris baru (Enter)."
    )
    alamat_sekretariat = models.TextField(
        default="Jogahan, Trangsan, Gatak, Sukoharjo",
        verbose_name="Alamat Sekretariat"
    )
    telepon = models.CharField(
        max_length=50,
        blank=True,
        default="Informasi belum tersedia",
        verbose_name="Telepon Resmi"
    )
    email = models.CharField(
        max_length=100,
        blank=True,
        default="Informasi belum tersedia",
        verbose_name="Email Resmi"
    )
    jumlah_anggota_ktam = models.CharField(
        max_length=50,
        default="Belum tersedia",
        verbose_name="Jumlah Anggota ber-KTAM",
        help_text="Tulis 'Belum tersedia' jika data belum terverifikasi"
    )
    gambar_utama = models.ImageField(
        upload_to="profil/",
        blank=True,
        null=True,
        verbose_name="Gambar Utama / Hero Banner"
    )

    class Meta:
        verbose_name = "Profil Organisasi"
        verbose_name_plural = "Profil Organisasi"

    def clean(self):
        # Mencegah pembuatan lebih dari 1 record profil
        if not self.pk and ProfilOrganisasi.objects.exists():
            raise ValidationError("Hanya diperbolehkan ada satu record Profil Organisasi.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Mencegah penghapusan record profil
        raise ValidationError("Profil organisasi tidak boleh dihapus.")

    def misi_list(self):
        """Mengembalikan daftar butir misi yang dipisahkan baris baru."""
        if not self.misi or self.misi.strip() == "Belum tersedia data resmi":
            return []
        return [m.strip() for m in self.misi.splitlines() if m.strip()]

    def __str__(self):
        return self.nama


class Pimpinan(models.Model):
    """Model pimpinan harian (Ketua & Sekretaris) PCM Gatak periode 2022–2027."""
    nama = models.CharField(max_length=150, verbose_name="Nama Lengkap")
    jabatan = models.CharField(max_length=100, verbose_name="Jabatan")
    periode = models.CharField(
        max_length=50,
        default="Muktamar ke-48 (2022–2027)",
        verbose_name="Periode"
    )
    keterangan_sumber = models.CharField(
        max_length=200,
        default="Dokumen Internal SK Muktamar ke-48 (2022–2027)",
        verbose_name="Keterangan Sumber"
    )
    foto = models.ImageField(upload_to="pimpinan/", blank=True, null=True, verbose_name="Foto")
    urutan_tampil = models.PositiveIntegerField(default=1, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "Pimpinan Harian"
        verbose_name_plural = "Pimpinan Harian"
        ordering = ['urutan_tampil', 'nama']

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"


class Majelis(models.Model):
    """Model 9 Majelis Pembantu Pimpinan PCM Gatak berdasarkan SK 16 Oktober 2023."""
    nama = models.CharField(max_length=150, verbose_name="Nama Majelis")
    periode = models.CharField(max_length=50, default="2022–2027", verbose_name="Periode")
    dasar_sk = models.CharField(
        max_length=255,
        default="SK Pimpinan Cabang Muhammadiyah Gatak No. 1 bertanggal 16 Oktober 2023",
        verbose_name="Dasar SK"
    )
    urutan = models.PositiveIntegerField(default=1, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "Majelis"
        verbose_name_plural = "Daftar 9 Majelis"
        ordering = ['urutan', 'nama']

    def __str__(self):
        return self.nama


class PengurusMajelis(models.Model):
    """Model pengurus dalam majelis PCM Gatak."""
    majelis = models.ForeignKey(
        Majelis,
        on_delete=models.CASCADE,
        related_name='pengurus_list',
        verbose_name="Majelis"
    )
    nama = models.CharField(max_length=150, verbose_name="Nama Lengkap")
    jabatan = models.CharField(max_length=100, verbose_name="Jabatan dalam Majelis")
    urutan = models.PositiveIntegerField(default=1, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "Pengurus Majelis"
        verbose_name_plural = "Pengurus Majelis"
        ordering = ['urutan', 'nama']

    def __str__(self):
        return f"{self.nama} ({self.jabatan}) - {self.majelis.nama}"


class Ranting(models.Model):
    """Model 14 Pimpinan Ranting Muhammadiyah (PRM) di wilayah Gatak."""
    nama_ranting = models.CharField(max_length=100, verbose_name="Nama Ranting")
    ketua = models.CharField(
        max_length=150,
        blank=True,
        default="Belum ada kepengurusan",
        verbose_name="Ketua Ranting"
    )
    status_kepengurusan = models.CharField(
        max_length=100,
        default="Ada Kepengurusan",
        verbose_name="Status Kepengurusan"
    )
    alamat = models.TextField(
        blank=True,
        default="Kecamatan Gatak, Kabupaten Sukoharjo",
        verbose_name="Wilayah / Desa"
    )
    telepon = models.CharField(
        max_length=50,
        blank=True,
        default="Informasi belum tersedia",
        verbose_name="Kontak Resmi"
    )

    class Meta:
        verbose_name = "Ranting"
        verbose_name_plural = "Daftar 14 Ranting"
        ordering = ['nama_ranting']

    def __str__(self):
        return self.nama_ranting


class AmalUsaha(models.Model):
    """Model Amal Usaha Muhammadiyah (AUM) se-Cabang Gatak."""
    BIDANG_CHOICES = [
        ('pendidikan', 'Pendidikan'),
        ('kesehatan', 'Kesehatan'),
        ('sosial', 'Sosial'),
        ('ekonomi', 'Ekonomi'),
    ]

    KATEGORI_PENDIDIKAN_CHOICES = [
        ('paud_tk', 'PAUD & TK'),
        ('mim', 'Madrasah Ibtidaiyah'),
        ('smp', 'SMP Muhammadiyah'),
        ('sma', 'SMA Muhammadiyah'),
        ('boarding_school', 'Muhammadiyah Boarding School'),
        ('lainnya', 'Lainnya'),
    ]

    nama = models.CharField(max_length=200, verbose_name="Nama Amal Usaha")
    bidang = models.CharField(max_length=20, choices=BIDANG_CHOICES, default='pendidikan', verbose_name="Bidang")
    kategori_pendidikan = models.CharField(
        max_length=30,
        choices=KATEGORI_PENDIDIKAN_CHOICES,
        default='lainnya',
        verbose_name="Kategori AUM Pendidikan"
    )
    deskripsi = models.TextField(blank=True, default="Informasi belum tersedia", verbose_name="Deskripsi")
    alamat = models.TextField(blank=True, default="Informasi belum tersedia", verbose_name="Alamat")
    gambar = models.ImageField(upload_to="amal_usaha/", blank=True, null=True, verbose_name="Foto / Gambar")

    class Meta:
        verbose_name = "Amal Usaha"
        verbose_name_plural = "Amal Usaha (AUM)"
        ordering = ['bidang', 'kategori_pendidikan', 'nama']

    def __str__(self):
        return f"{self.nama} ({self.get_kategori_pendidikan_display() if self.kategori_pendidikan != 'lainnya' else self.get_bidang_display()})"


class BeritaQuerySet(models.QuerySet):
    """QuerySet custom untuk berita."""
    def terbit(self):
        return self.filter(
            status_terbit='terbit',
            tanggal_terbit__lte=timezone.now()
        )


class BeritaManager(models.Manager):
    """Custom Manager untuk berita terbit."""
    def get_queryset(self):
        return BeritaQuerySet(self.model, using=self._db)

    def terbit(self):
        return self.get_queryset().terbit()


class Berita(models.Model):
    """Model Berita dan Artikel kegiatan PCM Gatak."""
    STATUS_CHOICES = [
        ('draf', 'Draf'),
        ('terbit', 'Terbit'),
    ]

    judul = models.CharField(max_length=250, verbose_name="Judul Berita")
    slug = models.SlugField(max_length=280, unique=True, blank=True, verbose_name="Slug URL")
    ringkasan = models.TextField(max_length=500, verbose_name="Ringkasan")
    isi = models.TextField(verbose_name="Isi Berita")
    gambar_sampul = models.ImageField(upload_to="berita/", blank=True, null=True, verbose_name="Gambar Sampul")
    tanggal_terbit = models.DateTimeField(default=timezone.now, verbose_name="Tanggal Terbit")
    status_terbit = models.CharField(max_length=10, choices=STATUS_CHOICES, default='terbit', verbose_name="Status")
    
    # Metadata Sumber Berita Internet
    sumber_nama = models.CharField(max_length=150, blank=True, verbose_name="Nama Sumber Berita")
    sumber_url = models.URLField(blank=True, verbose_name="Tautan Sumber Asli")
    kategori = models.CharField(max_length=100, blank=True, default="Kegiatan", verbose_name="Kategori Berita")
    catatan_redaksi = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Catatan Redaksi / Penyelenggara (mis. Kegiatan PCA)",
        help_text="Tandai dengan jelas jika diselenggarakan oleh Ortom seperti PCA."
    )

    objects = BeritaManager()

    class Meta:
        verbose_name = "Berita"
        verbose_name_plural = "Daftar Berita"
        ordering = ['-tanggal_terbit']

    def save(self, *args, **kwargs):
        # Otomatis buat slug yang unik
        if not self.slug:
            base_slug = slugify(self.judul) or "berita"
            slug = base_slug
            counter = 1
            while Berita.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul


class Agenda(models.Model):
    """Model Agenda kegiatan PCM Gatak."""
    nama_kegiatan = models.CharField(max_length=200, verbose_name="Nama Kegiatan")
    waktu_mulai = models.DateTimeField(verbose_name="Waktu Mulai")
    tempat = models.CharField(max_length=200, verbose_name="Tempat")
    keterangan = models.TextField(blank=True, verbose_name="Keterangan")

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agenda Kegiatan"
        ordering = ['waktu_mulai']

    @property
    def sudah_terlaksana(self):
        return self.waktu_mulai < timezone.now()

    def __str__(self):
        return f"{self.nama_kegiatan} - {self.waktu_mulai.strftime('%d/%m/%Y')}"


class Dokumen(models.Model):
    """Model Dokumen & Berkas Publikasi Organisasi."""
    judul = models.CharField(max_length=200, verbose_name="Judul Dokumen")
    keterangan = models.TextField(blank=True, verbose_name="Keterangan")
    berkas = models.FileField(upload_to="dokumen/", verbose_name="Berkas (PDF, dsb.)")
    tanggal_unggah = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Unggah")

    class Meta:
        verbose_name = "Dokumen"
        verbose_name_plural = "Dokumen & Unduhan"
        ordering = ['-tanggal_unggah']

    def __str__(self):
        return self.judul


class PesanMasuk(models.Model):
    """Model formulir kontak / aspirasi masyarakat."""
    nama = models.CharField(max_length=150, verbose_name="Nama Pengirim")
    email = models.EmailField(verbose_name="Email")
    subjek = models.CharField(max_length=200, verbose_name="Subjek")
    pesan = models.TextField(verbose_name="Isi Pesan")
    waktu_kirim = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Kirim")
    sudah_dibaca = models.BooleanField(default=False, verbose_name="Sudah Dibaca")

    class Meta:
        verbose_name = "Pesan Masuk"
        verbose_name_plural = "Pesan Masuk"
        ordering = ['-waktu_kirim']

    def __str__(self):
        return f"Pesan dari {self.nama} ({self.subjek})"


class TautanTerkait(models.Model):
    """Model Tautan Persyarikatan (PP, PWM, PDM, Aisyiyah, dsb.)."""
    nama = models.CharField(max_length=150, verbose_name="Nama Organisasi / Lembaga")
    url = models.URLField(verbose_name="URL Website")
    urutan = models.PositiveIntegerField(default=1, verbose_name="Urutan")

    class Meta:
        verbose_name = "Tautan Terkait"
        verbose_name_plural = "Tautan Persyarikatan"
        ordering = ['urutan', 'nama']

    def __str__(self):
        return self.nama


class SumberInformasi(models.Model):
    """Model transparansi data dan sumber verifikasi informasi website PCM Gatak."""
    JENIS_CHOICES = [
        ('internal', 'Dokumen Internal PCM Gatak'),
        ('publik', 'Website / Media Publik'),
    ]

    nama_sumber = models.CharField(max_length=200, verbose_name="Nama Sumber / Dokumen")
    url_sumber = models.URLField(blank=True, verbose_name="URL Sumber (jika website)")
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='publik', verbose_name="Jenis Sumber")
    jenis_informasi = models.TextField(verbose_name="Data / Informasi yang Digunakan")
    tanggal_akses = models.DateField(default=timezone.now, verbose_name="Tanggal Pengambilan Data")
    keterangan = models.TextField(blank=True, verbose_name="Keterangan & Catatan Verifikasi")

    class Meta:
        verbose_name = "Sumber Informasi"
        verbose_name_plural = "Daftar Sumber Informasi"
        ordering = ['jenis', 'nama_sumber']

    def __str__(self):
        return f"[{self.get_jenis_display()}] {self.nama_sumber}"
