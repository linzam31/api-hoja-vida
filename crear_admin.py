from werkzeug.security import (generate_password_hash, check_password_hash)
from flask import Flask, request
from flask_cors import CORS
from database import conectar_bd
import os
from getpass import getpass



def crear_administrador():
    nombre = input("Ingresar nombre del rol reclutador: ")
    correo = input("Ingresar correo del rol reclutador: ")
    password = getpass("Contraseña: ")


    if len(password) < 8:
        print("La contraseña debe tener mínimo 8 caracteres")
        return

    conec = conectar_bd()
    cursor = conec.cursor()

    try:
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
        existente = cursor.fetchone()

        if existente:
            print("Este correo ya está registrado")
            return

        #Cifrar contraseña 
        password_hash = generate_password_hash(password)

        sql = """INSERT INTO usuarios (nombre, correo, password, rol, estado) VALUES (%s, %s, %s, 'reclutador', 1)"""

        cursor.execute (sql,(nombre, correo, password_hash))

        conec.commit()
        print ("Reclutador creado correctamente")

    except Exception as error:
        conec.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conec.close()

if __name__ == "__main__":
    crear_administrador()


