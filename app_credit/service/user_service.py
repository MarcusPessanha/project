from fastapi import status, HTTPException
from ..models import User as models
from ..database_config.postgre_config import get_db
from ..extra.hashing import Hash
from ..extra.support import Support


class UserService(object):

    @staticmethod
    def get_all_data(db):
        user_data = db.query(models.User).all()
        if not user_data:
            raise HTTPException(status_code=404, detail= (
                f"msg: No user was found in the database - status: {status.HTTP_404_NOT_FOUND}"))
        else:
            return user_data

    @staticmethod
    def get_user_data(id, db):
        user_data = db.query(models.User).filter(models.User.id == id).first()

        if not user_data:
            raise HTTPException(status_code=404, detail= (
                f"msg: The user with the id {id} not exists - status: {status.HTTP_404_NOT_FOUND}"))
        else:
            return user_data

    @staticmethod
    def post_user(request, db):
        hashed_password = Hash.bcrypt(request.password)
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

    @staticmethod
    def delete_user(id, db):
        user_data = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)

        if not user_data:
            raise HTTPException(status_code=404, detail= (
                f"msg: id {id} does not exist in database - status: - status: {status.HTTP_404_NOT_FOUND}"))
        try:
            db.commit()
            return {"msg": f"id {id} data was deleted from the database - status: {200}"}
        except Exception as e:
            return {"msg": f"Something goes wrong - Exception: {e}"}
