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
            self.cursor.execute(f"USE {database}")
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
            password VARCHAR(50) NOT NULL, \
            avatar VARCHAR(50) DEFAULT NULL \
        )")

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS favoritos ( \
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
            usuario_id INT NOT NULL, \
            pelicula_id VARCHAR(50) NOT NULL, \
            pelicula_nombre VARCHAR(100) NOT NULL, \
            pelicula_calificacion INT NOT NULL, \
            pelicula_imagen VARCHAR(100) NOT NULL \
        )")


    def get_one(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()


    def get_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def run_query(self, query, valores = None):
        if valores:
            self.cursor.execute(query, valores)
        else:
            self.cursor.execute(query)
        
        self.conn.commit()
        return self.cursor.rowcount > 0