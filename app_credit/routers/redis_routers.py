from fastapi import APIRouter, status
from ..schema.redis_schemas import Redis_Query, Redis_Purchase

from ..service import cache_service

router = APIRouter()


@router.get("/allkeys", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def all_data():
    return cache_service.get_all_keys()


@router.get("/bureau/{cpf}", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def last_query(cpf: int):
    return cache_service.get_last_query(cpf)


@router.post("/bureau", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def create_bureau_query(request: Redis_Query):
    return cache_service.post_bureau_query(request)


@router.get("/purchase/{cpf}", status_code = status.HTTP_200_OK, tags = ["Purchases"])
def last_purchase(cpf: int):
    return cache_service.get_last_purchase(cpf)


@router.post("/purchase", status_code = status.HTTP_200_OK, tags = ["Purchases"])
def create_purchase(request: Redis_Purchase):
    return cache_service.post_purchase(request)