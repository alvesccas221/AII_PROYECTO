#encoding:utf-8
from django import forms

   
class BusquedaJuego(forms.Form):
    id1 = forms.CharField(label='Título del juego a buscar')
    
    
class BusquedaPorPrecio(forms.Form):
    rango1 = forms.FloatField(label="Precio mínimo")
    rango2 = forms.FloatField(label="Precio máximo", required=True)


class RecomiendaJuego(forms.Form):
    usuario = forms.CharField(label='Nombre de usuario')
    
    
class RecomiendaJuegoSimilar(forms.Form):
    juego = forms.IntegerField(label='Id del juego')
    