#import os
#import time
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
#from werkzeug.utils import secure_filename
from conector import Conector
from usuarios import Usuarios


conexion = Conector(host='127.0.0.1', user='root', password='root', database='miapp')
usuarios = Usuarios(conexion)

api_headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhODViZTJjYWY5MjUzOWVmMDM0NzA1ODFhMWQ1ZTAzMSIsInN1YiI6IjY0ZTY4ZDQyYzYxM2NlMDEwYjhiYzc1ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AzcehxudafYj4U2pzKNuWxw8BZLJJFK_sVXO_Bjg6QE'
}

app = Flask(__name__)
app.secret_key = 'CLAVE_PRIVADA'

app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')

CORS(app)  # Esto habilitará CORS para todas las rutas

# Carpeta para guardar las imagenes.
RUTA_DESTINO = '/static/imagenes/'



#-------------------------------------------------------------------------------
# Pagina principal
#-------------------------------------------------------------------------------
@app.route("/", defaults={"seccion":"en_cartelera", "pagina": 1}, methods=["GET"])
@app.route("/<seccion>", defaults={"pagina": 1}, methods=["GET"])
@app.route("/<seccion>/<int:pagina>", methods=["GET"])
def index(seccion, pagina):
    usuario = session.get('nombre')
    resultado = api_peliculas(seccion, pagina)
    return render_template("index.html", usuario=usuario, seccion=seccion, pagina=pagina, resultado=resultado)


#-------------------------------------------------------------------------------
# Buscador
#-------------------------------------------------------------------------------
@app.route("/buscar", methods=["GET"])
def buscar():
    usuario = session.get('nombre')
    buscar = request.args.get('query', '')
    pagina = request.args.get('pagina', 1)
    resultado = api_peliculas_buscar(buscar, pagina)
    return render_template("index.html", usuario=usuario, resultado=resultado, buscar=buscar, pagina=pagina)


#-------------------------------------------------------------------------------
# Pagina de contacto
#-------------------------------------------------------------------------------
@app.route("/contacto", methods=["GET"])
def contacto():
    return render_template("contacto.html")


#-------------------------------------------------------------------------------
# Pagina de logueo
#-------------------------------------------------------------------------------
@app.route('/ingresar', methods=['GET', 'POST'])
def login():
    error = ''
    email = ''
    password = ''

    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']

            usuario = usuarios.login(email, password)

            if usuario:
                return redirect(url_for('index'))
        
        error = 'Credenciales inválidas.'

    return render_template('ingresar.html', mensaje=error, email=email, password=password)


#-------------------------------------------------------------------------------
# Pagina de deslogueo
#-------------------------------------------------------------------------------
@app.route('/salir', methods=['GET', 'POST'])
def logout():
    usuarios.logout()
    return redirect(url_for('index'))


#-------------------------------------------------------------------------------
# Pagina de registro
#-------------------------------------------------------------------------------
@app.route('/registro', methods=['GET', 'POST'])
def register():
    error = ''
    nombre = ''
    email = ''
    password = ''
    password2 = ''

    if request.method == 'POST':
        if 'email' in request.form and 'nombre' in request.form and 'password' in request.form:
            email = request.form['email']
            nombre = request.form['nombre']
            password = request.form['password']
            password2 = request.form['password2']

            usuario = usuarios.register(nombre, email, password)

            if usuario:
                return redirect(url_for('index'))
        
        error = 'Error al registrarse.'

    return render_template('registro.html', mensaje=error, nombre=nombre, email=email, password=password, password2=password2)


#-------------------------------------------------------------------------------
# Detalle de película
#-------------------------------------------------------------------------------
@app.route("/detalle", methods=["GET"])
def detalle_pelicula():
    usuario = session.get('nombre')
    respuesta = api_detalle_pelicula(request.args.get('id'))
    poster = request.args.get('path')
    return render_template("detalle.html", usuario=usuario, respuesta=respuesta, poster=poster)


#-------------------------------------------------------------------------------
# Detalle de coleccion (saga)
#-------------------------------------------------------------------------------
@app.route("/coleccion", methods=["GET"])
def coleccion_peliculas():
    usuario = session.get('nombre')
    respuesta = api_detalle_coleccion(request.args.get('id'))
    poster = request.args.get('path')
    return render_template("coleccion.html", usuario=usuario, respuesta=respuesta, poster=poster)


#-------------------------------------------------------------------------------
# API - Lista de peliculas
#-------------------------------------------------------------------------------
@app.route("/api/peliculas/<seccion>", defaults={"pagina": 1, "buscar":""}, methods=["GET"])
@app.route("/api/peliculas/<seccion>/<int:pagina>", methods=["GET"])
def api_peliculas(seccion, pagina):
    if seccion=="en_cartelera":
        seccion = "now_playing"
    elif seccion=="populares":
        seccion = "popular"
    elif seccion=="top":
        seccion = "top_rated"
    elif seccion=="proximamente":
        seccion = "upcoming"

    respuesta = requests.get(f"https://api.themoviedb.org/3/movie/{seccion}?language=en&page={pagina}", headers=api_headers)
    return respuesta.json()


#-------------------------------------------------------------------------------
# API - Lista de peliculas
#-------------------------------------------------------------------------------
@app.route("/api/buscar_pelicula/<query>/<pagina>", methods=["GET"])
def api_peliculas_buscar(query, pagina):
    respuesta = requests.get(f"https://api.themoviedb.org/3/search/movie?query='{query}'&language=en&page={pagina}", headers=api_headers)
    return respuesta.json()


#-------------------------------------------------------------------------------
# API - Detalle de pelicula
#-------------------------------------------------------------------------------
@app.route("/api/pelicula/<int:id>", methods=["GET"])
def api_detalle_pelicula(id):
    respuesta = {}
    respuesta["detalle"] = requests.get(f"https://api.themoviedb.org/3/movie/{id}?language=es-AR", headers=api_headers).json()
    respuesta["videos"] = requests.get(f"https://api.themoviedb.org/3/movie/{id}/videos?language=es-AR", headers=api_headers).json()["results"]
    respuesta["reparto"] = requests.get(f"https://api.themoviedb.org/3/movie/{id}/credits?language=es-AR", headers=api_headers).json()
    return respuesta


#-------------------------------------------------------------------------------
# API - Detalle de coleccion (saga)
#-------------------------------------------------------------------------------
@app.route("/api/coleccion/<int:id>", methods=["GET"])
def api_detalle_coleccion(id):
    respuesta = requests.get(f"https://api.themoviedb.org/3/collection/{id}", headers=api_headers)
    return respuesta.json()


#-------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
