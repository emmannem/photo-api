# schemas/contact.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Esquema para recibir los datos del formulario de contacto


class ContactFormCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    message: str

# Esquema para responder con los datos guardados, incluyendo la fecha de creación


class ContactFormResponse(ContactFormCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
