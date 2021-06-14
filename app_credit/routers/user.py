from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, hashing
from ..database import get_db


router = APIRouter()

@router.get("/users", tags = ["User"])
def get_all_user(db: Session=Depends(get_db)):
    user_data = db.query(models.User).all()
    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: No user was found in the database - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        return user_data


@router.get("/user/{id}", response_model = schemas.User_View, status_code = status.HTTP_200_OK, tags = ["User"])
def get_user_data(id: int,db: Session=Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id).first()

    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The user with the id {id} not exists - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        return user_data


@router.post("/user", status_code = status.HTTP_200_OK, tags = ["User"])
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_user = models.User(
        login = request.login,
        email = request.email,
        password = hashed_password,
        cpf = request.cpf)
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"msg": f"The user {request.login} was created - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@router.delete("/user/{id}", tags = ["User"])
def destroy_user_data(id: int, db: Session=Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)

    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: id {id} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))
    try:
        db.commit()
        return {"msg": f"id {id} data was deleted from the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}