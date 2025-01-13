from fastapi import APIRouter, Depends
from ...models.api_schema import CreateAlert
from ...core.auth import Authorization
from ...methods.alert_service import Alert
from ...methods.scheduler_service import SchedulerService

class AlertsServices:
    def __init__(self):
        self.router = APIRouter()
        self.auth = Authorization()
        self.setup_routes()
        self.alerts = Alert()
        self.scheduler = SchedulerService()



    def setup_routes(self):

        # WS pro vytvoření alertu
        @self.router.post("/protected/alert/create", tags=["create_alert"])
        async def create_alert(create_alert: CreateAlert, user_id: str = Depends(self.auth.verify_token)):
            self.alerts.insert_alert(create_alert, user_id)

            if create_alert.Status == "a":
                self.scheduler.add_task(user_id, create_alert.Url, create_alert.Interval, create_alert.Threshold)
            return {"message": "Alert was add. "}

        # WS pro načtení všech alertů daného uživatele
        @self.router.get("/protected/alert/all", tags=["get_all_alerts"])
        async def get_alerts(user_id: str = Depends(self.auth.verify_token)):
            return self.alerts.get_user_alerts(user_id)

        # WS pro update alertu daného uživatele
        @self.router.put("/protected/alert/update", tags=["update_alert"])
        async def update_alert(update_alert: CreateAlert, user_id: str = Depends(self.auth.verify_token)):
            self.alerts.update_alert(user_id, update_alert)
            interval = int(update_alert.Interval)

            if update_alert.Status == "n":
                self.scheduler.remove_task(user_id, update_alert.Url)
            else:
                self.scheduler.add_task(user_id, update_alert.Url, interval, update_alert.Threshold)
            return {"message": "Alert was updated. "}

