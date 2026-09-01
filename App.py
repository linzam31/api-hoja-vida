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
            "mensaje":"Base de datos conectada"
        }

@app.route("/api/registro-hoja-vida", methods = ["POST"])
def registro_hoja_vida():
    conec = conectar_bd()
    cursor = conec.cursor()
    datos = request.json
    correo_nuevo= datos ["correo"]
    
    #consultar si el correo ya existe
    cursor.execute("SELECT correo from hojas_vida WHERE correo = %s", (correo_nuevo))
    consultar = cursor.fetchone()
        
    if consultar:
        cursor.close
        conec.close()
        return("mensaje":"el correo ya existe")
    else:
        ("mensaje":"hoja de vida creada")
        sql = """INSERT INTO hojas_vida(nombre,edad,ciudad,correo,fotografia,programa,ficha,jornada) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        valor = (datos ["nombre"],
                datos ["edad"],
                datos ["ciudad"],
                datos ["correo"],
                datos.get ("fotografia"),
                datos ["programa"],
                datos ["ficha"],
                datos ["jornada"])
    
    cursor.execute(sql,valor)
    conec.commit()
    
    id_generado = cursor.lastrowid
    
    cursor.close()
    conec.close()
    
    return{"mensaje":"hoja de vida creada", "id": id_generado}
    

@app.route("/api/hojas-vida/<int:id>")
def obtener_hojasvidaid(id):
    return{
        "Mensaje":"Hoja de vida encontrada","id":id
    }

@app.route("/api/hojas-vida")
def obtener_hojasvida():
    #return{
    #    "mensaje":"Listado de hojas de vida"
    #}
    hojas_vida =[
        {
            "id": 1,
            "nombre":"Low",
            "edad": 36,
            "ciudad":"nuevo mundo",
            "correo":"low@gmail.com",
            "fotografia":"foto",
            "programa":"ADSO",
            "ficha":2222,
            "jornada":"diurna"
        },
        {
            "id": 2,
            "nombre":"Usop",
            "edad": 27,
            "ciudad":"nuevomundo",
            "correo":"usop@gmail.com",
            "fotografia":"foto",
            "programa":"fotografia",
            "ficha":4444,
            "jornada":"nocturna"
        }
    ]
    
    return hojas_vida

if __name__ == '__main__':
    app.run(debug = True)