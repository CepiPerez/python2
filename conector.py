import mysql.connector

class Conector:

    # Constructor de la clase
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password
        )
        self.cursor = self.conn.cursor(dictionary=True)

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute("USE miapp")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
        
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS usuarios ( \
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
            email VARCHAR(50) NOT NULL, \
            nombre VARCHAR(100) NOT NULL, \
            password VARCHAR(50) NOT NULL \
        )")

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS favoritos ( \
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
            usuario_id INT NOT NULL, \
            pelicula_id VARCHAR(50) NOT NULL, \
            pelicula_nombre VARCHAR(100) NOT NULL, \
            pelicula_calificacion INT NOT NULL, \
            pelicula_imagen VARCHAR(100) NOT NULL \
        )")