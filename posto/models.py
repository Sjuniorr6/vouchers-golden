# posto/models.py

from django.db import models
from gerentes.models import Gerente  # Importa o modelo Gerente

class Posto(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)  # Ex.: 'SP', 'RJ'...
    endereco = models.CharField(max_length=200)
    gerente = models.ForeignKey(
        Gerente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Gerente"
    )

    def __str__(self):
        return self.nome
