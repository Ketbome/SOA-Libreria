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
        # Recepcion de datos
        while True:
            data = connection.recv(4096).decode()
            data = json.loads(data)

            if data["rol"] == "1":  # Admin
                try:
                    # Ejecuta la consulta
                    cursor = conn.cursor()
                    # ver estado de todos los libros
                    statement = "SELECT id_libro, nombre, cantidad, estado FROM libros order by id_libro asc;"
                    cursor.execute(statement)
                    results = cursor.fetchall()
                    data_json = json.dumps({"status": "200", "data": results})
                    send = str(data_json).replace("'", '"').encode()
                    connection.sendall(send)
                    break
                except Exception as e:
                    print("Error: " + str(e))
                    error = str({"status": "404", "error": str(e)}
                                ).replace("'", '"')
                    connection.sendall(str(error).encode())
                    break
            elif data["rol"] == "0":  # Usuarios
                try:
                    # Ejecuta la consulta
                    cursor = conn.cursor()
                    # ver estado de todos los libros
                    statement = "SELECT id_libro, nombre, autor, genero, anio FROM libros WHERE estado = 'Disponible' order by id_libro asc;"
                    cursor.execute(statement)
                    results = cursor.fetchall()
                    data_json = json.dumps({"status": "200", "data": results})
                    send = str(data_json).replace("'", '"').encode()
                    connection.sendall(send)
                    break
                except Exception as e:
                    print("Error: " + str(e))
                    error = str({"status": "404", "error": str(e)}
                                ).replace("'", '"')
                    connection.sendall(str(error).encode())
                    break
            else:
                print(data)
                print("Llegaron mal los parametros")
                error = str({"status": "401"
                             }
                            ).replace("'", '"')
                connection.sendall(str(error).encode())
                break

    finally:
        connection.close()
