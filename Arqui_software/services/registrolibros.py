import socket
import sys
import json
import os
from database import conn
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se pone el puerto del servicio
server_address = ('localhost', 5005)
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
                statement = "INSERT INTO LIBROS(NOMBRE,AUTOR,ANIO,cantidad,estado,genero)VALUES('" + \
                    data["nombre"]+"','"+data["autor"]+"','" + \
                    data["anio"]+"','"+data["cantidad"]+"','" + \
                    data["estado"]+"','"+data["genero"]+"');"
                cursor.execute(statement)
                conn.commit()
                send = str({"status": "200"}
                           ).replace("'", '"')
                print('Correcto registro')
                connection.sendall(str(send).encode())
                break
            except Exception as e:
                print("Error: " + str(e))
                error = str({"status": "404", "error": str(e)}
                            ).replace("'", '"')
                connection.sendall(str(error).encode())
                break
    finally:
        connection.close()
