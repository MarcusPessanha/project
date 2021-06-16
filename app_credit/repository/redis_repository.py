from fastapi import status
from ..database_config.redis_config import redis
from ..extra.support import Support



def get_all_keys():
    try:
        response = redis.keys()        
        return response
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


def get_last_query(cpf):
    try:
        last_query = redis.get(key= f'{cpf}_query', serialization=True)        
        return last_query
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


def post_bureau_query(request):
    cpf = request.cpf
    bureau_postal_code = request.bureau_postal_code
    last_query = Support.get_time()
    value = {'cpf': cpf, 'bureau_postal_code': bureau_postal_code, 'datetime': last_query}
    try:
        redis.set(key= f'{cpf}_query', value= value, serialization=True)
        return {"msg": f"successfully registered - status: {status.HTTP_201_CREATED}"}
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


def get_last_purchase(cpf):
    try:
        response = redis.get(key= f'{cpf}_purchase', serialization=True)        
        return response
    except Exception as e:
        return {"msg": f"Something goes wrong - Exception: {e}"}


def post_purchase(request):
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