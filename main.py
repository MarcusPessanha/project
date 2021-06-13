from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app_credit import schemas, models, database, hashing


app = FastAPI()

models.Base.metadata.create_all(database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags = ['Index'])
def index():
    response = {"message": "Hello World"}
    return response


@app.get("/allpersons", tags = ["Person"])
def get_all_data(db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).all()
    address_data = db.query(models.Address_Data).all()
    debt_data = db.query(models.Debt_Data).all()

    if not personal_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The database is empty - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        return personal_data, address_data, debt_data


@app.get("/cpfid/{cpf}", status_code = status.HTTP_200_OK, tags = ["Person_CPF"])
def get_cpf_id(cpf, db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.cpf == cpf).first()
    if not personal_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The person with the cpf {cpf} not exists in the database - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        return personal_data


@app.get("/person/{id}", response_model = schemas.Person_View, status_code = status.HTTP_200_OK, tags = ["Person_id"])
def get_person_data(id, db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.id == id).first()
    address_data = db.query(models.Address_Data).filter(models.Address_Data.id == id).first()
    debt_data = db.query(models.Debt_Data).filter(models.Debt_Data.cpf == personal_data.cpf).all()
    if not personal_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The person with the id {id} not exists in the database - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        return schemas.Person_View(personal_info = personal_data, address_info = address_data, debt_info = debt_data)


@app.get("/cpfdata/{cpf}", response_model = schemas.Person_View, status_code = status.HTTP_200_OK, tags = ["Person_CPF"])
def get_cpf_data(cpf, db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.cpf == cpf).first()
    address_data = db.query(models.Address_Data).filter(models.Address_Data.cpf == cpf).first()
    debt_data = db.query(models.Debt_Data).filter(models.Debt_Data.cpf == cpf).all()
    if not personal_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The person with the id {cpf} not exists in the database - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        return schemas.Person_View(personal_info = personal_data, address_info = address_data, debt_info = debt_data)


@app.post("/person", status_code = status.HTTP_200_OK, tags = ["Person"])
def create_person_data(request: schemas.Person_In, db: Session=Depends(get_db)):
    person_check = db.query(models.Personal_Data).filter(models.Personal_Data.cpf == request.personal_info.cpf).first()
    if person_check:    
        raise HTTPException(status_code=404, detail= (
            f"msg: Person with the cpf {request.personal_info.cpf} already exists in database - status: - status: {status.HTTP_404_NOT_FOUND}"))

    personal_data = models.Personal_Data(
        cpf = request.personal_info.cpf,
        name = request.personal_info.name,
        surname = request.personal_info.surname,
        age = request.personal_info.age,
        creditcard_id = request.personal_info.creditcard_id,
        phone = request.personal_info.phone,)

    address_data = models.Address_Data(
        postal_code = request.address_info.postal_code,
        number = request.address_info.number,
        street = request.address_info.street,
        district = request.address_info.district,
        city_id = request.address_info.city_id,
        country = request.address_info.country,
        last_update = request.address_info.last_update,
        ##to do - Corrigir o relationship entre as tabelas do bd_1
        cpf = request.personal_info.cpf,
        )
        
    debt_data = models.Debt_Data(
        creditor = request.debt_info.creditor,
        debt_amount = request.debt_info.debt_amount,
        interest_rate = request.debt_info.interest_rate,
        ##to do - Corrigir o relationship entre as tabelas do bd_1
        cpf = request.personal_info.cpf,
        )
    try:
        db.add(personal_data)
        db.add(address_data)
        db.add(debt_data)
        db.commit()
        return {"msg": f"The person with the cpf {request.personal_info.cpf} was registered in the database - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@app.post("/debt", status_code = status.HTTP_200_OK, tags = ["Person_CPF"])
def create_debt_cpf(request: schemas.Debt_In, db: Session=Depends(get_db)):        
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.cpf == request.cpf).first()
    if not personal_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The person with the id {request.cpf} not exists in the database - status: {status.HTTP_404_NOT_FOUND}"))

    debt_data = models.Debt_Data(
        creditor = request.creditor,
        debt_amount = request.debt_amount,
        interest_rate = request.interest_rate,
        cpf = request.cpf)
    try:
        db.add(debt_data)
        db.commit()
        return {"msg": f"The debt: {request.debt_amount}, creditor: {request.creditor}, was registered to cpf {request.cpf} - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}

    
@app.delete("/person/{id}", tags = ["Person_id"])
def destroy_person_data(id, db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.id == id).first()
    if not personal_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: id {id} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))

    delete_person_data = db.query(models.Personal_Data).filter(models.Personal_Data.id == id).delete(synchronize_session=False)
    address_data = db.query(models.Address_Data).filter(models.Address_Data.id == id).delete(synchronize_session=False)
    debt_data = db.query(models.Debt_Data).filter(models.Debt_Data.cpf == personal_data.cpf).delete(synchronize_session=False)

    try:
        db.commit()
        return {"msg": f"id {id} data was deleted from the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@app.delete("/cpfdata/{cpf}", tags = ["Person_CPF"])
def destroy_cpf_data(cpf, db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.cpf == cpf).delete(synchronize_session=False)
    address_data = db.query(models.Address_Data).filter(models.Address_Data.cpf == cpf).delete(synchronize_session=False)
    debt_data = db.query(models.Debt_Data).filter(models.Debt_Data.cpf == cpf).delete(synchronize_session=False)
    if not personal_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: cpf {cpf} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))
    try:
        db.commit()
        return {"msg": f"cpf {cpf} data was deleted from the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@app.put("/person/{id}", status_code=status.HTTP_202_ACCEPTED, tags = ["Person_id"])
def update_person_data(id, request: schemas.Person_Update, db: Session=Depends(get_db)):
    personal_data = db.query(models.Personal_Data).filter(models.Personal_Data.id == id)
    address_data = db.query(models.Address_Data).filter(models.Address_Data.id == id)
    debt_data = db.query(models.Debt_Data).filter(models.Debt_Data.id == id)

    if not personal_data.first():
        raise HTTPException(status_code=404, detail= (
            f"msg: id {id} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        personal_data.update({
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
def get_all_user(db: Session=Depends(get_db)):
    user_data = db.query(models.User).all()
    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: No user was found in the database - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        return user_data


@app.get("/user/{id}", response_model = schemas.User_View, status_code = status.HTTP_200_OK, tags = ["User"])
def get_user_data(id,db: Session=Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id).first()

    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: The user with the id {id} not exists - status: {status.HTTP_404_NOT_FOUND}"))
    else:
        return user_data


@app.post("/user", status_code = status.HTTP_200_OK, tags = ["User"])
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


@app.delete("/user/{id}", tags = ["User"])
def destroy_user_data(id, db: Session=Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)

    if not user_data:
        raise HTTPException(status_code=404, detail= (
            f"msg: id {id} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))
    try:
        db.commit()
        return {"msg": f"id {id} data was deleted from the database - status: {200}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}