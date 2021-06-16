from fastapi import APIRouter, status
from ..schema.redis_schemas import Redis_Query, Redis_Purchase

from ..repository import redis_repository

router = APIRouter()


@router.get("/allkeys", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def all_data():
    return redis_repository.get_all_keys()


@router.get("/bureau/{cpf}", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def last_query(cpf: int):
    return redis_repository.get_last_query(cpf)


@router.post("/bureau", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def create_bureau_query(request: Redis_Query):
    return redis_repository.post_bureau_query(request)


@router.get("/purchase/{cpf}", status_code = status.HTTP_200_OK, tags = ["Purchases"])
def last_purchase(cpf: int):
    return redis_repository.get_last_purchase(cpf)


@router.post("/purchase", status_code = status.HTTP_200_OK, tags = ["Purchases"])
def create_purchase(request: Redis_Purchase):
    return redis_repository.post_purchase(request)