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

#registro
@app.route("/api/registro-hoja-vida", methods = ["POST"])
def registro_hoja_vida():
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)
    datos = request.json
    nuevo_correo = datos["correo"]
    
    # Consultar si el correo ya existe
    cursor.execute("SELECT correo FROM hojas_vida WHERE correo = %s", [nuevo_correo])
    consultar = cursor.fetchone()
    
    if consultar:
        cursor.close()
        conec.close()
        return {"Mensaje": "El correo ya existe"}, 400

    sql = """INSERT INTO hojas_vida (nombre, edad, ciudad, correo, fotografia, programa, ficha, jornada) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
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
    
    id_generado = cursor.lastrowid
    cursor.close()
    conec.close()
    return {"Mensaje": "Hoja de vida creada", "id": id_generado}, 21

#listar
@app.route("/api/hojas-vida")
def obtener_hojasvida():
    conec = conectar_bd()

    cursor = conec.cursor(dictionary=True) 
    cursor.execute("SELECT * from hojas_vida")

    hojas_vida = cursor.fetchall()
    cursor.close()
    conec.close()
    return hojas_vida


#BUSCAR HOJA DE VIDA POR ID
@app.route("/api/hojas-vida/<int:id>", methods=["GET"])
def obtener_hojasvidaid(id):
    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True) # Usamos dictionary para mapear columnas a JSON
    
    cursor.execute("SELECT * FROM hojas_vida WHERE id = %s", (id,))
    hoja_vida = cursor.fetchone()
    
    cursor.close()
    conec.close()
    
    if hoja_vida is None:
        return {"Mensaje": "Hoja de vida no encontrada"}, 404
        
    return {
        "Mensaje": "Hoja de vida encontrada",
        "datos": hoja_vida
    }

# ELIMINAR HOJA DE VIDA
@app.route("/api/eliminarhv/<int:id>", methods=["DELETE"])
def eliminar_hv(id):
    conec = conectar_bd()
    cursor = conec.cursor()
    
    # Verificar si el registro realmente existe antes de borrar
    cursor.execute("SELECT id FROM hojas_vida WHERE id = %s", (id,))
    existe = cursor.fetchone()
    
    if existe is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "La hoja de vida no existe"}, 404
        
    # Si existe, procedemos a eliminar
    cursor.execute("DELETE FROM hojas_vida WHERE id = %s", (id,))
    conec.commit()
    
    cursor.close()
    conec.close()
    return {"Mensaje": f"Hoja de vida con ID {id} eliminada correctamente"}

# ACTUALIZAR HOJA DE VIDA
@app.route("/api/actualizarhv/<int:id>", methods=["PUT"])
def actualizar_hv(id):
    conec = conectar_bd()
    cursor = conec.cursor()
    
    # Verificar si existe
    cursor.execute("SELECT id FROM hojas_vida WHERE id = %s", (id,))
    existe = cursor.fetchone()
    
    if existe is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "La hoja de vida no existe"}, 404
        
    datos = request.json
    
    # Consulta SQL para actualizar todos los campos modificables
    sql = """UPDATE hojas_vida 
             SET nombre=%s, edad=%s, ciudad=%s, correo=%s, fotografia=%s, programa=%s, ficha=%s, jornada=%s 
             WHERE id=%s"""
             
    valores = (
        datos["nombre"],
        datos["edad"],
        datos["ciudad"],
        datos["correo"],
        datos.get("fotografia"),
        datos["programa"],
        datos["ficha"],
        datos["jornada"],
        id
    )
    
    cursor.execute(sql, valores)
    conec.commit()
    
    cursor.close()
    conec.close()
    return {"Mensaje": f"Hoja de vida con ID {id} actualizada correctamente"}

if __name__ == '__main__':
    app.run(debug=True)
