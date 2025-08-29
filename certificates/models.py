from django.db import models
import uuid

class Certificado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    curso = models.CharField(max_length=200)
    data_emissao = models.CharField(max_length=20)  # formato: 01/01/2025
    status = models.CharField(max_length=20, default='ativo')

    def __str__(self):
        return f"{self.nome} - {self.curso}"