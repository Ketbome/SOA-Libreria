import psycopg2
# Conexion a la base de datos mysql
conn = psycopg2.connect(
    host="localhost",
    database="biblioteca",
    user="postgres",
    password="0527"
)

# Crea un cursor para realizar consultas a la base de datos
cursor = conn.cursor()

# Ejecuta una consulta SQL
cursor.execute("SELECT * FROM usuarios")

# Obtiene todos los resultados de la consulta
results = cursor.fetchall()

# Procesa los resultados
for result in results:
    print(result)

# Cierra la conexión con la base de datos
conn.close()
