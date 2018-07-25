from django.db import models


# Create your models here.
class Components(models.Model):
    nombre = models.CharField(max_length=100)
    acciones = models.ManyToManyField('Acciones')

    def __str__(self):
        return '{}'.format(self.nombre)


class Acciones(models.Model):
    nombre = models.CharField(max_length=100)
    hotkeys = models.ManyToManyField('HotKeys')

    def __str__(self):
        return '{}'.format(self.nombre)


class HotKeys(models.Model):
    keycode = models.IntegerField(primary_key=True)
    equivalencia = models.CharField(max_length=50)

    def __str__(self):
        return '{} = {}'.format(self.keycode, self.equivalencia)
