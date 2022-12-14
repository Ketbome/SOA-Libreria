import socket
import sys
import json
import os
from database import conn
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Puerto del servicio
server_address = ('localhost', 5008)
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
                statement = "SELECT bloqueo FROM USUARIOS WHERE username='" + data["username"]+"';"
               
                cursor.execute(statement)

                # Muestra los resultados de la consulta
                results = cursor.fetchall()
                if len(results) == 1:
                    # Actualiza el libro con esa id
                    statement = "SELECT bloqueo FROM  USUARIOS WHERE username = '" + data["username"]+"';"
                    cursor.execute(statement)
                    conn.commit()
                    print('Estado de la cuenta')
                   
                    connection.sendall(str(results[0][0]).encode())
                elif len(results) == 0:
                    # Se envia el 404 cuando no existe o se puso un mal dato
                    connection.sendall(str(420).encode())
                
                break
            except Exception as e:
                print("Error al consultar: ", e)
                connection.sendall(str(411).encode())
                break
    finally:
        connection.close()

               