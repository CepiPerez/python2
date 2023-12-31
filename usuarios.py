from conector import Conector
from flask import session

class Usuarios:

    def __init__(self, conexion):
        self.conexion = conexion


    def get_user(self, email):
        return self.conexion.get_one(f"SELECT * FROM usuarios WHERE email = '{email}'")


    def login(self, email, password):
        account = self.get_user(email)
       
        # Si existe el usuario creamos una sesion, de lo contrario retornamos Falso
        if account and account['password']==password:
            session['loggedin'] = True
            session['id'] = account['id']
            session['nombre'] = account['nombre']
            session['email'] = account['email']
            session['avatar'] = account['avatar']
            return True
        else:
            return False
        
    
    def logout(self):
        session['loggedin'] = False
        session.pop('id')
        session.pop('nombre')
        session.pop('email')


    def register(self, nombre, email, password):
        account = self.get_user(email)
       
        # Si ya existe el usuario creamos retornamos error
        if account:
            return False
        else:
            sql = "INSERT INTO usuarios (email, nombre, password) VALUES (%s, %s, %s)"
            valores = (email, nombre, password)

            if self.conexion.run_query(sql, valores):
                return self.login(email, password)
            
            return False
        

    def update(self, original, nombre, email, password, avatar):
        account = self.get_user(original)
       
        # Si no existe el usuario creamos retornamos error
        if not account:
            return False
        else:
            if not password:
                password = account['password']
            if not avatar:
                avatar = account['avatar']

            sql = "UPDATE usuarios SET nombre = %s, email = %s, password = %s, avatar = %s WHERE email = %s"
            valores = (nombre, email, password, avatar, original)

            if self.conexion.run_query(sql, valores):
                session['nombre'] = nombre
                session['email'] = email
                session['avatar'] = avatar
                return True
            
            return False


    def es_favorito(self, usuario, pelicula):
        resultado = self.conexion.get_one(f"SELECT * FROM favoritos WHERE usuario_id = {usuario} and pelicula_id = '{pelicula}'")
        if resultado:
            return True
        return False


    def cargar_favoritos(self, usuario):
        return self.conexion.get_all(f"SELECT * FROM favoritos WHERE usuario_id = {usuario} ORDER BY pelicula_id")
    

    def agregar_favoritos(self, usuario, pelicula, nombre, imagen, calificacion):
        sql = f"INSERT INTO favoritos (usuario_id, pelicula_id, pelicula_nombre, pelicula_imagen, pelicula_calificacion) VALUES (%s, %s, %s, %s, %s)"
        valores = (usuario, pelicula, nombre, imagen, calificacion)
        return self.conexion.run_query(sql, valores)
    

    def quitar_favoritos(self, usuario, pelicula):
        sql = f"DELETE FROM favoritos WHERE usuario_id = {usuario} and pelicula_id = {pelicula}"
        return self.conexion.run_query(sql)
