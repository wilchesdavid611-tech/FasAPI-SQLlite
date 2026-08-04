from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Asignaturas con SQLAlchemy")

@app.post("/asignaturas", response_model=schemas.AsignaturaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_asignatura(asignatura: schemas.AsignaturaCrear, db: Session = Depends(get_db)):

    horas_autonomas = (asignatura.creditos * 48) - asignatura.horas_presenciales
    

    if horas_autonomas < 10:
        raise HTTPException(
            status_code=400,
            detail="Las horas presenciales superan el límite permitido para el número de créditos."
        )
    
    if asignatura.creditos >= 5 or horas_autonomas > 120:
        nivel_dificultad = "Avanzado"
    elif 3 <= asignatura.creditos <= 4:
        nivel_dificultad = "Intermedio"
    else:
        nivel_dificultad = "Básico"
        
    nueva_asignatura = models.Asignatura(
        nombre=asignatura.nombre,
        creditos=asignatura.creditos,
        horas_presenciales=asignatura.horas_presenciales,
        horas_autonomas=horas_autonomas,
        nivel_dificultad=nivel_dificultad
    )
    
   
    db.add(nueva_asignatura)
    db.commit()
    db.refresh(nueva_asignatura)
    
    return nueva_asignatura


@app.get("/asignaturas/resumen", response_model=List[schemas.AsignaturaResumen])
def resumen_asignaturas(db: Session = Depends(get_db)):

    asignaturas = db.query(models.Asignatura).all()
    
    resultado = []
    
    for asig in asignaturas:
        total_semanal = (asig.horas_presenciales + asig.horas_autonomas) / 16
        total_semanal_redondeado = round(total_semanal, 1)
        

        asig_dict = {
            "id": asig.id,
            "nombre": asig.nombre,
            "creditos": asig.creditos,
            "horas_presenciales": asig.horas_presenciales,
            "horas_autonomas": asig.horas_autonomas,
            "nivel_dificultad": asig.nivel_dificultad,
            "total_horas_semanales": total_semanal_redondeado
        }
        resultado.append(asig_dict)
        
    return resultado