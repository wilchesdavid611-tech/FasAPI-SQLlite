from fastapi import FastAPI, HTTPException, status
from typing import List
from database import obtener_conexion, inicializar_db
from schema import ModuloCrear, ModuloRespuesta
import sqlite3

app = FastAPI(title="API de Módulos con SQLite")

inicializar_db()

@app.get("/")
def ruta_raiz():
    return {"mensaje" : "API de Módulos Conectada a SQLite"}

@app.get("/modulos", response_model=List[ModuloRespuesta])
def obtener_modulos():
    """
    Obtener todos los módulos desde la base de datos
    """
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM modulo")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]

@app.post("/modulos", response_model=ModuloRespuesta, status_code=status.HTTP_201_CREATED)
def crear_modulo(modulo: ModuloCrear):
    """
    Guardar un nuevo módulo en la base de datos
    """
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        try:
            query = "INSERT INTO modulo (titulo, lenguaje, horas, disponible) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (modulo.titulo, modulo.lenguaje, modulo.horas, modulo.disponible))
            conexion.commit()
            
            nuevo_id = cursor.lastrowid
            
            return {**modulo.model_dump(), "id": nuevo_id}
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Ocurrió un error al guardar: {str(e)}"
            )