# interfaces/contact_interface.py
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from schemas.contact import ContactFormCreate, ContactFormResponse


class ContactInterface(ABC):
    """
    Interfaz para el servicio de contacto.
    Define los métodos que deben implementarse para manejar el formulario de contacto.
    """

    @abstractmethod
    def create_contact(self, db: Session, contact_data: ContactFormCreate) -> ContactFormResponse:
        """
        Método abstracto para crear un contacto.
        :param db: Sesión de la base de datos.
        :param contact_data: Datos del formulario de contacto.
        :return: ContactFormResponse con los datos del contacto creado.
        """
        pass


class EmailServiceInterface(ABC):
    """
    Interfaz para el servicio de envío de correos electrónicos.
    Define los métodos que deben implementarse para enviar correos.
    """

    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str):
        """
        Método abstracto para enviar un correo electrónico.
        :param to_email: Dirección de correo del destinatario.
        :param subject: Asunto del correo.
        :param body: Contenido del correo.
        """
        pass
