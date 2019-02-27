import glob
import json
import mysql.connector
conexion = mysql.connector.connect(user='erm',password ='1234567',database = 'casas')
cursor = conexion.cursor()
files = glob.glob('*.json')
tipo = {'venta':1,'renta':2}
origen={'informador':1}
for file in files:
    with open(file) as f:
        casas = json.load(f)
        #print(casas)
        for casa in casas:
           #print(casa['ubicacion'])
            select = 'SELECT * FORM municipio WHERE nombre = %s'
            cursor.execute(select,(casa['ubicacion'],))
            if len(cursor.fetchall()) == 0:
                 insert = 'INSERT INTO municipios(nombre) VALUES (%s)'
                 cursor.execute(insert,(casa['ubicacion'],))
                 conexion.commit()

                 id_muni = cursor.lastrowid
                 insert = 'INSERT INTO colonia(nombre,id_municipio) VALUES (%s,%s)'
                 cursor.execute(insert, (casa['colonia'],id_muni))
                 id_colonia = cursor.lastrowid
                 conexion.commit()

                 select = 'SELECT * FORM fecha WHERE fecha = %s'
                 cursor.execute(select, (file[:-5],))
                 if_fecha = 0
                 row = cursor.fetchall();
                 if len(cursor.fetchall()==0):
                     insert = 'INSERT INTO fecha(fecha) VALUES (%s)'
                     cursor.execute(insert, (file[:-5]))
                     conexion.commit()
                     print(cursor.lastrowid)
                     id_fecha = cursor.lastrowid
                 else:
                     if_fecha = row[0][0]
                     insert = 'INSERT INTO bienraiz(titulo,precio,m2,rooms,baths,cars,descripcion,id_tipo,id_origen,id_colonia,id_fecha) VALUES (%s,%s,%s,%s%s,%s,%s,%s,%s,%s)'

                     cursor.execute(insert, (casa['titulo'],casa['precio'],casa['m2'],casa['recamaras'],casa['wc'],casa['cars'],casa['descripcion'],casa['tipo'],1,1,id_colonia,id_fecha))
                     conexion.commit()



