from fastapi import FastAPI, Depends
from typing import Optional
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():

	db = SessionLocal()

	try:
		yield db
	finally:
		db.close()


@app.post("/post")
def create(post: schemas.Post, db: Session = Depends(get_db)):

	new_post = models.Blog(title=post.title, body=post.body)
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post
