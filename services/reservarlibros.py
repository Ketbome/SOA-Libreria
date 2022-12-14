import socket
import sys
import json
import os
from database import conn
import hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Puerto del servicio
server_address = ('localhost', 5010)
print('Iniciando {} puerto {}'.format(*server_address))
sock.bind(server_address)

# Se tienen como maximo 1 conexion
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
                # Se ve si el libro existe para reserva
                statement = "SELECT 1 FROM prestamo WHERE id_user = '" + \
                    data["id_user"]+"' and entregado = '0';"
                cursor.execute(statement)
                results = cursor.fetchall()
                if len(results) == 0:
                    # Se ve si el libro existe para reserva
                    statement = "SELECT nombre, cantidad FROM libros WHERE id_libro = '" + \
                        data["id_libro"]+"';"
                    cursor.execute(statement)
                    results = cursor.fetchall()
                    if int(results[0][1]) >= 1:
                        if int(results[0][1]) == 1:
                            # Si está disponible la cantidad baja -1 y pasa a no disponible
                            statement = "UPDATE libros SET cantidad = cantidad - 1, estado = 'No Disponible' WHERE id_libro = '" + \
                                data["id_libro"]+"' AND estado = 'Disponible';"
                            cursor.execute(statement)
                            conn.commit()
                        else:
                            # Si está disponible la cantidad baja -1
                            statement = "UPDATE libros SET cantidad = cantidad - 1 WHERE id_libro = '" + \
                                data["id_libro"]+"' AND estado = 'Disponible';"
                            cursor.execute(statement)
                            conn.commit()
                        # Se inserta el prestamo (entregado = 0)
                        statement = "INSERT INTO prestamo(id_user,id_libro,dia_prestamo,dia_entrega,entregado)VALUES('" + \
                            data["id_user"]+"','" + data["id_libro"] + \
                            "',NOW(),NOW() + interval '1 month',0);"
                        cursor.execute(statement)
                        conn.commit()

                        print("Reserva exitosa")
                        send = str({"status": "200"}
                                   ).replace("'", '"')
                        connection.sendall(str(send).encode())
                        break
                    else:
                        print("No Disponible")
                        send = str({"status": "401", "data": "No Disponible"}
                                   ).replace("'", '"')
                        connection.sendall(str(send).encode())
                        break
                else:
                    print("Entrega pendiente")
                    send = str({"status": "402", "data": "Entrega pendiente"}
                               ).replace("'", '"')
                    connection.sendall(str(send).encode())
                    break
            except Exception as e:
                # Se produce un error
                print("Error: " + str(e))
                error = str({"status": "404"}
                            ).replace("'", '"')
                connection.sendall(str(error).encode())
                break

    finally:
        connection.close()
