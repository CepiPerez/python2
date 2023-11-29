import os
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
#import mysql.connector
#from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

# Carpeta para guardar las imagenes.
RUTA_DESTINO = '/static/imagenes/'


#--------------------------------------------------------------------
# Pagina principal
#--------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
    

#--------------------------------------------------------------------
# Pagina de contacto
#--------------------------------------------------------------------
@app.route("/contacto", methods=["GET"])
def contacto():
    return render_template("contacto.html")


#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)