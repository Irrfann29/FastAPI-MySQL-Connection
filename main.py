from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Create a model instance from the Pydantic data
    new_user = models.User(name=user.name, email=user.email)
    
    # 2. Add the object to the session
    db.add(new_user)
    
    # 3. Commit the transaction to save to MySQL
    db.commit()
    
    # 4. Refresh to get the generated ID from the database
    db.refresh(new_user)
    
    return new_user