from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, MapAttribute


class Score(Model):
    class Meta:
        table_name = "score"

    cpf = UnicodeAttribute(hash_key=True)
    salary = NumberAttribute()
    # patrimony = MapAttribute()
    occupation = UnicodeAttribute()    
    postal_code = UnicodeAttribute()
    