"""Context processor untuk menyediakan Profil Organisasi dan Tautan Terkait ke seluruh template."""

def pcm_context(request):
    """Menyediakan data profil PCM dan tautan persyarikatan secara global."""
    try:
        from website.models import ProfilOrganisasi, TautanTerkait
        profil = ProfilOrganisasi.objects.first()
        tautan_terkait = TautanTerkait.objects.all().order_by('urutan')
    except Exception:
        profil = None
        tautan_terkait = []

    return {
        'profil_organisasi': profil,
        'tautan_persyarikatan': tautan_terkait,
    }
