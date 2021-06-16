from fastapi import APIRouter, status, HTTPException

from ..database_config.dynamodb_config import ScoreData

from pynamodb.attributes import UnicodeAttribute, NumberAttribute

router = APIRouter()


@router.post("/score", tags = ["Score_Data"])
def create_score_data():
    ScoreData.create_table(read_capacity_units=5, write_capacity_units=5)
    person = ScoreData("Tricoteira", 20000)
    person.cpf = "12397101785"
    # person.age = 30
    # person.patrimony = 1000000000

    person.save()

    return 'Sucess'

@router.get("/scoreget/", tags = ["Score_Data"])
def last_query(cpf: str):
    # teste = ScoreData.exists()
    # return teste
    # for user in ScoreData.query("Denver", ScoreData.first_name.startswith("J")):
    #     teste = user.first_name
    #     return  type(teste)
    # teste = ScoreData.query("Denver", ScoreData.first_name.startswith("J"))
    # tables = ScoreData.first_name
    teste_2 = ScoreData.scan()
    return teste_2