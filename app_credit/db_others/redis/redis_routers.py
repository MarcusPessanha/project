from fastapi import APIRouter, Depends, status, HTTPException

from .redis_config import Redis_Cache, redis
from .redis_schemas import Redis_Query, Redis_Purchase
from ... support import Support

router = APIRouter()


# ToDo: Melhorar mensagens de erro.  

@router.get("/allkeys", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def all_keys_data():
    try:
        response = redis.keys()        
        return response
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@router.get("/bureau/{cpf}", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def last_query(cpf: int):
    try:
        last_query = redis.get(key= f'{cpf}_query', serialization=True)        
        return last_query
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@router.post("/bureau", status_code = status.HTTP_200_OK, tags = ["Bureau_Queryes"])
def create_bureau_query(request: Redis_Query):
    cpf = request.cpf
    bureau_postal_code = request.bureau_postal_code
    last_query = Support.get_time()

    value = {'cpf': cpf, 'bureau_postal_code': bureau_postal_code, 'datetime': last_query}

    try:
        redis.set(key= f'{cpf}_query', value= value, serialization=True)
        
        return {"msg": f"successfully registered - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@router.get("/purchase/{cpf}", status_code = status.HTTP_200_OK, tags = ["Purchases"])
def last_purchase(cpf: int):
    try:
        response = redis.get(key= f'{cpf}_purchase', serialization=True)        
        return response
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


@router.post("/purchase", status_code = status.HTTP_200_OK, tags = ["Purchases"])
def create_purchase(request: Redis_Purchase):
    cpf = request.cpf
    creditcard_id = request.creditcard_id
    store = request.store
    store_postal_code = request.store_postal_code
    value = request.value
    datetime = Support.get_time()
    
    value = {
        'cpf': cpf, 
        'creditcard_id': creditcard_id,
        'store': store,
        'store_postal_code': store_postal_code,
        'value': value,
        'datetime': datetime        
        }

    try:
        redis.set(key= f'{cpf}_purchase', value= value, serialization=True)
        
        return {"msg": f"successfully registered - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}