# services/email_service.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
from config import TOKEN_FILE, FROM_EMAIL, CREDENTIALS_FILE
import os
from google.auth.transport.requests import Request
from fastapi import HTTPException
from interfaces.contact_interface import EmailServiceInterface


class EmailService(EmailServiceInterface):
    """
    Implementación del servicio de envío de correos utilizando la API de Gmail.
    """

    def __init__(self):
        self.creds = None

        # Si no existe el archivo token.json, inicia el flujo de autenticación manual
        if not os.path.exists(TOKEN_FILE):
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, ['https://www.googleapis.com/auth/gmail.send'])
            self.creds = flow.run_local_server(port=0)

            # Guardar el token para futuras ejecuciones
            with open(TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())

        # Cargar las credenciales desde el archivo token.json si existe
        if os.path.exists(TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(
                TOKEN_FILE, ['https://www.googleapis.com/auth/gmail.send'])

        # Si no hay credenciales o están vencidas, actualizar o lanzar una excepción
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                raise HTTPException(
                    status_code=500, detail="Error en la autenticación de OAuth 2.0. Credenciales inválidas.")

            # Guardar las credenciales para reutilización futura
            with open(TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())

        # Construir el servicio de Gmail
        self.service = build('gmail', 'v1', credentials=self.creds)

    def send_email(self, to_email: str, subject: str, body: str):

        # Crear el mensaje MIMEText
        message = MIMEText(body)
        message['to'] = to_email
        message['from'] = FROM_EMAIL
        message['subject'] = subject

        # Codificar el mensaje en base64 para la API de Gmail
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Crear el cuerpo de la solicitud de envío
        send_message = {
            'raw': encoded_message
        }

        try:
            # Enviar el correo
            sent_message = self.service.users().messages().send(
                userId="me", body=send_message).execute()
            print(
                f"Mensaje enviado a {to_email}. Status code: {sent_message['id']}")
        except HttpError as error:
            print(f'Error al enviar el correo: {error}')
            raise HTTPException(
                status_code=500, detail="Error al enviar el correo.")
