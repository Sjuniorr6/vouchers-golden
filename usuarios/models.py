from django.db import models

# Create your models here.
# usuarios/models.py

from django.db import models
from django.contrib.auth.models import User
from rota.models import Rota

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rotas = models.ManyToManyField(Rota, blank=True, related_name='userprofiles')

    def __str__(self):
        return f"Perfil de {self.user.username}"
