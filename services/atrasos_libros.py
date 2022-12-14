import socket
import sys
import json
import os
from database import conn

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
                statement = "SELECT prestamo.id_libro as id, libros.nombre as nombre, libros.autor as autor, cast(prestamo.dia_prestamo AS TEXT) as pp, cast(prestamo.dia_entrega AS TEXT) as pe FROM prestamo INNER JOIN libros ON prestamo.id_libro = libros.id_libro INNER JOIN usuarios ON prestamo.id_user = usuarios.id_user WHERE prestamo.id_user = '" + \
                    data["id_user"]+"' and prestamo.entregado = '0';"
                cursor.execute(statement)
                results = cursor.fetchall()
                if len(results) > 0:
                    data_json = json.dumps({"status": "200", "data": results})
                    print(data_json)
                    send = str(data_json).replace("'", '"').encode()
                    print(send)
                    connection.sendall(send)
                    break
                elif len(results) == 0:
                    send = str({"status": "201"}
                               ).replace("'", '"')
                    connection.sendall(send.encode())
                    break
            except Exception as e:
                print("Error: " + str(e))
                error = str({"status": "404"}
                            ).replace("'", '"')
                connection.sendall(error.encode())
                break

    finally:
        connection.close()
