from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..schema import postgre_schemas as schema
from ..database_config.postgre_config import get_db


from ..repository import postgre_person_repository, postgre_user_repository


router = APIRouter()

# Persons
@router.get("/allpersons", tags = ["Person"])
def all_data(db: Session=Depends(get_db)):
    return postgre_person_repository.get_all_data(db)


@router.get("/cpfid/{cpf}", status_code = status.HTTP_200_OK, tags = ["Person_CPF"])
def cpf_id(cpf: int, db: Session=Depends(get_db)):
    return postgre_person_repository.get_cpf_id(cpf, db)


@router.get("/person/{id}", response_model = schema.Person_View, status_code = status.HTTP_200_OK, tags = ["Person_id"])
def id_data(id: int, db: Session=Depends(get_db)):
    return postgre_person_repository.get_id_data(id, db)


@router.get("/cpfdata/{cpf}", response_model = schema.Person_View, status_code = status.HTTP_200_OK, tags = ["Person_CPF"])
def get_cpf_data(cpf: int, db: Session=Depends(get_db)):
    return postgre_person_repository.get_cpf_data(cpf, db)


@router.post("/person", status_code = status.HTTP_200_OK, tags = ["Person"])
def create_person_data(request: schema.Person_In, db: Session=Depends(get_db)):
    return postgre_person_repository.post_person_data(request, db)


@router.post("/debt", status_code = status.HTTP_200_OK, tags = ["Person_CPF"])
def create_person_debt(request: schema.Debt_In, db: Session=Depends(get_db)):        
    return postgre_person_repository.post_person_debt(request, db)


@router.delete("/person/{id}", tags = ["Person_id"])
def destroy_person_data(id: int, db: Session=Depends(get_db)):
    return postgre_person_repository.delete_id_data(id, db)

    
@router.delete("/cpfdata/{cpf}", tags = ["Person_CPF"])
def destroy_cpf_data(cpf: int, db: Session=Depends(get_db)):
    return postgre_person_repository.delete_cpf_data(cpf, db)


@router.put("/person/{id}", status_code=status.HTTP_202_ACCEPTED, tags = ["Person_id"])
def update_person_data(id: int, request: schema.Person_Update, db: Session=Depends(get_db)):
    return postgre_person_repository.put_person_data(id, request, db)


# Users
@router.get("/users", tags = ["User"])
def all_data(db: Session=Depends(get_db)):
    return postgre_user_repository.get_all_data(db)


@router.get("/user/{id}", response_model = schema.User_View, status_code = status.HTTP_200_OK, tags = ["User"])
def get_user_data(id: int,db: Session=Depends(get_db)):
    return postgre_user_repository.get_user_data(id, db)


@router.post("/user", status_code = status.HTTP_200_OK, tags = ["User"])
def create_user(request: schema.User, db: Session=Depends(get_db)):
    return postgre_user_repository.post_user(request, db)


@router.delete("/user/{id}", tags = ["User"])
def destroy_user_data(id: int, db: Session=Depends(get_db)):
    return postgre_user_repository.delete_user_data(id, db)
