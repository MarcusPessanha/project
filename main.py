from fastapi import FastAPI, Depends, status, HTTPException
from app_credit import models
from app_credit.database import engine, get_db
from app_credit.routers import person, user
from app_credit.databases.redis import redis_routers

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.get("/health", tags = ['Health'])
def health(session: bool = Depends(get_db)):
    if session:
        return f'Postgre db Connected successfully status: {status.HTTP_200_OK}'
    else:
        return 'Message to help with error' 


app.include_router(person.router)
app.include_router(user.router)
app.include_router(redis_routers.router)