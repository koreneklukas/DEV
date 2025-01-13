from pydantic import BaseModel


class CreateUser(BaseModel):
	Name: str
	Last_Name: str
	User_Name: str
	Email: str
	Password: str

class Login(BaseModel):
	Username: str
	Password: str

class ChangePwd(BaseModel):
	Old_Password: str
	New_Password: str

class ForgetPwd(BaseModel):
	User_Name: str
	New_Password: str


class CreateAlert(BaseModel):
	Url: str
	Threshold: str
	Interval: str
	Status: str



