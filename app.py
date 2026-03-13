from flask import Flask, request, jsonify
from supabase import create_client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = Flask(__name__)

# Crear tarea
@app.route("/tareas", methods=["POST"])
def crear_tarea():
    data = request.get_json()
    titulo = data.get("titulo")
    descripcion = data.get("descripcion", "")
    estado = data.get("estado", "pendiente")

    tarea = {"titulo": titulo, "descripcion": descripcion, "estado": estado}
    supabase.table("tareas").insert(tarea).execute()

    return jsonify({"mensaje": "Tarea creada exitosamente"}), 201

# Consultar todas las tareas
@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    response = supabase.table("tareas").select("*").execute()
    return jsonify(response.data), 200

# Actualizar tarea por ID
@app.route("/tareas/<int:id>", methods=["PUT"])
def actualizar_tarea(id):
    data = request.get_json()
    supabase.table("tareas").update(data).eq("id", id).execute()
    return jsonify({"mensaje": "Tarea actualizada exitosamente"}), 200

# Eliminar tarea por ID
@app.route("/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    supabase.table("tareas").delete().eq("id", id).execute()
    return jsonify({"mensaje": "Tarea eliminada exitosamente"}), 200

if __name__ == "__main__":
    app.run(debug=True)
