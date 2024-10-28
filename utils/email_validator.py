import re


def is_valid_email(email: str) -> bool:
    """
    Valida si el correo electrónico tiene un formato correcto.
    """
    # Expresión regular para validar el formato del correo electrónico
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None
