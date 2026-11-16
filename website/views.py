"""
Views untuk seluruh halaman publik Website PCM Gatak.
Mata Kuliah: Pemrograman Web berbasis Framework (TIF1336)
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from .models import (
    ProfilOrganisasi,
    Pimpinan,
    Majelis,
    Ranting,
    AmalUsaha,
    Berita,
    Agenda,
    Dokumen,
    SumberInformasi,
)
from .forms import KontakForm


def beranda(request):
    """Halaman Beranda utama PCM Gatak."""
    profil = ProfilOrganisasi.objects.first()

    # Statistik Organisasi Terverifikasi
    jumlah_ranting = Ranting.objects.count()
    jumlah_amal_usaha = AmalUsaha.objects.count()
    jumlah_majelis = Majelis.objects.count()
    jumlah_anggota = profil.jumlah_anggota_ktam if profil and profil.jumlah_anggota_ktam else "Belum tersedia"

    # 3 Berita terbaru berstatus terbit
    berita_terbaru = Berita.objects.terbit()[:3]

    # 3 Agenda kegiatan terdekat
    now = timezone.now()
    agenda_mendatang = Agenda.objects.filter(waktu_mulai__gte=now).order_by('waktu_mulai')[:3]

    # Preview Amal Usaha
    amal_usaha_preview = AmalUsaha.objects.all()[:6]

    context = {
        'profil': profil,
        'jumlah_ranting': jumlah_ranting,
        'jumlah_amal_usaha': jumlah_amal_usaha,
        'jumlah_majelis': jumlah_majelis,
        'jumlah_anggota': jumlah_anggota,
        'berita_terbaru': berita_terbaru,
        'agenda_terbaru': agenda_mendatang,
        'amal_usaha_preview': amal_usaha_preview,
    }
    return render(request, 'website/beranda.html', context)


def profil(request):
    """Halaman Tentang, Sejarah, Latar Belakang PDM, Visi, dan Misi Organisasi."""
    profil_obj = ProfilOrganisasi.objects.first()
    context = {
        'profil': profil_obj,
    }
    return render(request, 'website/profil.html', context)


def pimpinan(request):
    """
    Halaman Susunan Pimpinan Cabang Muhammadiyah Gatak.
    Memuat Pimpinan Harian (Ketua & Sekretaris) dan 9 Majelis Pembantu Pimpinan (SK 16 Okt 2023).
    """
    pimpinan_harian = Pimpinan.objects.all().order_by('urutan_tampil')
    majelis_list = Majelis.objects.prefetch_related('pengurus_list').all().order_by('urutan')
    
    context = {
        'pimpinan_harian': pimpinan_harian,
        'majelis_list': majelis_list,
    }
    return render(request, 'website/pimpinan.html', context)


def ranting(request):
    """Halaman Tabel 14 Pimpinan Ranting Muhammadiyah (PRM) se-Kecamatan Gatak."""
    ranting_list = Ranting.objects.all().order_by('nama_ranting')
    context = {
        'ranting_list': ranting_list,
    }
    return render(request, 'website/ranting.html', context)


def amal_usaha(request):
    """
    Halaman Amal Usaha Muhammadiyah (AUM) 23 Unit Pendidikan
    Dikelompokkan berdasarkan: PAUD/TK, MIM, SMP, SMA, dan Boarding School (MBS).
    """
    paud_tk = AmalUsaha.objects.filter(kategori_pendidikan='paud_tk')
    mim = AmalUsaha.objects.filter(kategori_pendidikan='mim')
    smp = AmalUsaha.objects.filter(kategori_pendidikan='smp')
    sma = AmalUsaha.objects.filter(kategori_pendidikan='sma')
    boarding_school = AmalUsaha.objects.filter(kategori_pendidikan='boarding_school')
    total_aum = AmalUsaha.objects.count()

    context = {
        'paud_tk': paud_tk,
        'mim': mim,
        'smp': smp,
        'sma': sma,
        'boarding_school': boarding_school,
        'total_aum': total_aum,
    }
    return render(request, 'website/amal_usaha.html', context)


def berita_daftar(request):
    """Halaman Daftar Berita dengan Paginasi 6 artikel per halaman."""
    berita_qs = Berita.objects.terbit()
    paginator = Paginator(berita_qs, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'website/berita_daftar.html', context)


def berita_detail(request, slug):
    """
    Halaman Detail Berita.
    Berita draf atau berita bertanggal di masa depan otomatis menghasilkan 404.
    """
    berita_obj = get_object_or_404(Berita.objects.terbit(), slug=slug)
    berita_terkait = Berita.objects.terbit().exclude(pk=berita_obj.pk)[:3]

    context = {
        'berita': berita_obj,
        'berita_terkait': berita_terkait,
    }
    return render(request, 'website/berita_detail.html', context)


def agenda(request):
    """Halaman Agenda Kegiatan (dipisah antara yang akan datang dan yang sudah terlaksana)."""
    now = timezone.now()
    agenda_mendatang = Agenda.objects.filter(waktu_mulai__gte=now).order_by('waktu_mulai')
    agenda_terlaksana = Agenda.objects.filter(waktu_mulai__lt=now).order_by('-waktu_mulai')

    context = {
        'agenda_mendatang': agenda_mendatang,
        'agenda_terlaksana': agenda_terlaksana,
    }
    return render(request, 'website/agenda.html', context)


def unduhan(request):
    """Halaman Dokumen Publikasi dan Unduhan."""
    dokumen_list = Dokumen.objects.all().order_by('-tanggal_unggah')
    context = {
        'dokumen_list': dokumen_list,
    }
    return render(request, 'website/unduhan.html', context)


def kontak(request):
    """Halaman Kontak Sekretariat dan Formulir Pengiriman Pesan."""
    profil_obj = ProfilOrganisasi.objects.first()

    if request.method == 'POST':
        form = KontakForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Alhamdulillah, pesan Anda telah berhasil dikirimkan ke sekretariat PCM Gatak. Terima kasih!"
            )
            return redirect('website:kontak')
        else:
            messages.error(
                request,
                "Terdapat kesalahan pada formulir yang Anda kirimkan. Mohon periksa kembali isian Anda."
            )
    else:
        form = KontakForm()

    context = {
        'profil': profil_obj,
        'form': form,
    }
    return render(request, 'website/kontak.html', context)


def sumber_informasi(request):
    """Halaman Transparansi Data, Sumber Referensi, dan Atribusi."""
    sumber_internal = SumberInformasi.objects.filter(jenis='internal')
    sumber_publik = SumberInformasi.objects.filter(jenis='publik')

    context = {
        'sumber_internal': sumber_internal,
        'sumber_publik': sumber_publik,
    }
    return render(request, 'website/sumber_informasi.html', context)
