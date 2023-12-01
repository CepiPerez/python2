from conector import Conector
from flask import session

class Usuarios:

    def __init__(self, conector):
        self.cursor = conector.cursor
        self.conn = conector.conn


    def get_user(self, email):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE email = '{email}'")
        return self.cursor.fetchone()


    def login(self, email, password):
        account = self.get_user(email)
       
        # Si existe el usuario creamos una sesion, de lo contrario retornamos Falso
        if account and account['password']==password:
            session['loggedin'] = True
            session['id'] = account['id']
            session['nombre'] = account['nombre']
            session['email'] = account['email']
            return True
        else:
            return False
        
    
    def logout(self):
        session['loggedin'] = False
        session.pop('id', None)
        session.pop('nombre', None)


    def register(self, nombre, email, password):
        account = self.get_user(email)
       
        # Si ya existe el usuario creamos retornamos error
        if account:
            return False
        else:
            sql = "INSERT INTO usuarios (email, nombre, password) VALUES (%s, %s, %s)"
            valores = (email, nombre, password)

            self.cursor.execute(sql, valores)        
            self.conn.commit()

            # Si se registró correctamente hacemos el login 
            return self.login(email, password)


    #----------------------------------------------------------------
    def agregar_producto(self, codigo, descripcion, cantidad, precio, imagen, proveedor):
        # Verificamos si ya existe un producto con el mismo código
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo}")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        
        sql = "INSERT INTO productos (codigo, descripcion, cantidad, precio, imagen_url, proveedor) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (codigo, descripcion, cantidad, precio, imagen, proveedor)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

    #----------------------------------------------------------------
    def consultar_producto(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor):
        sql = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, imagen_url = %s, proveedor = %s WHERE codigo = %s"
        valores = (nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos

    #----------------------------------------------------------------
    def eliminar_producto(self, codigo):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM productos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_producto(self, codigo):
        # Mostramos los datos de un producto a partir de su código
        producto = self.consultar_producto(codigo)
        if producto:
            print("-" * 40)
            print(f"Código.....: {producto['codigo']}")
            print(f"Descripción: {producto['descripcion']}")
            print(f"Cantidad...: {producto['cantidad']}")
            print(f"Precio.....: {producto['precio']}")
            print(f"Imagen.....: {producto['imagen_url']}")
            print(f"Proveedor..: {producto['proveedor']}")
            print("-" * 40)
        else:
            print("Producto no encontrado.")