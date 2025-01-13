from ..core.db_connector import Connector
from passlib.context import CryptContext
from fastapi import HTTPException
from ..models.api_schema import ChangePwd, ForgetPwd


class Pwd:
    def __init__(self):
        self.conn = Connector()

    # Metoda pro změnu hesla po přihlášení
    def change_pwd(self, change_pwd: ChangePwd, user_id):
        conn = self.conn.get_db_connection()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user_id_new = int(user_id)
        get_client = conn.execute('SELECT hashed_pwd from password WHERE id_us = ?', (user_id_new,)).fetchone()

        get_old_pwd = get_client["hashed_pwd"]
        if not pwd_context.verify(change_pwd.Old_Password, get_old_pwd):
            conn.close()
            raise HTTPException(status_code=401, detail="Current password is incorrect.")

        hashed_new_pwd = pwd_context.hash(change_pwd.New_Password)
        conn.execute('UPDATE password SET hashed_pwd = ?, modif_time = DATEtime("now", "localtime") WHERE id_us=?',
                     (hashed_new_pwd, user_id_new))
        conn.commit()
        conn.close()
        return {"message": "Passsword was changed successfully."}

    # Metoda pro zapomenuté heslo (bez loginu)
    def forget_pwd(self, forget_pwd: ForgetPwd):
        conn = self.conn.get_db_connection()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        get_user = conn.execute('SELECT user_id FROM users WHERE user_name =?', (forget_pwd.User_Name,)).fetchone()
        get_user_id = get_user["user_id"]

        if get_user is None:
            raise HTTPException(status_code=404, detail="User not exist. ")
        else:
            hashed_new_pwd = pwd_context.hash(forget_pwd.New_Password)
            conn.execute('UPDATE password SET hashed_pwd = ?, modif_time = DATEtime("now", "localtime") WHERE id_us=?',
                         (hashed_new_pwd, get_user_id))
            conn.commit()
            conn.close()
            return {"message": "Passsword was changed successfully."}