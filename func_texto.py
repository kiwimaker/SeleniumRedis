# importamos librerias necesarias
from inflector import Inflector, Spanish
import unicodedata
import re

# importamos globales
from globales import *

def comprobarKwEnTexto(keyword, texto, longitud=None):
    global filtro_palabras
    # filtro de palabras
    filtro_texto = ['Referencia:', '"']
    if any(palabra in texto for palabra in filtro_texto):
        return None

    # filtro de longitud
    if longitud is not None:
        if len(texto) < longitud:
            return None

    # limpiamos el texto
    texto = texto.replace('?', '').replace('¿', '')

    # pasamos a minuscula
    keyword = keyword.lower()
    texto = texto.lower()

    # singular y sin tildes
    # declaramos inflector
    n = Inflector(Spanish)

    # keyword ----
    kw_separada = keyword.split(" ")
    length_kw = len(kw_separada)
    i = 0
    while i < length_kw:
        original = kw_separada[i]
        palabra = strip_accents_spain(n.singularize(kw_separada[i]))
        kw_separada[i] = palabra
        i += 1

    # texto ----
    # separamos y pasamos por singularize
    texto = texto.split(" ")
    length = len(texto)
    i = 0
    while i < length:
        original = texto[i]
        palabra = strip_accents_spain(n.singularize(texto[i]))
        texto[i] = palabra
        i += 1
    texto = ' '.join(texto)

    # si encontramos una preposicion en kw_separada, la eliminamos
    kw_separada = list(set(kw_separada).difference(set(filtro_palabras)))

    # comprobamos si todas las kw estan en el parrafo
    i = 0
    for kw_s in kw_separada:
        regex = r""+re.escape(kw_s)+""
        if(re.findall(regex, texto)):
            i = i+1

    # para tres kw
    if(length_kw == 3):
        if i > 1:
            return True
    elif(length_kw == 4):
        if i > 2:
            return True
    elif(length_kw == 5):
        if i > 3:
            return True
    elif(length_kw == 6):
        if i > 4:
            return True
    else:
        if i == length_kw:
            return True

    return None

def strip_accents_spain(string, accents=('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT')):
    accents = set(map(unicodedata.lookup, accents))
    chars = [c for c in unicodedata.normalize('NFD', string) if c not in accents]
    return unicodedata.normalize('NFC', ''.join(chars))

def limpiarTexto(texto):
    texto = texto.lower()

    # stopwords spanish
    # stop_words = set(stopwords.words("spanish"))
    # texto = " ".join([word for word in texto.split() if word not in stop_words])

    # mentions
    texto = re.sub("@\S+", "", texto)

    # remove urls
    texto = re.sub("https?:\/\/.*[\r\n]*", "", texto)

    # removing hashtags 
    texto = re.sub("#", "", texto)

    # tags
    regex = re.compile('<.*?>')
    texto = re.sub(regex, '', texto)

    return texto

def is_question(texto):
    if '?' in texto:
        return True
    return None