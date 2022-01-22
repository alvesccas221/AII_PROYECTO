# Generated by Django 4.0.1 on 2022-01-15 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JuegoDeMesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(verbose_name='Título')),
                ('precio', models.FloatField(verbose_name='Precio')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('jugadores', models.TextField(verbose_name='Jugadores')),
                ('edad', models.PositiveIntegerField(verbose_name='Edad')),
                ('dificultad', models.TextField(verbose_name='Dificultad')),
                ('duracion', models.PositiveIntegerField(verbose_name='Duración')),
                ('idioma', models.TextField(verbose_name='Idioma')),
            ],
        ),
    ]
