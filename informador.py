import  requests
import json
from bs4 import BeautifulSoup
import datetime

class Informador:
    def __init__(self):
        self.lista =[]
        self.top =0;

    def to_json(self):
        with open(datetime.datetime.now().strftime('%Y-%m-%d')+'.json', 'w') as archivo:
            json.dump(self.lista, archivo, sort_keys=False, indent=4)
    def scrapping(self,url1,co):
        self.top=co
        # guardamos el url en una variable
        url = url1

        # obtenemos todo el html del url y lo guardamos en r
        r = requests.get(url)
        r.encoding = 'utf-8'

        # print(r.text)

        # Convertimos el texto a un tipo con el cual podemos trabajar
        soup = BeautifulSoup(r.text, 'html.parser')

        # print(soup)

        # Encontramos todos los objetos de clase items
        items = soup.find_all(class_='items')
        # print(items)

        # todos los items se guardan en na variable con solo la posicion 0, conseguimos cada elemento de la lista en casas
        casas = items[0].find_all('li')

        self.scrapping_casas(casas)

        paginas = soup.find(class_="pagination")
        pagina = paginas.find_all('li')
        urls = []
        i = 2
        while i < len(pagina) - 1:

            urls.append(pagina[i].a['href'])
            i = i + 1
        print(len(urls))

        self.scrapping_paginas(urls,url1)

    def scrapping_paginas(self,urls,url1):
        for url in urls:
            r= requests.get(url)
            r.encoding ='uft-8'
            url = url1
            r = requests.get(url)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.find_all(class_='items')
            casas = items[0].find_all('li')
            self.scrapping_casas(casas)

    def scrapping_casas(self,casas):
        if self.top == 1 or self.top ==2:
            for c in casas:
                casa = {
                    "ubicacion": c.find_all(class_='location')[0].text,
                    "titulo": c.a.text,
                    "precio": c.h5.text,
                    "descripcion": c.p.text,
                    "recamaras": c.find(class_='info-rec').text,
                    "m2": c.find(class_='info-m2').text,
                    "m2_2": c.find(class_='info-m2-2').text,
                    "wc": c.find(class_='info-wc').text,
                    "cars": c.find(class_='info-cars').text,
                    "colonia": c.find(class_='info-gps').contents[1],
                    "imgs": ['http:' + i['src'] for i in c.find_all('img')],
                    "tipo": "venta"
                }
                self.lista.append(casa)
        elif self.top == 3 or self.top == 4:
                for c in casas:
                    casa = {
                        "ubicacion": c.find_all(class_='location')[0].text,
                        "titulo": c.a.text,
                        "precio": c.h5.text,
                        "descripcion": c.p.text,
                        "recamaras": c.find(class_='info-rec').text,
                        "m2": c.find(class_='info-m2').text,
                        "m2_2": c.find(class_='info-m2-2').text,
                        "wc": c.find(class_='info-wc').text,
                        "cars": c.find(class_='info-cars').text,
                        "colonia": c.find(class_='info-gps').contents[1],
                        "imgs": ['http:' + i['src'] for i in c.find_all('img')],
                        "tipo": "renta"
                    }
                    self.lista.append(casa)
