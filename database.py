import sqlite3
from contextlib import contextmanager

DB_NAME = "modulos.db"

@contextmanager
def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row 
    try:
        yield conexion
    finally:
        conexion.close()

def inicializar_db():
    """Crea la tabla 'modulo' si no existe al arrancar la API"""
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modulo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                lenguaje TEXT NOT NULL,
                horas INTEGER NOT NULL,
                disponible BOOLEAN NOT NULL DEFAULT 1
            )
        """)
        conexion.commit()