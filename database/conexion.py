import os
import psycopg

conexion = psycopg.connect(

    host=os.getenv("DB_HOST"),

    dbname=os.getenv("DB_NAME"),

    user=os.getenv("DB_USER"),

    password=os.getenv("DB_PASSWORD")

)

cursor = conexion.cursor()

print("PostgreSQL conectado 😎")