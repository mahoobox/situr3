"""import MySQLdb
 
DB_HOST = '192.95.22.65' 
DB_USER = 'sitursit_bot' 
DB_PASS = 'RwfMXSUurWCX' 
DB_NAME = 'sitursit_bot' 
 
def run_query(query=''): 
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
 
    conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 
 
    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
 
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 
 
    return data"""
import sys

soyversion = sys.version

print(soyversion)


import MySQLdb
import time




def maindb():
  # Connect to the MySQL database
    db = MySQLdb.connect(host = '192.95.22.65', user = 'sitursit_bot', passwd = 'RwfMXSUurWCX', db = 'sitursit_bot')
    #db = MySQLdb.connect(host = '23.96.113.148', user = 'SITUR_BOT', passwd = 'O9pIeuNfF1BMQM1W', db = 'SITUR_BOT')
    cursor = db.cursor()

    valorconsultado = "y aun mas consultas de acá"
    fechayhora= str(time.time())
    print(fechayhora)
    fechayhora2="1505308957.3476646"


    sql2 = """INSERT INTO `atractivos_cons` (`ID`, `fecha_hora`, `sexo`, `edad`, `ubicacion`, `atractivo_buscado`) VALUES (NULL, NULL, 'M', '28', 'Líbano, Colombia', '"""+valorconsultado+"""')"""

    cursor.execute(sql2)

    db.close()




def maindb2():
  # Connect to the MySQL database
    db = MySQLdb.connect(host = 'localhost', user = 'admin', passwd = 'd12190', db = 'mysql')
    # Check if connection was successful
    if (db):
        # Carry out normal procedure
        databasemauricio= "Connection successful"
        print("me conecté hpt")
    else:
        # Terminate
        databasemauricio = "Connection unsuccessful"
        print("no me pude conectar")


maindb()