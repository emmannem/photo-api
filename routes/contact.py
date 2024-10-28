# routes/contact.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.contact import ContactFormCreate, ContactFormResponse
from services.contact_service import ContactService
from database import get_db

# Crear un enrutador para las rutas de contacto
router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)

# Instancia de ContactService
contact_service = ContactService()


@router.post("/", response_model=ContactFormResponse)
def submit_contact_form(contact_data: ContactFormCreate, db: Session = Depends(get_db)):
    """
    Ruta para enviar un formulario de contacto.
    1. Recibe los datos del formulario.
    2. Valida y guarda los datos en la base de datos.
    3. Envía un correo electrónico de confirmación al usuario.
    """
    try:
        # Llamar al método `create_contact` de ContactService
        new_contact = contact_service.create_contact(db, contact_data)
        return new_contact
    except HTTPException as e:
        # Manejo de excepciones
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Ocurrió un error al procesar la solicitud."
        )
