import sqlite3
from fastapi import FastAPI, HTTPException, status
from typing import List
from database import obtener_conexion, inicializar_db
from schema import AprendizCREAR, AprendizRespuesta

app = FastAPI(title="API con SQLite nativo")

inicializar_db()

@app.get("/")
def ruta_raiz():
    return {"mensaje": "API conectada a la db"}

@app.get("/aprendices", response_model=List[AprendizRespuesta])
def obtener_aprendices():
    """obtener todos los aprendices de la base de datos SELECT *"""
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM aprendices")
        filas = cursor.fetchall()
        return [dict(fila) for fila in filas]
    
@app.post("/aprendices", response_model=AprendizRespuesta, status_code=status.HTTP_201_CREATED)    
def crear_aprendiz(aprendiz: AprendizCREAR):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        try:
            query = """INSERT INTO aprendices (nombre, documento, programa)
                       VALUES (?, ?, ?)"""
            cursor.execute(query, (aprendiz.nombre, aprendiz.documento, aprendiz.programa))
            conexion.commit()

            nuevo_id = cursor.lastrowid
            return {**aprendiz.model_dump(), "id": nuevo_id}

        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="El documento ya existe")