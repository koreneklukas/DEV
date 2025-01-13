from ..core.db_connector import Connector
from passlib.context import CryptContext
import random
from fastapi import HTTPException
from ..models.api_schema import CreateUser


class Users:
    def __init__(self):
        self.conn = Connector()


    # Metoda na zístkání všech uživatelů z DB
    def get_user(self, username: str):
        conn = self.conn.get_db_connection()
        user = conn.execute(
            'SELECT u.user_name, u.user_id, u.Email, p.hashed_pwd FROM users u join password p on p.id_us = u.user_id WHERE u.user_name = ?',
            (username,)).fetchone()
        conn.close()

        if user:
            return {
                "user_name": user["user_name"],
                "user_id": user["user_id"],
                "Email": user["Email"],
                "hashed_pwd": user["hashed_pwd"]
            }
        return None

    # Metoda na přidání nového usera do DB
    def insert_client(self, create_user: CreateUser):
        conn = self.conn.get_db_connection()

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        user_id = random.randint(1000, 9999)

        unique_result = conn.execute('Select 1 from users where Email = ?', (create_user.Email,)).fetchone()

        if unique_result is None:
            values = (
                create_user.Name,
                create_user.Last_Name,
                create_user.User_Name,
                create_user.Email,
                user_id
            )

            new_client = conn.execute(
                'insert into users (Name, Last_Name, user_name, Email, user_id, modif_time) VALUES (?,?,?,?,?, DATETIME("now", "localtime"))',
                values)
            hashed_pw = pwd_context.hash(create_user.Password)
            conn.execute(
                'insert into password (hashed_pwd, id_us, modif_time) VALUES (?,?, DATETIME("now", "localtime"))',
                (hashed_pw, user_id))
            conn.commit()
            conn.close()
            print(hashed_pw)
            return new_client
        else:
            conn.close()
            raise HTTPException(status_code=422, detail="User already exist")
