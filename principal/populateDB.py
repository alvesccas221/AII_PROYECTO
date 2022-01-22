# -*- coding: utf-8 -*-
from principal.models import JuegoDeMesa, Puntuacion

import csv
import requests, mechanize, re
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser
import re, os, shutil
from whoosh import qparser 

path = "dataset"

def PopulateDB():
    JuegoDeMesa.objects.all().delete()
    
    i=0
    while i <=20:
        i=i+1
        url = "https://www.jupiterjuegos.com/juegos-de-mesa?page=" + str(i)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f, "lxml")
        juegos = s.find_all("article", class_="product-miniature js-product-miniature")
        for juego in juegos:
            link = juego.a['href']
            if "juegos-de-mesa" not in link:
                continue
            else: 
                f2 = urllib.request.urlopen(link)
                s2 = BeautifulSoup(f2, "lxml")
                titulo = s2.find("h1").string.strip()
                precio = float(s2.find("span", itemprop="price").string.strip().replace("€","").replace(",","."))
                if s2.find("div", class_="product-description").p is not None:
                    descripcion = s2.find("div", class_="product-description").p.text
                    if s2.find("dl", class_="data-sheet") is not None:
                        jugadores = s2.find("dl", class_="data-sheet").dd
                        edad = jugadores.find_next_sibling("dd")
                        dificultad = edad.find_next_sibling("dd")
                        if dificultad.find_next_sibling("dd") is not None:
                            tiempo = dificultad.find_next_sibling("dd")
                            if tiempo.find_next_sibling("dd") is not None:
                                idioma = tiempo.find_next_sibling("dd")
                                jugadores = jugadores.text.replace("  - ",", ")
                                edad = int(edad.text.replace("+",""))
                                dificultad = dificultad.text
                                tiempo = int(tiempo.text.replace("'","").replace(" o más",""))
                                idioma = idioma.text
                                m = JuegoDeMesa.objects.create(titulo = titulo, precio = precio, 
                                                               descripcion = descripcion, jugadores = jugadores, 
                                                               edad = edad, dificultad = dificultad, duracion = tiempo, 
                                                               idioma = idioma)
    return True


def crear_schema():
        schem = Schema(titulo=TEXT(stored=True), precio=NUMERIC(numtype=float,stored=True), 
                   descripcion=TEXT(stored=True), jugadores=TEXT(stored=True), edad=NUMERIC(numtype=int,stored=True), 
                   dificultad=TEXT(stored=True), duracion=NUMERIC(numtype=int, stored=True), idioma=TEXT(stored=True))
    
        if os.path.exists("Index"):
            shutil.rmtree("Index")
        os.mkdir("Index")
    
        ix1 = create_in("Index", schema=schem)
        writer = ix1.writer()
        i=0
        lista=JuegoDeMesa.objects.all()
        for juego in lista:
            writer.add_document(titulo=juego.titulo, precio=juego.precio,
                   descripcion=juego.descripcion, jugadores=juego.jugadores, edad=juego.edad, dificultad=juego.dificultad, 
                   duracion=juego.duracion, idioma=juego.idioma)
            i+=1
        writer.commit()    
        
def populatePuntuacion():
    Puntuacion.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\bgg-15m-reviews.csv", "r", encoding="utf-8")
    next(fileobj)
    for line in fileobj:
        rip = line.split(",")
        if len(rip)==6:
            p=Puntuacion(usuario=rip[1],puntuacion=rip[2],juego_id=rip[4], juego_nombre=rip[5])
            lista.append(p)
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)
        