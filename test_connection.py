# test_connection.py
from database import SessionLocal
from sqlalchemy import text


def test_db_connection():
    db = SessionLocal()
    try:
        # Ejecutar una consulta básica para verificar la conexión
        result = db.execute(text("SELECT 1"))
        print("Conexión exitosa:", result.fetchone())
    except Exception as e:
        print("Error en la conexión:", e)
    finally:
        db.close()


test_db_connection()
