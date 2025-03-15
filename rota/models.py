from django.db import models

# Create your models here.
# rota/models.py

from django.db import models
from posto.models import Posto  # Importando o modelo Posto

class Rota(models.Model):
    nome = models.CharField(max_length=100)
    postos = models.ManyToManyField(Posto, related_name='rotas')
    

    def __str__(self):
        return self.nome
