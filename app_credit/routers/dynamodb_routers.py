from fastapi import APIRouter, status, HTTPException
from ..service.score_service import ScoreService
from ..schema.Score_schema import Score_Info

router = APIRouter()


# @router.post("/score", tags = ["Score_Data"])
# def create_score_data():
#     # Score.create_table(read_capacity_units=5, write_capacity_units=5)
#     person = Score("12397101785", 20000)
#     person.postal_code = '444444444'    
#     person.patrimony = {'carro': 50, 'ovelha': 30}
#     person.occupation = 'Motorista'
#     # person.age = 30
#     # person.patrimony = 1000000000

    # person.save()

    # return 'Sucess'

@router.get("/allscore/", tags = ["Score_Data"])
def all_data():
    return ScoreService.get_all_data()

@router.get("/scorecpf/", tags = ["Score_Data"])
def cpf_data(cpf:int):
    return ScoreService.get_cpf_data(cpf)

@router.post("/scorecpf/", tags = ["Score_Data"])
def create_cpf_data(request: Score_Info):
    return ScoreService.post_cpf_data(request)

@router.delete("/scorecpf/", tags = ["Score_Data"])
def delete_cpf_data(cpf:int):
    return ScoreService.delete_cpf_data(cpf)


@router.delete("/deleteall/", tags = ["Score_Data"])
def delete_table():
    return ScoreService.flush()