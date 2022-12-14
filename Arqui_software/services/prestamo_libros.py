import socket
import sys
import json
import os
from database import conn
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Puerto del servicio
server_address = ('localhost', 5009)
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
                #1. Ver si libro existe.
                statement = "SELECT nombre FROM libros WHERE id_libro = '"+data["id_libro"]+"'"
                cursor.execute(statement)
                results1 = cursor.fetchall()

                if len(results1) == 1:
                    #2. Si está disponible => baja cantidad -1
                    statement = "UPDATE libros SET cantidad = cantidad - 1 WHERE id_libro = '"+data["id_libro"]+"' AND estado = 'Disponible'"
                    cursor.execute(statement)
                    #3. Si cantidad = 0 => Estado = No Disponible
                    statement = "UPDATE libros SET estado = 'No Disponible' WHERE id_libro = '"+data["id_libro"]+"' and cantidad = 0;"
                    cursor.execute(statement)
                    #3. Inserta prestamo en tabla prestamo con prestamo de 14 días respecto a fecha actual.
                    statement = "INSERT INTO prestamo (id_user, id_libro, dia_prestamo, dia_entrega) VALUES ('"+data["id_user"]+"', '"+data["id_libro"]+"', NOW(), current_date + interval '14 day');"
                    cursor.execute(statement)
                    conn.commit()

                elif len(results1) == 0:
                    # Se envia el 404 cuando no existe o se puso un mal dato
                    connection.sendall(str(405).encode())    
                break
            except:
                print("Error")
                break
            
    finally:
        connection.close()
        