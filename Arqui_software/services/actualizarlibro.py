import socket
import sys
import json
import os
from database import conn
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Puerto del servicio
server_address = ('localhost', 5006)
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
                statement = "SELECT nombre FROM LIBROS WHERE id_libro = '" + \
                    data["id_libro"]+"';"
                cursor.execute(statement)
                results = cursor.fetchall()
                # print(results)
                if len(results) == 1:
                    # Actualiza el libro con esa id
                    statement = "UPDATE libros SET cantidad = '" + \
                        data["cantidad"]+"', estado = 'Disponible' WHERE id_libro = '" + \
                        data["id_libro"]+"';"
                    cursor.execute(statement)
                    conn.commit()
                    print('Libro actualizado')
                    # Se envia un el nombre del libro diciendo que esta bien hecho
                    # print(results[0][0])
                    connection.sendall(str(results[0][0]).encode())
                elif len(results) == 0:
                    # Se envia el 405 cuando no existe o se puso un mal dato
                    connection.sendall(str(405).encode())
                break
            except Exception as e:
                print("Error al actualizar el libro: ", e)
                connection.sendall(str(404).encode())
                break

    finally:
        connection.close()
