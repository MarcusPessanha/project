from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database_config.postgre_config import get_db
from ..schema.Debt_schema import Debt_In
from ..schema.Person_schema import Person_Update, Person_In, Person_View
from ..schema.User_schema import User_Schema, User_View

from ..service.person_service import PersonService
from ..service.user_service import UserService

router = APIRouter()



# Persons
@router.get("/allpersons", tags=["Person"])
def all_data(db: Session = Depends(get_db)):
    return PersonService.get_all_data(db)


@router.get("/cpfid/{cpf}", status_code=status.HTTP_200_OK, tags=["Person_CPF"])
def cpf_id(cpf: int, db: Session = Depends(get_db)):
    return PersonService.get_cpf_id(cpf, db)


@router.get("/person/{id}", response_model=Person_View, status_code=status.HTTP_200_OK, tags=["Person_id"])
def id_data(id: int, db: Session = Depends(get_db)):
    return PersonService.get_id_data(id, db)


@router.get("/cpfdata/{cpf}", response_model=Person_View, status_code=status.HTTP_200_OK, tags=["Person_CPF"])
def get_cpf_data(cpf: int, db: Session = Depends(get_db)):
    return PersonService.get_cpf_data(cpf, db)


@router.post("/person", status_code=status.HTTP_200_OK, tags=["Person"])
def create_person_data(request: Person_In, db: Session = Depends(get_db)):
    return PersonService.post_person_data(request, db)


@router.post("/debt", status_code=status.HTTP_200_OK, tags=["Person_CPF"])
def create_person_debt(request: Debt_In, db: Session = Depends(get_db)):
    return PersonService.post_person_debt(request, db)


@router.delete("/person/{id}", tags=["Person_id"])
def destroy_person_data(id: int, db: Session = Depends(get_db)):
    return PersonService.delete_id_data(id, db)


@router.delete("/cpfdata/{cpf}", tags=["Person_CPF"])
def destroy_cpf_data(cpf: int, db: Session = Depends(get_db)):
    return PersonService.delete_cpf_data(cpf, db)


@router.put("/person/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Person_id"])
def update_person_data(id: int, request: Person_Update, db: Session = Depends(get_db)):
    return PersonService.put_person_data(id, request, db)


# Users
@router.get("/users", tags=["User"])
def all_data(db: Session = Depends(get_db)):
    return UserService.get_all_data(db)


@router.get("/user/{id}", response_model=User_View, status_code=status.HTTP_200_OK, tags=["User"])
def get_user_data(id: int, db: Session = Depends(get_db)):
    return UserService.get_user_data(id, db)


@router.post("/user", status_code=status.HTTP_200_OK, tags=["User"])
def create_user(request: User_Schema, db: Session = Depends(get_db)):
    return UserService.post_user(request, db)


@router.delete("/user/{id}", tags=["User"])
def destroy_user_data(id: int, db: Session = Depends(get_db)):
    return UserService.delete_user(id, db)
