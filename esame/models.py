from types import NoneType

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

SCELTE = [('Sat', 'Satira'),
          ('Bar', 'Barzelletta'),
          ('Bhu', 'Black Humor'),
          ('Bsq', 'Battute Squallide')]


class ProfiloDettagliato(models.Model):
    utente = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ciao')
    foto_profilo = models.ImageField(null=True)
    bio = models.TextField(default="", blank=True)
    nome = models.CharField(max_length=25, blank=True)
    cognome = models.CharField(max_length=50, blank=True)
    datadinascita = models.DateField(null=True)
    email = models.EmailField(null=True)
    citta = models.CharField(max_length=50, blank=True)


class Battute(models.Model):
    testo = models.TextField(default="")
    utente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='utentebat')
    tempo = models.DateTimeField(auto_now=True)
    tipo = models.CharField(choices=SCELTE, default='bar', max_length=3)

    @property
    def calcola_media(self):
        media_tupla = self.battutarec.all().aggregate(Avg('voto'))
        media_lunga = media_tupla['voto__avg']
        if type(media_lunga) is NoneType:
            media = media_lunga
        else:
            media = round(media_lunga, 2)
        return media


class Recensioni(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    battuta = models.ForeignKey(Battute, on_delete=models.CASCADE, to_field='id', related_name='battutarec')
    voto = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Follower(models.Model):
    seguitore = models.ForeignKey(User, on_delete=models.CASCADE)
    seguito = models.ForeignKey(User, on_delete=models.CASCADE)
