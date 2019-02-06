#Importamos las dos librerias necesarias
import  requests
import json
from bs4 import BeautifulSoup

# guardamos el url en una variable
url = "http://aviso.informador.com.mx/index.php/bienes_raices/busqueda?selecciono=1&ciudad_autocomplete=0&colonia_autocomplete=&transaccion=1&tipo=1&consulta=Zona+Metropolitana&precio_min=min&precio_max=max&recamaras_min=0&recamaras_max=0&metros_min=0&metros_max=0&quick-search=Zona+metropolitana-&quick-searchZap=Zapopan-3&quick-searchGdl=Guadalajara-2&quick-searchTlaq=Tlaquepaque-5&quick-searchTon=Tonalá-4"


# obtenemos todo el html del url y lo guardamos en r
r = requests.get(url)
r.encoding = 'utf-8'

#print(r.text)

#Convertimos el texto a un tipo con el cual podemos trabajar
soup = BeautifulSoup(r.text, 'html.parser')

#print(soup)


#Encontramos todos los objetos de clase items
items = soup.find_all(class_ = 'items')
# print(items)

#todos los items se guardan en na variable con solo la posicion 0, conseguimos cada elemento de la lista en casas
casas = items[0].find_all('li')
# print(casas)
lista = []
for c in casas:
    casa ={
        "ubicacion": c.find_all(class_='location')[0].text,
        "titulo": c.a.text,
        "precio": c.h5.text,
        "descripcion": c.p.text,
        "recamaras": c.find(class_ = 'info-rec').text,
        "m2": c.find(class_ = 'info-m2').text,
        "m2_2": c.find(class_ = 'info-m2-2').text,
        "wc": c.find(class_ = 'info-wc').text,
        "cars": c.find(class_ = 'info-cars').text,
        "colonia": c.find(class_ = 'info-gps').contents[1],
        "imgs": ['http:' + i['src'] for i in c.find_all('img')]
    }
    lista.append(casa)

# print(lista)

with open('ínformador.json', 'w') as archivo:
    json.dump(lista, archivo, sort_keys=False, indent=4)

paginas = soup.find(class_="pagination")
pagina =  paginas.find_all('li')
urls = []
i=2
while i <len(pagina)-1:
    //print(pagina[i].a['href'])
    urls.append(pagina[i].a['href'])
    i = i + 1
# c = casas[0]
# c.span
# ubicacion = c.find_all(class_='location')[0].text
# titulo = c.a.text
# precio = c.h5.text
# descripcion = c.p.text
# recamaras = c.find(class_ = 'info-rec').text
# m2 = c.find(class_ = 'info-m2').text
# m2-2 = c.find(class_ = 'info-m2-2').text
# wc = c.find(class_ = 'info-wc').text
# cars = c.find(class_ = 'info-cars').text
# colonia = c.find(class_ = 'info-gps').contents[1]

# imgs = ['http:' + i['src'] for i in c.find_all('img')