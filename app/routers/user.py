from .. import utils, schemas, models
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user_result = db.query(models.User).filter(models.User.email == user.email).first()
    if user_result:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, 
                            detail=f"User with email: {user.email} alreadu exists")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserReturn)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} does not exist")
    return user