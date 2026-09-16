import mysql.connector

def conectar_bd():
    conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "hoja_vida"
    )
    
    return conexion