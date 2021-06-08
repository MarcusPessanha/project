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
def get_all_data(response: Response, db: Session=Depends(get_db)):
    Personal_Data = db.query(models.Personal_Data).all()
    # Address_Data = db.query(models.Address_Data).all()
    if not Personal_Data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"The database is empty - status: {response.status_code}"}
    return Personal_Data#, Address_Data


@app.get("/person/{id}", response_model = schemas.Person_View, status_code = status.HTTP_200_OK, tags = ["Person"])
def get_person_data(id, response: Response, db: Session=Depends(get_db)):
    Personal_Data = db.query(models.Personal_Data).filter(models.Personal_Data.id == id).first()
    # Address_Data = db.query(models.Address_Data).filter(models.Address_Data.id == id).first()
    if not Personal_Data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"The person with the id {id} not exists in the database - status: {response.status_code}"}
    
    return Personal_Data#, Address_Data 


@app.post("/person", status_code = status.HTTP_200_OK, tags = ["Person"])
def create_person_data(request: schemas.Person, db: Session=Depends(get_db)):
    personal_data = models.Personal_Data(
        cpf = request.cpf,
        name = request.name,
        surname = request.name,
        age = request.age,
        creditcard_id = request.creditcard_id,
        phone = request.phone,
        person_id = 1                            #atrelar ao cpf
    )
    address_data = models.Address_Data(
        postal_code = request.postal_code,
        street = request.street,
        district = request.district,
        city_id = request.city_id,
        country = request.country,
        last_update = request.last_update
    )
    try:
        db.add(personal_data)
        db.commit()
        db.refresh(personal_data)
        db.add(address_data)
        db.commit()
        db.refresh(address_data)
        return {"msg": f"The person of cpf {request.cpf} was registered in the database - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}

    
@app.delete("/person/{id}", tags = ["Person"])
def destroy_person_data(id, response: Response, db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.id == id).delete(synchronize_session=False)
    address_data = db.query(models.Address_Data).filter(models.Address_Data.id == id).delete(synchronize_session=False)

    if not personal_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"id {id} does not exist in database - status: - status: {response.status_code}"}

    try:
        db.commit()
        return {"msg": f"id {id} data was deleted from the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@app.put("/person/{id}", status_code=status.HTTP_202_ACCEPTED, tags = ["Person"])
def update_person_data(id, response: Response, request: schemas.Person, db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.id == id)
    address_data = db.query(models.Address_Data).filter(models.Address_Data.id == id)
    
    if not personal_data.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"id {id} does not exist in database - status: - status: {response.status_code}"}
    else:
        personal_data.update({
        "cpf": request.cpf,
        "name": request.name,
        "surname":request.surname,
        "age": request.age,
        "creditcard_id": request.creditcard_id,
        "phone": request.phone
        },synchronize_session=False
    )
        address_data.update({
        "street": request.street,
        "district": request.district,
        "city_id": request.city_id,
        "country": request.country,
        "last_update": request.last_update
        },synchronize_session=False
    )

    try:
        db.commit()
        return {"msg": f"id {id} data was updated in the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@app.get("/users", tags = ["User"])
def get_all_user(response: Response, db: Session=Depends(get_db)):
    user_data = db.query(models.User).all()
    if not user_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": f"No user was found in the database - status: {response.status_code}"}
    return user_data


@app.get("/user/{id}", response_model = schemas.User_View, status_code = status.HTTP_200_OK, tags = ["User"])
def get_user_data(id,db: Session=Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id).first()

    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The user with the id {id} not exists - status: {status.HTTP_404_NOT_FOUND}")
            )
    
    return user_data


@app.post("/user", status_code = status.HTTP_200_OK, tags = ["User"])
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