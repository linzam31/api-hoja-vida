from flask import Flask, request
from database import conectar_bd

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Api hoja de vida funcionamiento"

@app.route("/probar")
def probar_bd():
    conec = conectar_bd()
    if conec.is_connected():
        conec.close()
       
        return {
            "mensaje":"database conectada"
        }

@app.route("/api/registro-hoja-vida", methods = ["POST"])
def registro_hoja_vida():
    conec = conectar_bd()
    # SOLUCIÓN: Agregamos buffered=True para evitar el error de resultados no leídos
    cursor = conec.cursor(buffered=True) 
    datos = request.json
   
    nuevo_correo = datos["correo"]
   
    # Consultar si el correo ya existe
    cursor.execute("SELECT correo FROM hojas_vida WHERE correo = %s", [nuevo_correo])
    consultar = cursor.fetchone()
   
    if consultar:
        cursor.close()
        conec.close()
        return {"Mensaje": "El correo ya existe"}
       
    sql = """INSERT INTO hojas_vida (nombre, edad, ciudad, correo, fotografia, programa, ficha, jornada) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    
    # CORRECCIÓN: Cambiado el último 'programa' por 'jornada'
    valor = (
        datos["nombre"],
        datos["edad"],
        datos["ciudad"],
        datos["correo"],
        datos.get("fotografia"),
        datos["programa"],
        datos["ficha"],
        datos["jornada"] 
    )
   
    cursor.execute(sql, valor)
    conec.commit()
   
    # Manejo del id de la hoja de vida
    id_generado = cursor.lastrowid
   
    cursor.close()
    conec.close()
   
    return {"Mensaje": "Hoja de vida creada", "id": id_generado}


@app.route("/api/hojas-vida/<int:id>")
def obtener_hojasvidaid(id):
    return{
        "Mensaje":"Hoja de vida encontrada","id":id
    }

@app.route("/api/hojas-vida")
def obtener_hojasvida():
    conec = conectar_bd()
    # Usamos dictionary=True para que devuelva los datos como diccionarios en vez de tuplas
    cursor = conec.cursor()
    
    # Consultamos todos los campos de la tabla
    cursor.execute("SELECT * from hojas_vida")
    hojas_vida = cursor.fetchall()
    
    cursor.close()
    conec.close()
    
    # Flask convertirá automáticamente la lista de diccionarios a formato JSON
    return hojas_vida

if __name__ == '__main__':
    app.run(debug=True)
