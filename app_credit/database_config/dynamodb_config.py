from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute




class ScoreData(Model):
    class Meta:
        table_name = "Occupation_Salary"

    occupation = UnicodeAttribute(hash_key=True)
    salary = NumberAttribute(range_key=True)
    cpf = UnicodeAttribute()    

