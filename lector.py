import glob
import json
import mysql.connector

conexion = mysql.connector.connect(user ='erm', password='1234567', database='casas')

cursor = conexion.cursor()

files = glob.glob('*.json')

tipo = {'venta': 1, 'renta': 2}
origen = {'informador': 1}

for file in files:
    with open(file, encoding = 'utf-8') as f:
        casas = json.load(f)
        for casa in casas:
            # print(casa['ubicacion'])
            select = 'SELECT * FROM municipio WHERE nombre = %s'
            cursor.execute(select, (casa['ubicacion'], ))
            if len(cursor.fetchall()) == 0:
                insert = 'INSERT INTO municipio(nombre) VALUES(%s)'
                cursor.execute(insert, (casa['ubicacion'], ))
                conexion.commit()
                id_muni = cursor.lastrowid

                insert = 'INSERT INTO colonia(nombre, id_municipio) VALUES(%s, %s)'
                cursor.execute(insert, (casa['colonia'], id_muni))
                conexion.commit()
                id_colonia = cursor.lastrowid

                select = 'SELECT * FROM fecha WHERE fecha = %s'
                cursor.execute(select, (file[:-5], ))
                id_fecha = 0
                rows = cursor.fetchall()
                if len(rows) == 0:

                    insert = 'INSERT INTO fecha(fecha) VALUES(%s)'
                    cursor.execute(insert, (file[:-5], ))
                    conexion.commit()
                    id_fecha = cursor.lastrowid

                else:
                    id_fecha = rows[0][0]


                insert = 'INSERT INTO bienraiz(titulo, precio, m2, rooms, baths, cars, descripcion, id_tipo, id_origen, id_colonia, id_fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(insert, (casa['titulo'],
                                            casa['precio'],
                                            casa['m2'],
                                            casa['recamaras'],
                                            casa['wc'],
                                            casa['cars'],
                                            casa['descripcion'],
                                            tipo[casa['tipo']],
                                            1,
                                            id_colonia,
                                            id_fecha))

                conexion.commit()
