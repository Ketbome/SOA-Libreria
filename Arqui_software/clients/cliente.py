import socket
import json
from os import system, name
from prettytable import PrettyTable

global sesion
sesion = {"id": None, "username": None, "bloqueo": None, "rol": None}

################################### CLIENTE MAIN ########################################


def menuSULI():
    menu = """
    +-------------------------------------+
    | Usuario                             |
    +-------------------------------------+
    | Elija una opción:                   |
    | 1) Registrar un usuario             |
    | 2) Ingresar con usuario             |
    +-------------------------------------+

    Opción: """
    option = input(menu)
    if option == "1":
        menuSU()
    elif option == "2":
        menuLI()
    else:
        print("Opción ingresada no válida.")
        menuSULI()

################################### RESGISTRO ########################################


def menuSU():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Se ponen los datos de la conexion con servidor
    server_address = ('localhost', 5001)
    # Intenta la conexion en caso de no conectarse el servicio no esta encendido o no disponible
    try:
        sock.connect(server_address)
    except:
        menuUN = """
            ---------------------------------------
            | Servicio no disponible              |
            ---------------------------------------
            """
        print(menuUN)
        menuSULI()
    username = None
    password = None
    email = None
    rol = 0  # Usuario

    menuUN = """
    ---------------------------------------
    | Resgistro                           |
    |-------------------------------------|
    | Ingresar nombre de usuario          |
    ---------------------------------------

    Usuario: """
    username = input(menuUN)

    menuPW = """
    ---------------------------------------
    | Registro                            |
    |-------------------------------------|
    | Ingresar contraseña                 |
    ---------------------------------------
    
    Contraseña: """
    password = input(menuPW)

    menuEM = """
    ---------------------------------------
    | Registro                            |
    |-------------------------------------|
    | Ingresar email                      |
    ---------------------------------------
    
    Contraseña: """
    email = input(menuEM)

    menuYN = f"""
    ---------------------------------------
    | Registro                            |
    |-------------------------------------|
    | Confirme sus datos [y/n]            |
    ---------------------------------------
    
    Usuario: {username}
    Contraseña: {password}
    Email: {email}
    Rol: {"Administrador" if rol == "1" else "General"}
    
    Opción: """
    yn = input(menuYN)
    if yn == 'y':
        arg = str({"username": str(username), "password": str(password),
                   "email": str(email), "bloqueo": "0", "rol": "0"}).replace("'", '"').encode()
        # Se envian los datos al servicio
        sock.sendall(arg)
        # Espera la respuesta
        data = sock.recv(4096).decode()
        if (data == "-1"):
            print('Resgistrado correctamente')
            menuSULI()
        else:
            print("Error: " + data)
            menuSULI()
    else:
        print('Ya existe un usuario con ese nombre o hay un dato mal puesto')
        menuSU()

################################### INICIO DE SESION ########################################


def menuLI():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Se ponen los datos de la conexion con servidor
    server_address = ('localhost', 5002)
    # Intenta la conexion en caso de no conectarse el servicio no esta encendido o no disponible
    try:
        sock.connect(server_address)
    except:
        menuUN = """
            ---------------------------------------
            | Servicio no disponible              |
            ---------------------------------------
            """
        print(menuUN)
        menuSULI()
    username = None
    password = None
    # rol = 2 # Usuario general

    menuUN = """
    ---------------------------------------
    | Inicio de sesión                    |
    |-------------------------------------|
    | Ingresar nombre de usuario          |
    ---------------------------------------

    Usuario: """
    username = input(menuUN)

    menuPW = """
    ---------------------------------------
    | Inicio de sesión                    |
    |-------------------------------------|
    | Ingresar contraseña                 |
    ---------------------------------------
    
    Contraseña: """
    password = input(menuPW)

    arg = str({"username": str(username), "password": str(password)}
              ).replace("'", '"').encode()
    sock.sendall(arg)
    resp = sock.recv(4096).decode()
    if resp == "400":
        print("Error en servicio.")
        menuSULI()
    elif resp == "404":
        print("Datos invalidos o no existe.")
        menuSULI()
    else:
        data = resp.split(",")
        sesion["id"], sesion["username"], sesion["bloqueo"], sesion["rol"] = data[0], data[1], data[2], data[3]
        if data[3] == "0":
            menuUN = """
            ---------------------------------------
            | Inicio correcto                     |
            ---------------------------------------
            """
            print(menuUN)
            menuUser()
        elif data[3] == "1":
            menuUN = """
            ---------------------------------------
            | Buenas admin hermoso                |
            ---------------------------------------
            """
            print(menuUN)
            menuAdmin()

################################### USUARIOS ########################################


def menuUser():
    menuGD2 = """
    +-------------------------------------+
    | Usuario general                     |
    +-------------------------------------+
    | Consultar datos                     |
    | Elija una opción                    |
    +-------------------------------------+
    | 1) Estado de cuenta                 |
    | 2) Ver libros disponibles           |
    | 3) Reservar libros                  |
    | 4) Devoluciones Pendientes          |
    |                                     |
    | 0) Cerrar sesión                    |
    +-------------------------------------+
    
    Opción: """
    opcion = int(input(menuGD2))
    if opcion == 1:
        estado_cuenta()
        menuUser()
    if opcion == 2:
        mostrar_libros()
        menuUser()
    if opcion == 0:
        sesion["id"], sesion["username"], sesion["bloqueo"], sesion["rol"] = None, None, None, None
        menuSULI()
    else:
        print("Opcion mal puesta.")
        print("Presione enter para volver al menú.")
        input()
        menuUser()

################################### ADMIN ########################################


def menuAdmin():
    menuGD2 = """
    +-------------------------------------+
    | Admin general                       |
    +-------------------------------------+
    | Consultar datos                     |
    | Elija una opción                    |
    +-------------------------------------+
    | 1) Añadir libro                     |
    | 2) Actualizar cantidad de libro     |
    | 3) Eliminar libro                   |
    | 4) Estado de libros                 |
    |                                     |
    | 0) Cerrar sesión                    |
    +-------------------------------------+
    
    Opción: """
    opcion = int(input(menuGD2))

    if opcion == 1:
        anadir_libros()
        menuAdmin()

    if opcion == 2:
        modificar_libros()
        menuAdmin()

    if opcion == 3:
        eliminar_libros()
        menuAdmin()

    if opcion == 4:
        mostrar_libros()
        menuAdmin()

    if opcion == 0:
        sesion["id"], sesion["username"], sesion["bloqueo"], sesion["rol"] = None, None, None, None
        menuSULI()
    else:
        print("Opcion mal puesta.")
        menuAdmin()


################################### FUNCIONES ########################################
def atrasos_libros():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5004)
    # Intenta la conexion en caso de no conectarse el servicio no esta encendido o no disponible
    try:
        sock.connect(server_address)
    except:
        menuUN = """
            +-------------------------------------+
            | Servicio no disponible              |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
        if sesion["rol"] == "0":
            menuUser()
        elif sesion["rol"] == "1":
            menuAdmin()


def anadir_libros():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5005)
    nombre = None
    autor = None
    anio = None
    cantidad = None
    estado = "Disponible"
    genero = None

    menuUN = """
            +-------------------------------------+
            | Añadir libro                        |
            +-------------------------------------+
            | Ingresar nombre del libro           |
            +-------------------------------------+

            Nombre: """
    nombre = input(menuUN)
    menuUN = """
            +-------------------------------------+
            | Añadir libro                        |
            +-------------------------------------+
            | Ingresar autor del libro            |
            +-------------------------------------+

            Autor: """
    autor = input(menuUN)

    menuUN = """
            +-------------------------------------+
            | Añadir libro                        |
            +-------------------------------------+
            | Ingresar año del libro              |
            +-------------------------------------+

            Año: """
    anio = input(menuUN)
    try:
        if (int(anio) <= 1800 or int(anio) >= 2022):
            print("Año mal puesto")
            print("Presione Enter para continuar...")
            input()
            menuAdmin()
    except Exception as e:
        print("Ponga valores numericos")
        print("Presione Enter para continuar...")
        input()
        menuAdmin()

    menuUN = """
            +-------------------------------------+
            | Añadir libro                        |
            +-------------------------------------+
            | Ingresar cantidad libros            |
            +-------------------------------------+

            cantidad: """
    cantidad = input(menuUN)
    try:
        if (int(cantidad) < 0):
            print("Cantidad debe ser mayor a 0")
            print("Presione Enter para continuar...")
            input()
            menuAdmin()
    except Exception as e:
        print("Ponga valores numericos")
        print("Presione Enter para continuar...")
        input()
        menuAdmin()

    menuUN = """
            +-------------------------------------+
            | Añadir libro                        |
            +-------------------------------------+
            | Ingresar genero libro               |
            +-------------------------------------+

            genero: """
    genero = input(menuUN)
    # Intenta la conexion en caso de no conectarse el servicio no esta encendido o no disponible
    try:
        sock.connect(server_address)
    except:
        menuUN = """
            +-------------------------------------+
            | Servicio no disponible              |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
        if sesion["rol"] == "0":
            menuUser()
        elif sesion["rol"] == "1":
            menuAdmin()
   # Se tienen los valores y se hace añade el libro
    arg = str({"nombre": str(nombre), "autor": str(autor), "anio": anio, "cantidad": cantidad,
              "estado": str(estado), "genero": str(genero)}).replace("'", '"').encode()
    # Se mandan los datos al cliente
    sock.sendall(arg)
    # Se espera la respuesta del cliente
    resp = sock.recv(4096).decode()
    data = json.loads(resp)
    # Si la respuesta es 404 es algun error
    if data["status"] == "404":
        menuUN = """
            +-------------------------------------+
            | Error en el servicio                |
            +-------------------------------------+

            """
        print(menuUN)
        print(data["error"])
        print("Presione enter para volver al menú.")
        input()
        menuAdmin()
    elif data["status"] == "200":
        menuUN = """
            +-------------------------------------+
            | Registro de libro de forma correcta |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
        menuAdmin()


def modificar_libros():
    # Se crea el socket a utilizar
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Se pone la ip del servicio con el socket
    server_address = ('localhost', 5006)
    cantidad = None
    id_libro = None

    menuUN = """
            +-------------------------------------+
            | Modificar libro                     |
            +-------------------------------------+
            | Ingresar id del libro               |
            +-------------------------------------+

            nombre: """
    id_libro = input(menuUN)
    try:
        int(id_libro)
    except Exception as e:
        print("Ponga valores numericos")
        print("Presione Enter para continuar...")
        input()
        menuAdmin()
    menuUN = """
            +-------------------------------------+
            | Modificar Libro                     |
            +-------------------------------------+
            | Ingresar cantidad del libro         |
            +-------------------------------------+

            cantidad: """
    cantidad = input(menuUN)
    try:
        if (int(cantidad) < 0):
            print("Cantidad debe ser mayor a 0")
            print("Presione Enter para continuar...")
            input()
            menuAdmin()
    except Exception as e:
        print("Ponga valores numericos")
        print("Presione Enter para continuar...")
        input()
        menuAdmin()
    # Intenta la conexion en caso de no conectarse el servicio no esta encendido o no disponible
    try:
        sock.connect(server_address)
    except:
        menuUN = """
            ---------------------------------------
            | Servicio no disponible              |
            ---------------------------------------
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
        if sesion["rol"] == "0":
            menuUser()
        elif sesion["rol"] == "1":
            menuAdmin()

    # Se juntan los valores para enviarlos se hace el reemplazo y se encodea
    arg = str({"id_libro": id_libro, "cantidad": cantidad}
              ).replace("'", '"').encode()
    # Se manda al cliente los datos
    sock.sendall(arg)
    # Se espera la respuesta del cliente
    resp = sock.recv(4096).decode()
    # Si la respuesta es 404 es algun error
    if resp == "404":
        menuUN = """
            +-------------------------------------+
            | Error en el servicio                |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
    elif resp == "405":
        menuUN = """
            +-------------------------------------+
            | Datos erroneos                      |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
    else:
        menuUN = """
            +-------------------------------------+
            | Actualizacion correcta              |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()


def eliminar_libros():
    # Se crea el socket a utilizar
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Se pone la ip del servicio con el socket
    server_address = ('localhost', 5007)
    cantidad = None
    id_libro = None

    menuUN = """
            +-------------------------------------+
            | Modificar libro                     |
            +-------------------------------------+
            | Ingresar id del libro               |
            +-------------------------------------+

            nombre: """
    id_libro = input(menuUN)
    try:
        int(id_libro)
    except Exception as e:
        print("Ponga valores numericos")
        print("Presione Enter para continuar...")
        input()
        menuAdmin()
    # Intenta la conexion en caso de no conectarse el servicio no esta encendido o no disponible
    try:
        sock.connect(server_address)
    except:
        menuUN = """
            +-------------------------------------+
            | Servicio no disponible              |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
        if sesion["rol"] == "0":
            menuUser()
        elif sesion["rol"] == "1":
            menuAdmin()

    # Se juntan los valores para enviarlos se hace el reemplazo y se encodea
    arg = str({"id_libro": id_libro}
              ).replace("'", '"').encode()
    # Se manda al cliente los datos
    sock.sendall(arg)
    # Se espera la respuesta del cliente
    resp = sock.recv(4096).decode()
    # Si la respuesta es 404 es algun error
    if resp == "404":
        menuUN = """
            +-------------------------------------+
            | Error en el servicio                |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
        menuAdmin()
    elif resp == "405":
        menuUN = """
            +-------------------------------------+
            | Datos erroneos                      |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
    else:
        menuUN = """
            +-------------------------------------+
            | Eliminacion correcta                |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()


def estado_cuenta():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5008)
    # Intenta la conexion en caso de no conectarse el servicio no esta encendido o no disponible
    nombre = None
    menuUN = """
            +-------------------------------------+
            | Ver estado de la cuenta             |
            +-------------------------------------+
            | Ingresar nombre del usuario         |
            +-------------------------------------+

            nombre: """
    nombre = input(menuUN)
    try:
        sock.connect(server_address)
    except:
        menuUN = """
            +-------------------------------------+
            | Servicio no disponible              |
            +-------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
        if sesion["rol"] == "0":
            menuUser()
        elif sesion["rol"] == "1":
            menuAdmin()


def mostrar_libros():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5009)
    # Intenta la conexion en caso de no conectarse el servicio no esta encendido o no disponible
    try:
        sock.connect(server_address)
    except:
        menuUN = """
            +----------------------------------------+
            | Servicio no disponible                 |
            +----------------------------------------+
            """
        print(menuUN)
        print("Presione enter para volver al menú.")
        input()
        if sesion["rol"] == "0":
            menuUser()
        elif sesion["rol"] == "1":
            menuAdmin()
    # Se juntan los valores para enviarlos se hace el reemplazo y se encodea
    arg = str({"rol": sesion["rol"]}
              ).replace("'", '"').encode()
    # Se manda al cliente los datos
    sock.sendall(arg)
    # Se espera la respuesta del cliente
    data = sock.recv(4096).decode()
    data = json.loads(data)
    if data["status"] == "200":  # status 200 es el correcto
        if sesion["rol"] == "1":
            table = PrettyTable()
            table.field_names = ["id", "Nombre", "Cantidad", "Estado"]
            for row in data["data"]:
                table.add_row(row)
            print(table)
        elif sesion["rol"] == "0":
            table = PrettyTable()
            table.field_names = ["id", "Nombre",
                                 "Autor", "Genero", "Año"]
            for row in data["data"]:
                table.add_row(row)
            print(table)
        else:
            print("Id no reconocida: " + sesion["id"])
        print("Presione enter para volver al menú.")
        input()
    elif data["status"] == "404":
        print("Error en la consulta: "+data["error"])
    elif data["status"] == "401":
        print("Error en parametros")


################################### MAIN ########################################
if __name__ == "__main__":
    menuSULI()
