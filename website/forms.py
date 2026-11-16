"""Formulir untuk aplikasi website PCM Gatak."""

from django import forms
from .models import PesanMasuk


class KontakForm(forms.ModelForm):
    """ModelForm untuk formulir aspirasi dan kontak masyarakat."""

    class Meta:
        model = PesanMasuk
        fields = ['nama', 'email', 'subjek', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama lengkap Anda',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'nama@contoh.com',
                'required': True,
            }),
            'subjek': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Topik atau subjek pesan',
                'required': True,
            }),
            'pesan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tuliskan pesan, saran, atau pertanyaan Anda di sini...',
                'required': True,
            }),
        }
        labels = {
            'nama': 'Nama Lengkap',
            'email': 'Alamat Email',
            'subjek': 'Subjek Pesan',
            'pesan': 'Isi Pesan',
        }

    def clean_pesan(self):
        pesan = self.cleaned_data.get('pesan', '').strip()
        if len(pesan) < 10:
            raise forms.ValidationError("Pesan terlalu pendek. Mohon sampaikan minimal 10 karakter.")
        return pesan
