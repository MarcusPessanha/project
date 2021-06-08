from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from app_credit import schemas, models, database, hashing




app = FastAPI()

models.Base.metadata.create_all(database.engine)


@app.get("/", tags = ['Index'])
def index():
    response = {"message": "Hello World"}
    return response


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/person", tags = ["Person"])
def get_all_data(db: Session=Depends(get_db)):
    data_A = db.query(models.Base_A).all()
    data_B = db.query(models.Base_B).all()
    return data_A, data_B


@app.get("/person/{id}", status_code = status.HTTP_200_OK, tags = ["Person"])
def get_person_data(id, response: Response, db: Session=Depends(get_db)):
    data_A = db.query(models.Base_A).filter(models.Base_A.id == id).first()
    data_B = db.query(models.Base_B).filter(models.Base_B.id == id).first()
    if not data_A:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"The person with the id {id} not exists in the database - status: {response.status_code}"}
    
    return data_A, data_B 


@app.post("/person", status_code = status.HTTP_200_OK, tags = ["Person"])
def create_person_data(request: schemas.Person, db: Session=Depends(get_db)):
    sensitive_data = models.Base_A(
        cpf=request.cpf,
        name=request.name,
        address_cep = request.address_cep,
        debt_list = request.debt_list,
        person_id = 1
    )
    score_data = models.Base_B(
        age = request.age,
        patrimony = request.patrimony,
        address_cep = request.address_cep,
        occupation = request.occupation
    )
    try:
        db.add(sensitive_data)
        db.commit()
        db.refresh(sensitive_data)
        db.add(score_data)
        db.commit()
        db.refresh(score_data)
        return {"msg": f"The person of cpf {request.cpf} was registered in the database - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}

    
@app.delete("/person/{id}", tags = ["Person"])
def destroy_person_data(id, response: Response, db: Session=Depends(get_db)):
    sensitive_data = db.query(models.Base_A).filter(models.Base_A.id == id).delete(synchronize_session=False)
    score_data = db.query(models.Base_B).filter(models.Base_B.id == id).delete(synchronize_session=False)

    if not sensitive_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"id {id} does not exist in database - status: - status: {response.status_code}"}

    try:
        db.commit()
        return {"msg": f"id {id} data was deleted from the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@app.put("/person/{id}", status_code=status.HTTP_202_ACCEPTED, tags = ["Person"])
def update_person_data(id, response: Response, request: schemas.Person, db: Session=Depends(get_db)):
    sensitive_data = db.query(models.Base_A).filter(models.Base_A.id == id)
    score_data = db.query(models.Base_B).filter(models.Base_B.id == id)
    
    if not sensitive_data.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"id {id} does not exist in database - status: - status: {response.status_code}"}
    else:
        sensitive_data.update({
        "cpf": request.cpf,
        "name": request.name,
        "address_cep": request.address_cep,
        "debt_list": request.debt_list
        },synchronize_session=False
    )
        score_data.update({
        "age": request.age,
        "patrimony": request.patrimony,
        "address_cep": request.address_cep,
        "occupation": request.occupation
        },synchronize_session=False)

    try:
        db.commit()
        return {"msg": f"id {id} data was updated in the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@app.get("/user/{id}", response_model = schemas.User_View, status_code = status.HTTP_200_OK, tags = ["User"])
def get_user_data(id,db: Session=Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id).first()

    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The user with the id {id} not exists - status: {status.HTTP_404_NOT_FOUND}")
            )
    
    return user_data


@app.post("/user", response_model = schemas.User_View, status_code = status.HTTP_200_OK, tags = ["User"])
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_user = models.User(
        login = request.login,
        email = request.email,
        password = hashed_password,
        cpf = request.cpf
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"msg": f"The user {request.login} was created - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@app.delete("/user/{id}", tags = ["User"])
def destroy_user_data(id, db: Session=Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)

    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: id {id} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}")
            )

    try:
        db.commit()
        return {"msg": f"id {id} data was deleted from the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}