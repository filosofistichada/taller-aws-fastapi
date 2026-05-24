from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from mangum import Mangum
import boto3
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# --- CONFIGURACIÓN AWS Y BD ---
BUCKET_NAME = "taller4-sistop-ssg" # Cambia esto
DB_URL = "bd-taller-fastapi.cp2m0i6a4dsx.us-east-2.rds.amazonaws.com" # Cambia esto

app = FastAPI()
s3_client = boto3.client('s3')
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- MODELO RDS ---
class ImagenUsuario(Base):
    __tablename__ = "imagenes_usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False)
    ruta_s3 = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- ENDPOINTS ---
@app.post("/upload/")
async def upload_image(usuario: str = Form(...), file: UploadFile = File(...)):
    # 1. Validar formato
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=415, detail="Formato no permitido. Solo JPG o PNG.")
    
    # 2. Subir a S3 organizando por usuario
    ruta_s3 = f"{usuario}/{file.filename}"
    s3_client.upload_fileobj(file.file, BUCKET_NAME, ruta_s3)

    # 3. Guardar en RDS
    db = SessionLocal()
    nueva_imagen = ImagenUsuario(usuario=usuario, ruta_s3=ruta_s3)
    db.add(nueva_imagen)
    db.commit()
    db.close()

    return {"mensaje": "Imagen subida exitosamente", "ruta": ruta_s3}

@app.get("/imagen/")
async def get_image(usuario: str, nombre_imagen: str):
    db = SessionLocal()
    ruta_buscada = f"{usuario}/{nombre_imagen}"
    
    # 1. Consultar en RDS
    registro = db.query(ImagenUsuario).filter(ImagenUsuario.ruta_s3 == ruta_buscada).first()
    db.close()

    if not registro:
        raise HTTPException(status_code=404, detail="El usuario o la imagen no existen en la base de datos.")

    # 2. Generar URL prefirmada
    url_prefirmada = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': registro.ruta_s3},
        ExpiresIn=3600
    )

    return {
        "url": url_prefirmada,
        "fecha_creacion": registro.fecha_creacion
    }

# Wrapper para AWS Lambda
handler = Mangum(app)