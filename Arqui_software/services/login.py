import socket
import sys
import json
import os
from database import conn
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se pone el puerto del servicio
server_address = ('localhost', 5002)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Escucha conexiones 1 maximo y entra en el while
sock.listen(1)

while True:
    # Espera la conexion
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
                # Cursor para ejecutar la query
                cursor = conn.cursor()
                statement = "SELECT id_user, username, bloqueo, rol FROM usuarios WHERE username='" + \
                    data["username"]+"' and password = '"+data["password"]+"';"
                cursor.execute(statement)
                results = cursor.fetchall()
                print(results)
                if len(results) == 0:
                    connection.sendall(str(404).encode())
                elif len(results) == 1:
                    list = results[0]
                    # Descomponer la tupla en variables individuales.
                    id_user, username, bloqueo, rol = list
                    enviar = str(id_user)+","+username+"," + \
                        str(bloqueo)+","+str(rol)
                    connection.sendall(str(enviar).encode())
                break
            except:
                connection.sendall(str(400).encode())
                print("Error")
                break
    finally:
        connection.close()
