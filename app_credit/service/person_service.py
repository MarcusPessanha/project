from fastapi import status, HTTPException


from ..extra.support import Support
from ..models.Address import Address
from ..models.Debt import Debt
from ..models.Personal import Personal
from ..schema.Person_schema import Person_View


class PersonService(object):

    @staticmethod
    def get_all_data(db):

        personal_data = db.query(Personal).all()
        address_data = db.query(Address).all()
        debt_data = db.query(Debt).all()

        if not personal_data:
            raise HTTPException(status_code=404, detail=(
                f"msg: The database is empty - status: {status.HTTP_404_NOT_FOUND}"))
        else:
            return personal_data, address_data, debt_data

    @staticmethod
    def get_cpf_id(cpf, db):
        personal_data = db.query(Personal).filter(
            Personal.cpf == cpf).first()
        if not personal_data:
            raise HTTPException(status_code=404, detail=(
                f"msg: The person with the cpf {cpf} not exists in the database - status: {status.HTTP_404_NOT_FOUND}"))
        else:
            return personal_data

    @staticmethod
    def get_id_data(id, db):
        personal_data = db.query(Personal).filter(
            Personal.id == id).first()
        if not personal_data:
            raise HTTPException(status_code=404, detail=(
                f"msg: The person with the id {id} not exists in the database - status: {status.HTTP_404_NOT_FOUND}"))
        else:
            try:
                address_data = db.query(Address).filter(
                    Address.id == id).first()
                debt_data = db.query(Debt).filter(
                    Debt.cpf == personal_data.cpf).all()
                return Person_View(personal_info=personal_data, address_info=address_data, debt_info=debt_data)
            except Exception as e:
                return {"msg": f"Something goes wrong - Exception: {e}"}

    @staticmethod
    def get_cpf_data(cpf, db):
        personal_data = db.query(Personal).filter(
            Personal.cpf == cpf).first()
        if not personal_data:
            raise HTTPException(status_code=404, detail=(
                f"msg: The person with the cpf {cpf} not exists in the database - status: {status.HTTP_404_NOT_FOUND}"))
        else:
            try:
                address_data = db.query(Address).filter(
                    Address.cpf == cpf).first()
                debt_data = db.query(Debt).filter(
                    Debt.cpf == cpf).all()
                return Person_View(personal_info=personal_data, address_info=address_data, debt_info=debt_data)
            except Exception as e:
                return {"msg": f"Something goes wrong - Exception: {e}"}

    @staticmethod
    def post_person_data(request, db):
        person_check = db.query(Personal).filter(
            Personal.cpf == request.personal_info.cpf).first()
        if person_check:
            raise HTTPException(status_code=404, detail=(
                f"msg: Person with the cpf {request.personal_info.cpf} already exists in database - status: - status: {status.HTTP_404_NOT_FOUND}"))

        personal_data = Personal(
            cpf=request.personal_info.cpf,
            name=request.personal_info.name,
            surname=request.personal_info.surname,
            age=request.personal_info.age,
            creditcard_id=request.personal_info.creditcard_id,
            phone=request.personal_info.phone,
        )
        address_data = Address(
            postal_code=request.address_info.postal_code,
            number=request.address_info.number,
            street=request.address_info.street,
            district=request.address_info.district,
            city_id=request.address_info.city_id,
            country=request.address_info.country,
            last_update=Support.get_date(),
            # ToDo: Corrigir o relationship entre as tabelas do bd_1
            cpf=request.personal_info.cpf,
        )
        debt_data = Debt(
            creditor=request.debt_info.creditor,
            debt_amount=request.debt_info.debt_amount,
            interest_rate=request.debt_info.interest_rate,
            # ToDo: Corrigir o relationship entre as tabelas do bd_1
            cpf=request.personal_info.cpf,
        )
        try:
            db.add(personal_data)
            db.add(address_data)
            db.add(debt_data)
            db.commit()
            return {
                "msg": f"The person with the cpf {request.personal_info.cpf} was registered in the database - status: {status.HTTP_201_CREATED}"}
        except Exception as e:
            return {"msg": f"Something goes wrong - Exception: {e}"}

    @staticmethod
    def post_person_debt(request, db):
        personal_data = db.query(Personal).filter(
            Personal.cpf == request.cpf).first()
        if not personal_data:
            raise HTTPException(status_code=404, detail=(
                f"msg: The person with the id {request.cpf} not exists in the database - status: {status.HTTP_404_NOT_FOUND}"))

        debt_data = Debt(
            creditor=request.creditor,
            debt_amount=request.debt_amount,
            interest_rate=request.interest_rate,
            cpf=request.cpf
        )
        try:
            db.add(debt_data)
            db.commit()
            return {
                "msg": f"The debt: {request.debt_amount}, creditor: {request.creditor}, was registered to cpf {request.cpf} - status: {status.HTTP_201_CREATED}"}
        except Exception as e:
            return {"msg": f"Something goes wrong - Exception: {e}"}

    @staticmethod
    def delete_id_data(id, db):
        personal_data = db.query(Personal).filter(
            Personal.id == id).first()
        if not personal_data:
            raise HTTPException(status_code=404, detail=(
                f"msg: id {id} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))
        else:
            try:
                delete_person_data = db.query(Personal).filter(
                    Personal.id == id).delete(synchronize_session=False)
                address_data = db.query(Address).filter(
                    Address.id == id).delete(synchronize_session=False)
                debt_data = db.query(Debt).filter(
                    Debt.cpf == personal_data.cpf).delete(synchronize_session=False)
                db.commit()
                return {"msg": f"id {id} data was deleted from the database - status: {200}"}
            except Exception as e:
                return {"msg": f"Something goes wrong - Exception: {e}"}

    @staticmethod
    def delete_cpf_data(cpf, db):
        personal_data = db.query(Personal).filter(
            Personal.cpf == cpf).delete(synchronize_session=False)
        if not personal_data:
            raise HTTPException(status_code=404, detail=(
                f"msg: cpf {cpf} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))
        else:
            try:
                address_data = db.query(Address).filter(
                    Address.cpf == cpf).delete(synchronize_session=False)
                debt_data = db.query(Debt).filter(Debt.cpf == cpf).delete(
                    synchronize_session=False)
                db.commit()
                return {"msg": f"cpf {cpf} data was deleted from the database - status: {200}"}
            except Exception as e:
                return {"msg": f"Something goes wrong - Exception: {e}"}

    @staticmethod
    def put_person_data(id, request, db):
        personal_data = db.query(Personal).filter(
            Personal.id == id)
        if not personal_data.first():
            raise HTTPException(status_code=404, detail=(
                f"msg: id {id} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))

        address_data = db.query(Address).filter(
            Address.id == id)
        debt_data = db.query(Debt).filter(Debt.id == id)

        personal_data.update({
            "name": request.name,
            "surname": request.surname,
            "age": request.age,
            "creditcard_id": request.creditcard_id,
            "phone": request.phone}, synchronize_session=False
        )
        address_data.update({
            "street": request.street,
            "district": request.district,
            "city_id": request.city_id,
            "country": request.country,
            "last_update": Support.get_date()}, synchronize_session=False
        )
        try:
            db.commit()
            return {"msg": f"id {id} data was updated in the database - status: {200}"}
        except Exception as e:
            return {"msg": f"Something goes wrong - Exception: {e}"}
