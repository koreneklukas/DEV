from fastapi import APIRouter, HTTPException
from ...models.api_schema import CreateUser, Login
from ...core.auth import Authorization
from passlib.context import CryptContext
from ...methods.users_service import Users


class LoginRegistration:

    def __init__(self):
        self.router = APIRouter()
        self.auth = Authorization()
        self.setup_routes()
        self.users = Users()

    def setup_routes(self):

        # WS na provedení registrace (vytvoří se účet)
        @self.router.post("/user/register/", response_model=CreateUser, tags=["create_user"])
        async def create(create_user: CreateUser):
            self.users.insert_client(create_user)
            return create_user

        # WS na přihlášení do aplikace
        @self.router.post("/user/login", tags=["login"])
        async def login(user: Login):
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

            db_user = self.users.get_user(user.Username)

            if not db_user or not pwd_context.verify(user.Password, db_user["hashed_pwd"]):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            # Generate JWT token
            access_token = self.auth.create_access_token(data={"sub": db_user["user_id"]})
            return {"access_token": access_token, "token_type": "bearer"}










