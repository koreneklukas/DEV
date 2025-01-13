import smtplib
from email.message import EmailMessage
from ..core.config import Config


class Email:

    def email_notification(self, email):
        # Vytvoření emailu
        msg = EmailMessage()
        msg['Subject'] = "Dobrý den kořenys"
        msg['From'] = "koreneklukas@seznam.cz"
        msg['To'] = f"{email}"
        msg.set_content("Tohle přišlo z mého napsaného kódu. BAF")

        with smtplib.SMTP('smtp.seznam.cz', 587) as server:
            server.starttls()
            server.login(Config.user_name, Config.pwd)
            server.send_message(msg)
            server.quit()