from ..core.db_connector import Connector
from ..models.api_schema import CreateAlert
import logging
from .scheduler_service import SchedulerService


class Alert:
    def __init__(self):
        self.conn = Connector()
        self.scheduler = SchedulerService()

    # Metoda pro insertování alertu
    def insert_alert(self, insert_alert: CreateAlert, user_id):
        with self.conn.get_db_connection() as conn:
            values = (
                user_id,
                insert_alert.Url,
                insert_alert.Interval,
                insert_alert.Threshold,
                insert_alert.Status
            )
            conn.execute('insert into urlmonitor (pers_id, url, interval, threshold, status, modif_time) VALUES (?,?,?,?,'
                     '?, DATETIME("now", "localtime"))', values)
            conn.commit()


    # Metoda pro získání všech alertů
    def get_user_alerts(self, user_id):
        conn = self.conn.get_db_connection()
        alerts = conn.execute('select url, interval, threshold, status from urlmonitor where pers_id = ?',
                              (user_id,)).fetchall()
        return [{"url": alert["url"], "interval": alert["interval"], "status": alert["status"]} for alert in alerts]

    # Metoda pro update alertu
    def update_alert(self, user_id, update_alert: CreateAlert):
        with self.conn.get_db_connection() as conn:
            conn.execute(
                'UPDATE urlmonitor SET url = ?, interval = ?, threshold = ?, status = ?, modif_time = DATETIME("now", "localtime") '
                'WHERE pers_id = ?',
                (update_alert.Url, update_alert.Interval, update_alert.Threshold, update_alert.Status, user_id)
            )
            conn.commit()

        if update_alert.Status != "a":  # Pokud alert není aktivní, odstraníme odpovídající úlohu
            self.scheduler.remove_task(user_id, update_alert.Url)
        else:  # Pokud alert je aktivní, aktualizujeme nebo vytvoříme úlohu
            self.scheduler.add_task(user_id, update_alert.Url, update_alert.Interval, update_alert.Threshold)

        # Výpis všech aktuálních úloh ve scheduleru
        jobs = self.scheduler.scheduler.get_jobs()
        logging.info("Aktuální úlohy ve scheduleru:")
        for job in jobs:
            logging.info(f"Úloha: {job.id}")

        return {"message": "Alert byl aktualizován."}