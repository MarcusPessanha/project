from fastapi import HTTPException
from ..models.Score import Score


# ToDo - Acertar as respostas usando os schemas apropriados
class ScoreService(object):
    @staticmethod
    def get_all_data():
        scan_tables = Score.scan()
        if scan_tables:
            return scan_tables                
        else: 
            raise HTTPException(status_code=404, detail= (
                f"msg: No user was found in the database - status: {status.HTTP_404_NOT_FOUND}"))

    @staticmethod
    def get_cpf_data(cpf: str):
        person_data = Score.query(f"{cpf}")
        return person_data

    @staticmethod
    def post_cpf_data(request):
        if not Score.exists():
            Score.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)

        person_data = Score(str(request.cpf))
        person_data.salary = request.salary
        person_data.occupation = request.occupation
        person_data.postal_code = request.postal_code

        return person_data.save()    
    
    @staticmethod
    def delete_cpf_data(cpf: str):
        person_data = Score(str(cpf))
        print(person_data)
        if person_data:
            person_data.delete()
            return "The f'{cpf} Score data was deleted"
        else: 
            raise HTTPException(status_code=404, detail= (
                f"msg: No user was found in the database - status: {status.HTTP_404_NOT_FOUND}"))

    @staticmethod
    def flush():
        try:
            Score.delete_table()
            return "The Score table was deleted"
        except Exception as e:
            return {"msg": f"Something goes wrong - Exception: {e}"}
