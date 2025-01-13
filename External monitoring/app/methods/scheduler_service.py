import logging
from apscheduler.schedulers.background import BackgroundScheduler
from ..core.db_connector import Connector
import requests
from .email_service import Email



class SchedulerService:
    def __init__(self):
        self.conn = Connector()
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.e = Email()


    # Načítání existujících alertů do scheduleru při spuštění aplikace
    def load_existing_tasks(self):
        with self.conn.get_db_connection() as conn:
            alerts = conn.execute(
                'SELECT pers_id, url, interval, threshold, email FROM urlmonitor join users on users.user_id = urlmonitor.pers_id WHERE status = "a"').fetchall()

        for alert in alerts:
            user_id = alert["pers_id"]
            url = alert["url"]
            interval = alert["interval"]
            threshold = alert["threshold"]
            email = alert["email"]
            job_id = f"user-{user_id}-{url}"

            if not self.scheduler.get_job(job_id):
                self.scheduler.add_job(
                    self.ping_url,
                    'interval',
                    seconds=interval,
                    args=[user_id, url, email, threshold],
                    id=job_id
                )
                logging.info(f"Načtena úloha: {job_id} s intervalem {interval} sekund.")
            else:
                logging.warning(f"Úloha {job_id} již existuje a nebude znovu přidána.")

    # Ping URL
    def ping_url(self, user_id, url, email, threshold):
        job_id = f"user-{user_id}-{url}"
        if not self.scheduler.get_job(job_id):
            logging.info(f"Úloha {job_id} byla ukončena a nebude spuštěna.")
            return

        try:
            response = requests.get(url, timeout=5)
            response_time = response.elapsed.total_seconds()
            logging.info(f"[User {user_id}] URL: {url} | Odezva: {response_time} sekund")
        except requests.RequestException as e:
            logging.error(f"[User {user_id}] Chyba při pingu na {url}: {e}")

        threshold = float(threshold)
        if response_time < threshold:
            self.e.email_notification(email)
            logging.info(f"Response time je menší než uvedený v db. Byl odeslán email na uživatele {user_id}")
        else:
            logging.info(f"Threshold pro odeslání emailu pro uživatele {user_id} nebyl splněn. Email nebyl odeslán.")

    # Přidání nové ůlohy do scheduleru
    def add_task(self, user_id, url, interval, threshold):
        # Získání emailu z databáze
        with self.conn.get_db_connection() as conn:
            user_email = conn.execute(
                'SELECT Email FROM users WHERE user_id = ?',
                (user_id,)
            ).fetchone()

        if not user_email:
            raise ValueError(f"Uživatel s ID {user_id} nemá přiřazený e-mail.")

        email = user_email["Email"]  # Získaný e-mail

        # Přidání úlohy do scheduleru
        job_id = f"user-{user_id}-{url}"
        existing_job = self.scheduler.get_jobs(job_id)
        interval = int(interval)

        if existing_job:
            self.scheduler.remove_job(job_id)
            logging.info(f"Úloha {job_id} byla odstraněna před vytvořením nové.")

        self.scheduler.add_job(
            self.ping_url,
            'interval',
            seconds=interval,
            args=[user_id, url, email, threshold],  # Předáváme email do ping_url
            id=job_id
        )
        logging.info(f"Přidána úloha: {job_id} s intervalem {interval} sekund.")

    # Odstranění úlohy ze scheduleru
    def remove_task(self, user_id, url):
        job_id = f"user-{user_id}-{url}"
        job = self.scheduler.get_job(job_id)

        # for job in jobs:
        if job:
            self.scheduler.remove_job(job.id)
            logging.info(f"Úloha {job.id} byla odstraněna.")
        else:
            logging.warning(f"Úloha {job_id} neexistuje, není co odstranit.")