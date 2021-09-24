from pydantic import BaseModel

class Post(BaseModel):
	title: str
	body: str

class ShowPost(Post):
	class Config():
		orm_mode = True

class User(BaseModel):
	name: str
	email: str
	password: str
