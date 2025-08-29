from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('certificado/<uuid:cert_id>/', views.verificar_certificado, name='verificar_certificado'),
    path('download/<uuid:cert_id>/', views.download_pdf, name='download_pdf'),
]