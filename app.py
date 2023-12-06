import os
import time
import requests
from flask import Flask, request, session, render_template, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from conector import Conector
from usuarios import Usuarios

#conexion = Conector(host='127.0.0.1', user='root', password='root', database='miapp')
conexion = Conector(host='CepiPerez.mysql.pythonanywhere-services.com', user='CepiPerez', password='codoacodo2023', database='CepiPerez$codoacodo')
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
#RUTA_DESTINO = './static/imagenes/'
RUTA_DESTINO = '/home/CepiPerez/mysite/static/imagenes/'


#-------------------------------------------------------------------------------
# Pagina principal
#-------------------------------------------------------------------------------
@app.route("/", defaults={"seccion":"en_cartelera", "pagina": 1}, methods=["GET"])
@app.route("/<seccion>", defaults={"pagina": 1}, methods=["GET"])
@app.route("/<seccion>/<int:pagina>", methods=["GET"])
def index(seccion, pagina):
    usuario = session.get('nombre')
    avatar = session.get('avatar')
    resultado = api_peliculas(seccion, pagina)
    return render_template("index.html", usuario=usuario, avatar=avatar, seccion=seccion, pagina=pagina, resultado=resultado)


#-------------------------------------------------------------------------------
# Buscador
#-------------------------------------------------------------------------------
@app.route("/buscar", methods=["GET"])
def buscar():
    usuario = session.get('nombre')
    avatar = session.get('avatar')
    buscar = request.args.get('query', '')
    pagina = request.args.get('pagina', 1)
    resultado = api_peliculas_buscar(buscar, pagina)
    return render_template("index.html", usuario=usuario, avatar=avatar, resultado=resultado, buscar=buscar, pagina=pagina)


#-------------------------------------------------------------------------------
# Pagina de contacto
#-------------------------------------------------------------------------------
@app.route("/contacto", methods=["GET"])
def contacto():
    usuario = session.get('nombre')
    avatar = session.get('avatar')
    return render_template("contacto.html", usuario=usuario, avatar=avatar)


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
# Pagina de perfil de usuario
#-------------------------------------------------------------------------------
@app.route("/perfil", methods=["GET", "POST"])
def profile():
    email = session.get('email')
    usuario = session.get('nombre')
    avatar = session.get('avatar')

    if request.method == 'GET':
        estado = 0

    elif 'email' in request.form and 'nombre' in request.form:
        email = session.get('email')
        nuevo_email = request.form['email']
        nuevo_nombre = request.form['nombre']

        if 'password' in request.form:
            nuevo_password = request.form['password']
        else:
            nuevo_password = None
        
        if request.files['avatar'].filename != '':
            imagen = request.files['avatar']
            nombre_imagen = secure_filename(imagen.filename)
            nombre_base, extension = os.path.splitext(nombre_imagen)
            nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

            imagen_vieja = session.get('avatar')
            if imagen_vieja:
                ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)
                if os.path.exists(ruta_imagen):
                    os.remove(ruta_imagen)

        else:
            nombre_imagen = None

        if usuarios.update(email, nuevo_nombre, nuevo_email, nuevo_password, nombre_imagen):
            if nombre_imagen:
                imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
            email = session.get('email')
            usuario = session.get('nombre')
            avatar = session.get('avatar')
            estado = 1
        else:
            estado = 2
    else:
        estado = 2

    return render_template("perfil.html", usuario=usuario, email=email, avatar=avatar, estado=estado)


#-------------------------------------------------------------------------------
# Pagina de favoritos
#-------------------------------------------------------------------------------
@app.route("/favoritos", methods=["GET"])
def favoritos():
    id = session.get('id')
    usuario = session.get('nombre')
    avatar = session.get('avatar')
    resultado = usuarios.cargar_favoritos(id)
    return render_template("favoritos.html", usuario=usuario, avatar=avatar, resultado=resultado)



#-------------------------------------------------------------------------------
# Agregar a favoritos
#-------------------------------------------------------------------------------
@app.route("/api/agregar_favorito", methods=["GET"])
def agregar_favorito():
    usuario = session.get('id')
    pelicula = request.args.get('id')
    nombre = request.args.get('nombre')
    imagen = request.args.get('imagen')
    calificacion = request.args.get('calificacion')

    if usuarios.agregar_favoritos(usuario, pelicula, nombre, imagen, calificacion):
        return {'tipo':'agregar', 'status':'ok'}

    return {'tipo':'agregar', 'status':'error'}



#-------------------------------------------------------------------------------
# Quitar de favoritos
#-------------------------------------------------------------------------------
@app.route("/api/quitar_favorito", methods=["GET"])
def quitar_favorito():
    usuario = session.get('id')
    pelicula = request.args.get('id')
    
    if usuarios.quitar_favoritos(usuario, pelicula):
        return {'tipo':'quitar', 'status':'ok'}

    return {'tipo':'quitar', 'status':'error'}


#-------------------------------------------------------------------------------
# Detalle de película
#-------------------------------------------------------------------------------
@app.route("/detalle", methods=["GET"])
def detalle_pelicula():
    usuario = session.get('nombre')
    avatar = session.get('avatar')
    respuesta = api_detalle_pelicula(request.args.get('id'))
    poster = request.args.get('path')
    return render_template("detalle.html", usuario=usuario, avatar=avatar, respuesta=respuesta, poster=poster)


#-------------------------------------------------------------------------------
# Detalle de coleccion (saga)
#-------------------------------------------------------------------------------
@app.route("/coleccion", methods=["GET"])
def coleccion_peliculas():
    usuario = session.get('nombre')
    avatar = session.get('avatar')
    respuesta = api_detalle_coleccion(request.args.get('id'))
    poster = request.args.get('path')
    return render_template("coleccion.html", usuario=usuario, avatar=avatar, respuesta=respuesta, poster=poster)


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
    usuario_id = session.get('id')
    if usuario_id:
        respuesta["favorito"] = usuarios.es_favorito(usuario_id, id)
    else:
        respuesta["favorito"] = False
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
