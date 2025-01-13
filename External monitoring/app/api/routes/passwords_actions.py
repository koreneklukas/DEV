from fastapi import APIRouter, Depends
from ...models.api_schema import ChangePwd, ForgetPwd
from ...core.auth import Authorization
from ...methods.password_service import Pwd


class PasswordActions:
    def __init__(self):
        self.router = APIRouter()
        self.auth = Authorization()
        self.setup_routes()
        self.password = Pwd()


    def setup_routes(self):
        # WS pro změnu hesla po přihlášení
        @self.router.put("/protected/password", tags=["protected"])
        async def protected_password(change: ChangePwd, user_id: str = Depends(self.auth.verify_token)):
            self.password.change_pwd(change, user_id)
            return {"message": f'Welcome {user_id}'}

        # WS pro změnu hesla bez přihlášení
        @self.router.put("/user/password/forget", tags=["forget-password"])
        async def forget_password(forget_pwd: ForgetPwd):
            self.password.forget_pwd(forget_pwd)
            return {"message": "Password was changed."}
