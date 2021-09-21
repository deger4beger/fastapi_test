from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
	email: str
	password: str
	confirmed: Optional[bool]


@app.get("/users")
def get_users(limit: int = 10, confirm: bool = True, sort: Optional[str] = None):
	if confirm:
		return {"response": f"{limit} users, all is confirmed"}
	else:
		return {"response": f"{limit} users, all is unconfirmed"}


@app.get("/users/{id}")
def get_user(id: int):
	return {"response": id}

@app.post("/users")
def create_user(request: User):
	return request
