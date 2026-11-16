"""
Konfigurasi Django Admin untuk Website PCM Gatak.
Admin Site Header & Title disesuaikan menjadi 'Admin Website PCM Gatak'.
"""

from django.contrib import admin
from .models import (
    ProfilOrganisasi,
    Pimpinan,
    Majelis,
    PengurusMajelis,
    Ranting,
    AmalUsaha,
    Berita,
    Agenda,
    Dokumen,
    PesanMasuk,
    TautanTerkait,
    SumberInformasi,
)


@admin.register(ProfilOrganisasi)
class ProfilOrganisasiAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nama_singkat', 'alamat_sekretariat', 'telepon', 'email')

    def has_add_permission(self, request):
        if ProfilOrganisasi.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Pimpinan)
class PimpinanAdmin(admin.ModelAdmin):
    list_display = ('urutan_tampil', 'nama', 'jabatan', 'periode')
    list_display_links = ('nama',)
    list_editable = ('urutan_tampil',)
    search_fields = ('nama', 'jabatan', 'periode')
    list_filter = ('periode',)
    ordering = ('urutan_tampil', 'nama')


class PengurusMajelisInline(admin.TabularInline):
    model = PengurusMajelis
    extra = 1
    fields = ('urutan', 'nama', 'jabatan')
    ordering = ('urutan',)


@admin.register(Majelis)
class MajelisAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'nama', 'periode', 'dasar_sk', 'jumlah_anggota')
    list_display_links = ('nama',)
    list_editable = ('urutan',)
    search_fields = ('nama', 'dasar_sk')
    inlines = [PengurusMajelisInline]
    ordering = ('urutan', 'nama')

    @admin.display(description="Jumlah Pengurus")
    def jumlah_anggota(self, obj):
        return obj.pengurus_list.count()


@admin.register(PengurusMajelis)
class PengurusMajelisAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'nama', 'jabatan', 'majelis')
    list_display_links = ('nama',)
    list_editable = ('urutan',)
    list_filter = ('majelis',)
    search_fields = ('nama', 'jabatan', 'majelis__nama')
    ordering = ('majelis', 'urutan')


@admin.register(Ranting)
class RantingAdmin(admin.ModelAdmin):
    list_display = ('nama_ranting', 'ketua', 'status_kepengurusan', 'alamat')
    list_filter = ('status_kepengurusan',)
    search_fields = ('nama_ranting', 'ketua', 'alamat')
    ordering = ('nama_ranting',)


@admin.register(AmalUsaha)
class AmalUsahaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'bidang', 'kategori_pendidikan', 'alamat')
    list_filter = ('bidang', 'kategori_pendidikan')
    search_fields = ('nama', 'deskripsi', 'alamat')
    ordering = ('bidang', 'kategori_pendidikan', 'nama')


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'status_terbit', 'kategori', 'sumber_nama', 'tanggal_terbit')
    list_filter = ('status_terbit', 'kategori', 'tanggal_terbit')
    search_fields = ('judul', 'ringkasan', 'isi', 'sumber_nama')
    prepopulated_fields = {'slug': ('judul',)}
    date_hierarchy = 'tanggal_terbit'
    ordering = ('-tanggal_terbit',)


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('nama_kegiatan', 'waktu_mulai', 'tempat', 'status_terlaksana')
    list_filter = ('waktu_mulai',)
    search_fields = ('nama_kegiatan', 'tempat', 'keterangan')
    ordering = ('waktu_mulai',)

    @admin.display(boolean=True, description='Sudah Terlaksana')
    def status_terlaksana(self, obj):
        return obj.sudah_terlaksana


@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal_unggah')
    search_fields = ('judul', 'keterangan')
    ordering = ('-tanggal_unggah',)


@admin.register(PesanMasuk)
class PesanMasukAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'subjek', 'waktu_kirim', 'sudah_dibaca')
    list_filter = ('sudah_dibaca', 'waktu_kirim')
    search_fields = ('nama', 'email', 'subjek', 'pesan')
    readonly_fields = ('nama', 'email', 'subjek', 'pesan', 'waktu_kirim')
    ordering = ('-waktu_kirim',)
    actions = ['tandai_sudah_dibaca']

    def has_add_permission(self, request):
        return False

    @admin.action(description='Tandai pesan yang dipilih sebagai sudah dibaca')
    def tandai_sudah_dibaca(self, request, queryset):
        queryset.update(sudah_dibaca=True)
        self.message_user(request, f"{queryset.count()} pesan berhasil ditandai sebagai sudah dibaca.")


@admin.register(TautanTerkait)
class TautanTerkaitAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'nama', 'url')
    list_display_links = ('nama',)
    list_editable = ('urutan',)
    search_fields = ('nama', 'url')
    ordering = ('urutan', 'nama')


@admin.register(SumberInformasi)
class SumberInformasiAdmin(admin.ModelAdmin):
    list_display = ('nama_sumber', 'jenis', 'tanggal_akses')
    list_filter = ('jenis', 'tanggal_akses')
    search_fields = ('nama_sumber', 'jenis_informasi', 'keterangan')
    ordering = ('jenis', 'nama_sumber')
