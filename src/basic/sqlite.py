import sqlite3
conexion = sqlite3.connect('ejemplo.db')
cursor = conexion.cursor()
# cursor.execute('CREATE TABLE usuarios(nombre VARCHAR(100), edad INTEGER, email VARCHAR(100))')
cursor.execute('INSERT INTO usuarios VALUES (\'HECTOR\', 27, \'hector@ejemplo.com\')')
conexion.commit()
conexion.close()