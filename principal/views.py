from django.shortcuts import render
from principal.populateDB import PopulateDB, crear_schema, populatePuntuacion
from principal.models import JuegoDeMesa, Puntuacion
from principal.forms import BusquedaJuego, BusquedaPorPrecio, RecomiendaJuego, RecomiendaJuegoSimilar
from principal.recommendations import getRecommendations, topMatches, transformPrefs
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser
import re, os, shutil
from whoosh import qparser
import shelve

#Inicio
def inicio(request):
    return render(request,'inicio.html')

#Carga de base de datos
def populateDB(request):
    PopulateDB() 
    crear_schema()
    # populateJuegos()
    populatePuntuacion()
    return render(request, 'populate.html')

#Listado de juegos
def listaJuegos(request):
    juegos = JuegoDeMesa.objects.all()
    return render(request, 'juegos.html', {'juegos':juegos})

#Función auxiliar para comprobar si un juego se encuentra en la base de datos
def compruebaJupiterJuego(juego):
    juegosjupiter=JuegoDeMesa.objects.all()
    juegonombre = juego.replace("\n", "").replace(" ", "")
    lista=set()
    for juegojupiter in juegosjupiter:
        juegonombrejupiter = juegojupiter.titulo
        if juegonombre in juegonombrejupiter.replace("\n", "").replace(" ", ""):
            print(juegonombre)  
            print(juegonombrejupiter)
            if juegonombrejupiter in lista:
                continue
            else:
                lista.add(juegonombrejupiter)
    return lista

def listaPuntuaciones(request):
    puntuaciones = Puntuacion.objects.all()[1:100]
    tamano = Puntuacion.objects.count()
    listajuegos = set()
    for juego in puntuaciones:
        juegonombre = juego.juego_nombre
        listajuegos = set.union(listajuegos, (compruebaJupiterJuego(juegonombre)))
    return render(request, 'puntuaciones.html', {'puntuaciones':puntuaciones, 'tamano':tamano, 'juegosjupiter':listajuegos})


def buscarJuego(request):
    form = BusquedaJuego(request.GET, request.FILES)
    if request.method=='POST':
        form = BusquedaJuego(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['id1']
            ix=open_dir("Index")
            with ix.searcher() as searcher:
                query = QueryParser("titulo", ix.schema).parse(str(texto))
                results = searcher.search(query,limit=None)
                mensaje = "Se han encontrado: " + str(len(results)) + " resultados con la sentencia " + texto
                return render(request, 'buscarJuego.html', {'results': results, 'mensaje': mensaje})
    return render(request, 'buscarJuego.html',{'form':form})


def buscarRango(request):
    form = BusquedaPorPrecio(request.GET, request.FILES)
    if request.method=='POST':
        form = BusquedaPorPrecio(request.POST)
        if form.is_valid():
            rango1 = form.cleaned_data['rango1']
            rango2 = form.cleaned_data['rango2']

            ix=open_dir("Index")
            with ix.searcher() as searcher:
                rango_precio = '['+ str(rango1) + ' TO ' + str(rango2) +']'
                query = QueryParser("precio", ix.schema).parse(rango_precio)
                results = searcher.search(query, limit=None)
                mensaje = "Se han encontrado: " + str(len(results)) + " resultados con la sentencia " + str(rango1) + " - " + str(rango2)
                return render(request, 'buscarRango.html', {'results': results, 'mensaje': mensaje})
    return render(request, 'buscarRango.html',{'form':form})



def loadDict():
    prefs={}
    shelf = shelve.open("RECSYS.dat")
    puntuaciones = Puntuacion.objects.all()
    for puntuacion in puntuaciones:
        user = str(puntuacion.usuario)
        juego = int(puntuacion.juego_id)
        rate = float(puntuacion.puntuacion)
        prefs.setdefault(user,{})
        prefs[user][juego] = rate
    shelf['prefs']=prefs
    shelf['ItemsPrefs']=transformPrefs(prefs)
    shelf.close
    
def loadRS(request):
    loadDict()
    return render(request,'matrizCargada.html')


def recomiendaJuego(request):
    form = RecomiendaJuego(request.GET, request.FILES)
    if request.method=='POST':
        form = RecomiendaJuego(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            shelf = shelve.open("RECSYS.dat")
            Prefs = shelf['prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,usuario)
            recommended = rankings[:5]
            juegos2 = []
            juegos = []
            scores = []
            for rec in recommended:
                juego = Puntuacion.objects.filter(juego_id=rec[1])[0]
                juego = juego.juego_nombre
                juegos2.append(juego)
                juegos.append(rec[1])
                scores.append("{:.10f}".format(rec[0]))
            items= zip(juegos,scores,juegos2)
            return render(request,'recomienda.html', {'usuario': usuario, 'items': items})
    return render(request,'recomienda.html', {'form': form})



def similarJuego(request):
    form = RecomiendaJuegoSimilar(request.GET, request.FILES)
    if request.method=='POST':
        form = RecomiendaJuegoSimilar(request.POST)
        if form.is_valid():
            idJuego = form.cleaned_data['juego']
            shelf = shelve.open("RECSYS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, idJuego,n=5)
            juegos = []
            idjuegos = []
            similar = []
            listajuegos = set()
            for rec in recommended:
                juego = Puntuacion.objects.filter(juego_id=rec[1])[0]
                juego = juego.juego_nombre
                print(juego)
                listajuegos = set.union(listajuegos, (compruebaJupiterJuego(juego)))
                juegos.append(juego)
                idjuegos.append(rec[1])
                similar.append("{:.10f}".format(rec[0]))
            items= zip(juegos,similar, idjuegos)
            return render(request,'recomiendaSimilar.html', {'juego': idJuego,'items': items, 'juegosjupiter': listajuegos})
    return render(request,'recomiendaSimilar.html', {'form': form})
