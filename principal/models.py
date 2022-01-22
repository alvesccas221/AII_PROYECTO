from django.db import models

# Create your models here.


class JuegoDeMesa(models.Model):
    titulo = models.TextField(verbose_name='Título')
    precio = models.FloatField(verbose_name='Precio')
    descripcion = models.TextField(verbose_name='Descripción')
    jugadores = models.TextField(verbose_name='Jugadores')
    edad = models.PositiveIntegerField(verbose_name='Edad')
    dificultad = models.TextField(verbose_name='Dificultad')
    duracion = models.PositiveIntegerField(verbose_name='Duración')
    idioma = models.TextField(verbose_name='Idioma')
    # url = models.URLField()

    
class Puntuacion(models.Model):
    usuario = models.TextField()
    puntuacion = models.FloatField()
    juego_id = models.PositiveIntegerField()
    juego_nombre = models.TextField()