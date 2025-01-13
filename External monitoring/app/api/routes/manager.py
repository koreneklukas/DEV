from .alerts_service import AlertsServices
from .login_registration import LoginRegistration
from .passwords_actions import PasswordActions
import logging
from fastapi import FastAPI
from ...methods.scheduler_service import SchedulerService
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
class ApplicationApi:
    def __init__(self):
        self.app = FastAPI()

        # Nastavení CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Povolit všechny domény (doporučuji specifikovat konkrétní domény ve finální verzi)
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.alerts = AlertsServices()
        self.log_reg = LoginRegistration()
        self.password = PasswordActions()
        self.scheduler = SchedulerService()

        # Připojení routeru k hlavní aplikaci
        self.app.include_router(self.alerts.router)
        self.app.include_router(self.log_reg.router)
        self.app.include_router(self.password.router)

    # Metoda na spuštění asynchronního serveru pomocí aplikace Uvicorn
    def run(self, host="127.0.0.1", port=8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

api = ApplicationApi()
app = api.app

# Načtení job úloh při spuštění aplikace
api.scheduler.load_existing_tasks()
