from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
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



@app.get("/post", response_model=List[schemas.ShowPost])
def get_all(db: Session = Depends(get_db)):

    Posts = db.query(models.Post).all()

    return Posts


@app.get("/post/{id}", response_model=schemas.ShowPost)
def get_one(id: int, response: Response, db: Session = Depends(get_db)):

    Post = db.query(models.Post).filter(models.Post.id == id).first()
    if not Post:
    	raise HTTPException(
    		status_code=status.HTTP_404_NOT_FOUND,
    		detail=f"Post with id {id} doesn't exists"
    	)

    return Post


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Post, db: Session = Depends(get_db)):

    new_post = models.Post(title=request.title, body=request.body)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.put("/post/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Post, db: Session = Depends(get_db)):

	post = db.query(models.Post).filter(models.Post.id == id)
	if not post.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesn't exists")

	post.update(request.dict())
	db.commit()

	return "ok"


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):

	post = db.query(models.Post).filter(models.Post.id == id)

	if not post.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} doesn't exists")

	post.delete(synchronize_session=False)
	db.commit()

	return "ok"


@app.post("/user")
def create_user(request: schemas.User):
    pass