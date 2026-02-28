from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)

FASTAPI_URL = "http://localhost:5000/v1/usuarios"
app.secret_key = "secreto_seguro"

@app.route('/')
def index():
    usuarios = []
    try:
        respuesta = requests.get(f"{FASTAPI_URL}/0")
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            usuarios = datos.get("data", [])
        else:
            flash("Error al obtener usuarios", "warning")
            
    except requests.exceptions.ConnectionError:
        flash("No se pudo conectar con la API. ¿Está encendida?", "danger")

    return render_template('index.html', usuarios=usuarios)

@app.route('/guardar', methods=['POST'])
def guardar():
    id_usuario = request.form['id']
    nombre = request.form['nombre']
    edad = request.form['edad']

    nuevo_usuario = {
        "id": id_usuario,
        "nombre": nombre,
        "edad": edad
    }

    try:
        respuesta = requests.post(f"{FASTAPI_URL}/{id_usuario}", json=nuevo_usuario)

        if respuesta.status_code == 200:
            flash("Usuario agregado correctamente", "success")
        elif respuesta.status_code == 400:
            mensaje = respuesta.json().get('detail', 'Error desconocido')
            flash(f"Error: {mensaje}", "warning")
            
    except requests.exceptions.ConnectionError:
        flash("Error de conexión con la API", "danger")

    return redirect(url_for('index'))

@app.route('/borrar/<id>')
def borrar(id):
    try:
        respuesta = requests.delete(f"{FASTAPI_URL}/{id}")
        
        if respuesta.status_code == 200:
            flash(f"Usuario {id} eliminado", "info")
        else:
            flash("No se pudo eliminar el usuario", "warning")
            
    except requests.exceptions.ConnectionError:
        flash("Error de conexión", "danger")

    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(port=5010, debug=True)    