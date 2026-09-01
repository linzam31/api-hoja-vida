from flask import Flask
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
            "mensaje":"Base de datos conenctada"
        }

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
            "fotografia":"foto",
            "programa":"fotografia",
            "ficha":4444,
            "jornada":"nocturna"
        }
    ]
    
    return hojas_vida

if __name__ == '__main__':
    app.run(debug = True)