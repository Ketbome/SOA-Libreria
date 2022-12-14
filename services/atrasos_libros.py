import socket
import sys
import json
import os
from database import conn
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Puerto del servicio
server_address = ('localhost', 5004)
print('Iniciando {} puerto {}'.format(*server_address))
sock.bind(server_address)

# Escucha conexiones 1 maximo 
sock.listen(1)

while True:
    
    # Esperando la conexion
    print('Esperando conexión...')
    connection, client_address = sock.accept()
    try:
        print('Conectado en', client_address)
        
        # Recepcion de datos
        while True:
            
            data = connection.recv(4096).decode()
            print(data)
            data = json.loads(data)

            try:
                # Ejecuta la consulta
                cursor = conn.cursor()
                statement = """
                    SELECT prestamo.id_prestamo, usuarios.id_user, libros.id_libro, libros.nombre, libros.autor, prestamo.dia_prestamo, prestamo.dia_entrega, date_part('day', NOW()) - date_part('day', prestamo.dia_entrega) AS dias_atraso
                    FROM usuarios, libros, prestamo
                    WHERE date_part('day', NOW()) - date_part('day', dia_entrega) > 0
                    AND prestamo.id_user = usuarios.id_user
                    AND prestamo.id_libro = libros.id_libro;"""  #ver todos los libros con atraso
                #ver atrasos por usuario (mediante id_user)
                #statement = """
                    # SELECT usuarios.username, libros.id_libro, libros.nombre, libros.autor, prestamo.id_prestamo, date_part('day', NOW()) - date_part('day', prestamo.dia_entrega) AS dias_atraso
                    # FROM libros, prestamo, usuarios
                    # WHERE prestamo.id_user = '"+data["id_user"]+"
                    # AND prestamo.id_libro = libros.id_libro
                    # AND prestamo.id_user = usuarios.id_user
                    # AND date_part('day', NOW()) - date_part('day', dia_entrega) > 0; """ 
                cursor.execute(statement)
                results = cursor.fetchall()
                print(results)
                
                break
            except:
                print("Error")
                break
            
    finally:
        connection.close()