import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from classes.search import Search
from config import EMAIL_ACCOUNT, EMAIL_APP_KEY


def send_email(destinatary: str, search: Search, excel_name: str):
    SUBJECT = "Posts encontrados"
    MESSAGE = f"""
    Filtro usado:
    - Keyword: {search.keyword if search.keyword is not None else "None"}
    - Account: {search.account if search.account is not None else "None"}
    - Start: {search.start_date.date()}
    - End: {search.end_date.date()}
    """

    msg = MIMEMultipart()
    try:
        msg['From'] = "Twitter Scraping <twitter.scraping.pucv@gmail.com>"
        msg['To'] = destinatary
        msg['Subject'] = SUBJECT
        msg.attach(MIMEText(MESSAGE, 'plain'))

        with open(excel_name, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(excel_name)}'
            )
            msg.attach(part)
    except Exception:
        raise Exception("Error: No se pudo crear el mensaje de correo electrónico")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_APP_KEY)

        text = msg.as_string()
        server.sendmail(EMAIL_ACCOUNT, destinatary, text)
        print("Correo electrónico enviado correctamente")
        server.quit()
    except Exception as e:
        raise Exception(f"Error: No se pudo enviar el correo electrónico, mensaje: {e}")