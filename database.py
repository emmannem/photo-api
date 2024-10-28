# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/contact_db"

# Crear el motor para interactuar con la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base para definir los modelos de la base de datos
Base = declarative_base()

# Dependencia que nos permite obtener una sesión de base de datos en cualquier parte del código


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
