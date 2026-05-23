import psycopg

conexion = psycopg.connect(

    host="localhost",

    dbname="refugio",

    user="postgres",

    password="123456"

)

cursor = conexion.cursor()

print("Conexion exitosa 😎")