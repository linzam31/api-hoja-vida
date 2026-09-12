from flask import Flask, request
from database import conectar_bd
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["POST", "GET", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type"]}})

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
@app.route("/api/registro-hoja-vida", methods=["POST"])
def registro_hoja_vida():
    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()
    
    # 1. Extraer los textos planos reales de forma segura cuidando la anidación de React
    if isinstance(datos.get("correo"), dict):
        # Si viene anidado (el error de React), los extraemos desde el sub-diccionario
        sub_diccionario = datos["correo"]
        nuevo_correo = sub_diccionario.get("correo")
        nombre = sub_diccionario.get("nombre")
        edad = sub_diccionario.get("edad")
        ciudad = sub_diccionario.get("ciudad")
        programa = sub_diccionario.get("programa")
        ficha = sub_diccionario.get("ficha")
        jornada = sub_diccionario.get("jornada")
        fotografia = sub_diccionario.get("foto")  # En el print decía 'foto'
    else:
        # Si en algún momento viene limpio, los extrae directo
        nuevo_correo = datos.get("correo")
        nombre = datos.get("nombre")
        edad = datos.get("edad")
        ciudad = datos.get("ciudad")
        programa = datos.get("programa")
        ficha = datos.get("ficha")
        jornada = datos.get("jornada")
        fotografia = datos.get("fotografia")

    # 2. Validar duplicado con la variable limpia
    cursor.execute("SELECT correo FROM hojas_vida WHERE correo = %s", (nuevo_correo,))
    existe = cursor.fetchone()
    
    if existe:
        cursor.close()
        conec.close()
        return {"Mensaje": "El correo ya está registrado"}, 400

    # 3. Insertar usando únicamente variables limpias (Strings puros)
    sql = """INSERT INTO hojas_vida (nombre, edad, ciudad, correo, fotografia, programa, ficha, jornada) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
             
    valor = (
        nombre,
        edad,
        ciudad,
        nuevo_correo,
        fotografia,
        programa,
        ficha,
        jornada
    )
    
    cursor.execute(sql, valor)
    conec.commit()
    
    id_generado = cursor.lastrowid
    cursor.close()
    conec.close()
    
    return {"Mensaje": "Hoja de vida registrada con éxito", "id": id_generado}, 201


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


#Consultar hoja de vida por ID
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

# eliminar hoja de vida
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

# actualizar hoja de vida
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




#------------ ESTUDIOS -------------

#Consultar estudios de la hoja de vida
@app.route("/api/estudios-hoja-vida/<int:id>", methods=["GET"])
def estudios_hoja_vida(id):
    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)

    sql = """
            SELECT h.id AS hoja_vida_id, e.id AS id_estudio, e.nivel, e.institucion, e.titulo, e.anio_graduacion
            FROM hojas_vida h
            INNER JOIN estudios e ON h.id = e.hoja_vida_id
            WHERE h.id = %s
          
          """
    cursor.execute(sql, (id,))
    datos = cursor.fetchall()
          
    cursor.close()
    conec.close()
    
    if not datos:
        return {"Mensaje": "No se encontró la hoja de vida"}, 404
    if datos[0]['id_estudio'] is None:
        return {"Mensaje": "No se encontraron estudios para esta hoja de vida"}, 404
    return datos, 200


#registro 
@app.route("/api/registro-estudios/<int:id>", methods = ["POST"])
def registro_estudios(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)
    datos = request.json
    
    cursor.execute("SELECT id FROM hojas_vida WHERE id = %s", (id,))
    validar = cursor.fetchone()
    
    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "El id ingresado no existe"}, 404

    sql = """INSERT INTO estudios (hoja_vida_id, nivel, institucion, titulo, anio_graduacion) 
             VALUES (%s, %s, %s, %s, %s)"""
    valor = (
        id,
        datos["nivel"],
        datos["institucion"],
        datos["titulo"],
        datos["anio_graduacion"]
    )
    
    cursor.execute(sql, valor)
    conec.commit()
    
    id_generado = cursor.lastrowid
    cursor.close()
    conec.close()
    return {"Mensaje": "Estudio creado", "id": id_generado}, 201


#consultar estudios por id
@app.route("/api/estudios/<int:id>", methods=["GET"])
def consultar_estudio(id):
    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM estudios WHERE id = %s", (id,))
    estudio = cursor.fetchone()
    
    cursor.close()
    conec.close()
    
    if estudio is None:
        return {"Mensaje": "Estudio no encontrado"}, 404
        
    return {
        "Mensaje": "Estudio encontrado",
        "datos": estudio
    }


# actualizar estudio
@app.route("/api/actualizar-estudio/<int:id>", methods=["PUT"])
def actualizar_estudio(id):
    conec = conectar_bd()
    cursor = conec.cursor()
    
    cursor.execute("SELECT id FROM estudios WHERE id = %s", (id,))
    existe = cursor.fetchone()
    
    if existe is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "El estudio no existe"}, 404
        
    datos = request.json
    
    sql = """UPDATE estudios 
             SET nivel=%s, institucion=%s, titulo=%s, anio_graduacion=%s 
             WHERE id=%s"""
             
    valores = (
        datos["nivel"],
        datos["institucion"],
        datos["titulo"],
        datos["anio_graduacion"],
        id
    )
    
    cursor.execute(sql, valores)
    conec.commit()
    
    cursor.close()
    conec.close()

    return {"Mensaje": f"Estudio con ID {id} actualizado correctamente"}


# eliminar estudio
@app.route("/api/eliminar-estudio/<int:id>", methods=["DELETE"])
def eliminar_estudio(id):
    conec = conectar_bd()
    cursor = conec.cursor()
    
    cursor.execute("SELECT id FROM estudios WHERE id = %s", (id,))
    existe = cursor.fetchone()
    
    if existe is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "El estudio no existe"}, 404
        
    cursor.execute("DELETE FROM estudios WHERE id = %s", (id,))
    conec.commit()
    
    cursor.close()
    conec.close()
    return {"Mensaje": f"Estudio con ID {id} eliminado correctamente"}




#------------ EXPERIENCIA LABORAL -------------

#registro experiencia laboral
@app.route("/api/registro-experiencia/<int:id>", methods = ["POST"])
def registro_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)
    datos = request.json
    
    cursor.execute("SELECT id FROM hojas_vida WHERE id = %s", (id,))
    validar = cursor.fetchone()
    
    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "El id ingresado no existe"}, 404

    sql = """INSERT INTO experiencias (hoja_vida_id, empresa, cargo, tiempo, funciones) 
             VALUES (%s, %s, %s, %s, %s)"""
    valor = (
        id,
        datos["empresa"],
        datos["cargo"],
        datos["tiempo"],
        datos["funciones"]
    )
    
    cursor.execute(sql, valor)
    conec.commit()
    
    id_generado = cursor.lastrowid
    cursor.close()
    conec.close()
    return {"Mensaje": "Experiencia laboral creada", "id": id_generado}, 201


#Consultar experiencias laborales de una hoja de vida
@app.route("/api/experiencias-hv/<int:id>", methods=["GET"])
def experiencias_hoja_vida(id):
    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)
    sql = """
            SELECT h.id AS hoja_vida_id, e.id AS id_experiencia, e.empresa, e.cargo, e.tiempo, e.funciones
            FROM hojas_vida h
            INNER JOIN experiencias e ON h.id = e.hoja_vida_id
            WHERE h.id = %s
          
          """
    cursor.execute(sql, (id,))
    datos = cursor.fetchall()
          
    cursor.close()
    conec.close()
    
    if not datos:
        return {"Mensaje": "No se encontró la hoja de vida"}, 404
    if datos[0]['id_experiencia'] is None:
        return {"Mensaje": "No se encontraron experiencias para esta hoja de vida"}, 404
    return datos, 200


#consultar experiencias por id
@app.route("/api/experiencias/<int:id>", methods=["GET"])
def consultar_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM experiencias WHERE id = %s", (id,))
    experiencia = cursor.fetchone()
    
    cursor.close()
    conec.close()
    
    if experiencia is None:
        return {"Mensaje": "Experiencia no encontrada"}, 404
        
    return {
        "Mensaje": "Experiencia encontrada",
        "datos": experiencia
    }


# actualizar experiencia
@app.route("/api/actualizar-experiencia/<int:id>", methods=["PUT"])
def actualizar_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor()
    
    cursor.execute("SELECT id FROM experiencias WHERE id = %s", (id,))
    existe = cursor.fetchone()
    
    if existe is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "La experiencia no existe"}, 404
        
    datos = request.json
    
    sql = """UPDATE experiencias 
             SET empresa=%s, cargo=%s, tiempo=%s, funciones=%s 
             WHERE id=%s"""
             
    valores = (
        datos["empresa"],
        datos["cargo"],
        datos["tiempo"],
        datos["funciones"],
        id
    )
    
    cursor.execute(sql, valores)
    conec.commit()
    
    cursor.close()
    conec.close()

    return {"Mensaje": f"Experiencia con ID {id} actualizada correctamente"}


# eliminar experiencia
@app.route("/api/eliminar-experiencia/<int:id>", methods=["DELETE"])
def eliminar_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor()
    
    cursor.execute("SELECT id FROM experiencias WHERE id = %s", (id,))
    existe = cursor.fetchone()
    
    if existe is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "La experiencia no existe"}, 404
        
    cursor.execute("DELETE FROM experiencias WHERE id = %s", (id,))
    conec.commit()
    
    cursor.close()
    conec.close()
    return {"Mensaje": f"Experiencia con ID {id} eliminada correctamente"}


#----------------HABILIDADES-----------------

#registro habilidades
@app.route("/api/registro-habilidades/<int:id>", methods = ["POST"])
def registro_habilidades(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)
    datos = request.json
    
    cursor.execute("SELECT id FROM experiencias WHERE id = %s", (id,))
    validar = cursor.fetchone()
    
    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "El id ingresado no existe"}, 404

    sql = """INSERT INTO habilidades (experiencias_id, nombre) 
             VALUES (%s, %s)"""
    valor = (
        id,
        datos["nombre"]
    )
    
    cursor.execute(sql, valor)
    conec.commit()
    
    id_generado = cursor.lastrowid
    cursor.close()
    conec.close()
    return {"Mensaje": "Habilidad creada", "id": id_generado}, 201


# Consultar habilidades de una experiencia laboral
@app.route("/api/habilidades-exp/<int:id>", methods=["GET"])
def consultar_habilidades_experiencia(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)

    cursor.execute("SELECT id FROM experiencias WHERE id = %s", (id,))
    validar = cursor.fetchone()

    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "La experiencia no existe"}, 404

    cursor.execute("SELECT nombre FROM habilidades WHERE experiencias_id = %s", (id,))
    habilidades = cursor.fetchall()

    cursor.close()
    conec.close()

    return {"Mensaje": "Habilidades encontradas", "datos": habilidades}, 200


#actualizar habilidad
@app.route("/api/actualizar-habilidad/<int:id>", methods=["PUT"])
def actualizar_habilidad(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)

    cursor.execute("SELECT id FROM habilidades WHERE id = %s", (id,))
    validar = cursor.fetchone()

    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "La habilidad no existe"}, 404

    datos = request.json
    nuevo_nombre = datos["nombre"]

    cursor.execute("UPDATE habilidades SET nombre = %s WHERE id = %s", (nuevo_nombre, id))
    conec.commit()

    cursor.close()
    conec.close()

    return {"Mensaje": f"Habilidad con ID {id} actualizada correctamente"}, 200


#eliminar habilidad
@app.route("/api/eliminar-habilidad/<int:id>", methods=["DELETE"])
def eliminar_habilidad(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)

    cursor.execute("SELECT id FROM habilidades WHERE id = %s", (id,))
    validar = cursor.fetchone()

    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "La habilidad no existe"}, 404

    cursor.execute("DELETE FROM habilidades WHERE id = %s", (id,))
    conec.commit()

    cursor.close()
    conec.close()

    return {"Mensaje": f"Habilidad con ID {id} eliminada correctamente"}, 200


#-----------------CURSOS-----------------

#registro cursos
@app.route("/api/registro-cursos/<int:id>", methods = ["POST"])
def registro_cursos(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)
    datos = request.json
    
    cursor.execute("SELECT id FROM hojas_vida WHERE id = %s", (id,))
    validar = cursor.fetchone()
    
    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "El id ingresado no existe"}, 404

    sql = """INSERT INTO cursos (hoja_vida_id, nombre) 
             VALUES (%s, %s)"""
    valor = (
        id,
        datos["nombre"]
    )
    
    cursor.execute(sql, valor)
    conec.commit()
    
    id_generado = cursor.lastrowid
    cursor.close()
    conec.close()
    return {"Mensaje": "Curso creado", "id": id_generado}, 201


# Consultar cursos de una hoja de vida
@app.route("/api/cursos-hv/<int:id>", methods=["GET"])
def consultar_cursos(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)

    cursor.execute("SELECT id FROM hojas_vida WHERE id = %s", (id,))
    validar = cursor.fetchone()

    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "La hoja de vida no existe"}, 404

    cursor.execute("SELECT nombre FROM cursos WHERE hoja_vida_id = %s", (id,))
    cursos = cursor.fetchall()

    cursor.close()
    conec.close()

    return {"Mensaje": "Cursos encontrados", "datos": cursos}, 200


# Consultar curso por ID
@app.route("/api/curso/<int:id>", methods=["GET"])
def consultar_curso(id):
    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cursos WHERE id = %s", (id,))
    curso = cursor.fetchone()

    cursor.close()
    conec.close()

    if curso is None:
        return {"Mensaje": "Curso no encontrado"}, 404

    return {
        "Mensaje": "Curso encontrado",
        "datos": curso
    }


# Actualizar curso
@app.route("/api/actualizar-curso/<int:id>", methods=["PUT"])
def actualizar_curso(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)

    cursor.execute("SELECT id FROM cursos WHERE id = %s", (id,))
    validar = cursor.fetchone()

    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "El curso no existe"}, 404

    datos = request.json
    nuevo_nombre = datos["nombre"]

    cursor.execute("UPDATE cursos SET nombre = %s WHERE id = %s", (nuevo_nombre, id))
    conec.commit()

    cursor.close()
    conec.close()

    return {"Mensaje": f"Curso con ID {id} actualizado correctamente"}, 200


# Eliminar curso
@app.route("/api/eliminar-curso/<int:id>", methods=["DELETE"])
def eliminar_curso(id):
    conec = conectar_bd()
    cursor = conec.cursor(buffered=True)

    cursor.execute("SELECT id FROM cursos WHERE id = %s", (id,))
    validar = cursor.fetchone()

    if validar is None:
        cursor.close()
        conec.close()
        return {"Mensaje": "El curso no existe"}, 404

    cursor.execute("DELETE FROM cursos WHERE id = %s", (id,))
    conec.commit()

    cursor.close()
    conec.close()

    return {"Mensaje": f"Curso con ID {id} eliminado correctamente"}, 200


#-----------------HOJA DE VIDA-----------------
@app.route("/api/hoja-vida-completa/<int:id>", methods=["GET"])
def obtener_hoja_vida_completa(id):
    conec = conectar_bd()
    # Usamos dictionary=True para que nos entregue las columnas con sus nombres
    cursor = conec.cursor(dictionary=True)
    
    sql = """
        SELECT 
            h.id AS id_hoja, h.nombre, h.edad, h.ciudad, h.correo, h.fotografia, h.programa, h.ficha, h.jornada,
            e.id AS id_estudio, e.nivel, e.institucion, e.titulo, e.anio_graduacion, 
            c.id AS id_curso, c.nombre AS nombre_curso, 
            ex.id AS id_experiencia, ex.empresa, ex.cargo, ex.tiempo, ex.funciones, 
            ha.id AS id_habilidad, ha.nombre AS nombre_habilidad
        FROM hojas_vida h 
        LEFT JOIN estudios e ON h.id = e.hoja_vida_id
        LEFT JOIN cursos c ON h.id = c.hoja_vida_id 
        LEFT JOIN experiencias ex ON h.id = ex.hoja_vida_id 
        LEFT JOIN habilidades ha ON ha.experiencias_id = ex.id 
        WHERE h.id = %s
    """
    cursor.execute(sql, (id,))
    filas = cursor.fetchall()
    
    cursor.close()
    conec.close()
    
    # 1. Si no hay filas, la hoja de vida no existe
    if not filas:
        return {"Mensaje": "No se encontró la hoja de vida"}, 404
        
    # 2. Estructurar el objeto principal con los datos del usuario (tomados de la primera fila)
    primera_fila = filas[0]
    hoja_vida = {
        "id": primera_fila["id_hoja"],
        "nombre": primera_fila["nombre"],
        "edad": primera_fila["edad"],
        "ciudad": primera_fila["ciudad"],
        "correo": primera_fila["correo"],
        "fotografia": primera_fila["fotografia"],
        "programa": primera_fila["programa"],
        "ficha": primera_fila["ficha"],
        "jornada": primera_fila["jornada"],
        "estudios": [],
        "cursos": [],
        "experiencias": [],
        "habilidades": []
    }
    
    # Listas auxiliares para controlar qué IDs ya agregamos y evitar duplicados
    estudios_agregados = set()
    cursos_agregados = set()
    experiencias_agregadas = set()
    habilidades_agregadas = set()
    
    # 3. Recorrer todas las filas para extraer los datos de las tablas relacionadas
    for fila in filas:
        # Agrupar Estudios
        if fila["id_estudio"] and fila["id_estudio"] not in estudios_agregados:
            hoja_vida["estudios"].append({
                "id": fila["id_estudio"],
                "nivel": fila["nivel"],
                "institucion": fila["institucion"],
                "titulo": fila["titulo"],
                "anio_graduacion": fila["anio_graduacion"]
            })
            estudios_agregados.add(fila["id_estudio"])
            
        # Agrupar Cursos
        if fila["id_curso"] and fila["id_curso"] not in cursos_agregados:
            hoja_vida["cursos"].append({
                "id": fila["id_curso"],
                "nombre_curso": fila["nombre_curso"]
            })
            cursos_agregados.add(fila["id_curso"])
            
        # Agrupar Experiencias
        if fila["id_experiencia"] and fila["id_experiencia"] not in experiencias_agregadas:
            hoja_vida["experiencias"].append({
                "id": fila["id_experiencia"],
                "empresa": fila["empresa"],
                "cargo": fila["cargo"],
                "tiempo": fila["tiempo"],
                "funciones": fila["funciones"]
            })
            experiencias_agregadas.add(fila["id_experiencia"])
            
        # Agrupar Habilidades
        if fila["id_habilidad"] and fila["id_habilidad"] not in habilidades_agregadas:
            hoja_vida["habilidades"].append({
                "id": fila["id_habilidad"],
                "nombre_habilidad": fila["nombre_habilidad"]
            })
            habilidades_agregadas.add(fila["id_habilidad"])
            
    return hoja_vida, 200



if __name__ == '__main__':
    app.run(debug=True)