import socket
import sys
import json
import os
from database import conn
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se pone el puerto del servicio
server_address = ('localhost', 5001)
print('Iniciando {} puerto {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
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
                statement = "INSERT INTO USUARIOS(USERNAME,PASSWORD,EMAIL,BLOQUEO,ROL)VALUES('" + \
                    data["username"]+"','"+data["password"]+"','" + \
                    data["email"]+"','"+data["bloqueo"]+"','"+data["rol"]+"');"
                cursor.execute(statement)
                conn.commit()
                print('Correcto registro')
                connection.sendall(str(-1).encode())
                break
            except Exception as e:
                print("Error: " + str(e))
                connection.sendall(str(e).encode())
                break
    finally:
        connection.close()
