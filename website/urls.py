"""URL Routing untuk aplikasi website PCM Gatak."""

from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('profil/', views.profil, name='profil'),
    path('pimpinan/', views.pimpinan, name='pimpinan'),
    path('ranting/', views.ranting, name='ranting'),
    path('amal-usaha/', views.amal_usaha, name='amal_usaha'),
    path('berita/', views.berita_daftar, name='berita_daftar'),
    path('berita/<slug:slug>/', views.berita_detail, name='berita_detail'),
    path('agenda/', views.agenda, name='agenda'),
    path('unduhan/', views.unduhan, name='unduhan'),
    path('kontak/', views.kontak, name='kontak'),
    path('sumber-informasi/', views.sumber_informasi, name='sumber_informasi'),
]
