# services/contact_service.py
from sqlalchemy.orm import Session
from models.contact import ContactForm
from schemas.contact import ContactFormCreate, ContactFormResponse
from utils.email_validator import is_valid_email
from fastapi import HTTPException
from interfaces.contact_interface import ContactInterface
from services.base_service import BaseService
from services.email_service import EmailService


class ContactService(BaseService[ContactForm, ContactFormCreate], ContactInterface):
    """
    Implementación del servicio de contacto.
    Hereda de BaseService para las operaciones CRUD comunes y extiende la lógica de negocio específica.
    """

    def __init__(self):
        super().__init__(ContactForm)

    def create_contact(self, db: Session, contact_data: ContactFormCreate) -> ContactFormResponse:
        # Validar el correo electrónico
        if not is_valid_email(contact_data.email):
            raise HTTPException(
                status_code=400, detail="Correo electrónico no válido."
            )

        # Crear el contacto utilizando el método `create` de la clase BaseService
        new_contact = self.create(db, contact_data)

        # Enviar el correo al contacto
        email_service = EmailService()
        subject = "Gracias por contactarnos"
        body = f"""
        Hola {new_contact.first_name},

        Gracias por ponerte en contacto con nosotros. Hemos recibido tu mensaje:
        
        "{new_contact.message}"

        Nos pondremos en contacto contigo lo antes posible.

        Saludos,
        El equipo.
        """
        email_service.send_email(new_contact.email, subject, body)

        # Retornar el contacto creado
        return new_contact
