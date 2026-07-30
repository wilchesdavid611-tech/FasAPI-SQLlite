import sqlite3
DATABASE_NAME = 'sistema_aprendices.db'

def obtener_conexion():
    """
    crear una conexion con la base de datos y retornarla en forma de diccionario
    """
    conexion = sqlite3.connect(DATABASE_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    """crear las tablas necesarias si es que no existe"""
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS aprendices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento TEXT NOT NULL,
            programa TEXT NOT NULL
        )""")

        conexion.commit()
    