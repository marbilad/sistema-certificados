from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from .models import Certificado
import csv
import qrcode
from fpdf import FPDF
import os
from django.conf import settings
from django.core.files.storage import default_storage
from datetime import datetime

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        decoded_file = arquivo.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            nome = row['nome'].strip()
            empresa = row['empresa'].strip()
            curso = row['curso'].strip()
            data_emissao = datetime.now().strftime("%d/%m/%Y")

            # Criar certificado
            cert = Certificado.objects.create(
                nome=nome,
                empresa=empresa,
                curso=curso,
                data_emissao=data_emissao,
                status='ativo'
            )

            # Gerar QR Code
            url = request.build_absolute_uri(f'/certificado/{cert.id}/')
            qr = qrcode.make(url)
            qr_path = f"qrcodes/{cert.id}.png"
            full_qr_path = os.path.join(settings.MEDIA_ROOT, qr_path)
            os.makedirs(os.path.dirname(full_qr_path), exist_ok=True)
            qr.save(full_qr_path)

            # Gerar PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', size=16)
            pdf.cell(0, 10, "CERTIFICADO DE CONCLUSÃO", ln=True, align='C')
            pdf.ln(10)

            if os.path.exists(os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'certificates' / 'static', 'logo.png')):
                try:
                    pdf.image(os.path.join(settings.STATIC_ROOT or settings.BASE_DIR, 'certificates/static/logo.png'), x=85, y=30, w=40)
                    pdf.ln(50)
                except:
                    pass

            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Nome: {nome}", ln=True, align='C')
            pdf.cell(0, 10, f"Empresa: {empresa}", ln=True, align='C')
            pdf.cell(0, 10, f"Curso: {curso}", ln=True, align='C')
            pdf.cell(0, 10, f"Emissão: {data_emissao}", ln=True, align='C')
            pdf.ln(20)
            pdf.cell(0, 10, "Este certificado pode ser verificado em:", ln=True, align='C')
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 10, url, ln=True, align='C')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(10)
            pdf.image(full_qr_path, x=80, y=pdf.get_y(), w=50)

            # Salvar PDF
            # pdf_path = f"pdfs/{cert.id}.pdf"
            pdf_path = os.path.join(settings.MEDIA_ROOT, f'pdfs/certificado_{nome.replace(" ", "_")}_{cert.id}.pdf')
            full_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
            os.makedirs(os.path.dirname(full_pdf_path), exist_ok=True)
            pdf.output(full_pdf_path)

        return render(request, 'certificates/upload.html', {'success': True, 'count': Certificado.objects.count()})

    return render(request, 'certificates/upload.html')

def verificar_certificado(request, cert_id):
    cert = get_object_or_404(Certificado, id=cert_id)
    return render(request, 'certificates/verify.html', {'cert': cert})

def download_pdf(request, cert_id):
    cert = get_object_or_404(Certificado, id=cert_id)
    pdf_path = os.path.join(settings.MEDIA_ROOT, f'pdfs/{cert_id}.pdf')
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="certificado_{cert.nome.replace(" ", "_")}.pdf"'
            return response
    raise Http404("PDF não encontrado")