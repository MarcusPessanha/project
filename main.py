from fastapi import FastAPI, Depends, status
from app_credit.models import postgre_models as models
from app_credit.database_config.postgre_config import engine, get_db
from app_credit.routers import redis_routers, dynamodb_routers, postgre_routers

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.get("/health", tags = ['Health'])
def health(session: bool = Depends(get_db)):
    if session:
        return f'Postgre db Connected successfully status: {status.HTTP_200_OK}'
    else:
        return 'Message to help with error' 


app.include_router(postgre_routers.router)
app.include_router(redis_routers.router)
app.include_router(dynamodb_routers.router)