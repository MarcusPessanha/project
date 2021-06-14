# START 

## Create you environment:
 - create your virtualenv
 - pip3 install -r requirements.txt

## Docker compose:
 - docker-compose up

## Server start:
- uvicorn main:app

## Swagger Interface Description:
 - localhost:8000/docs     
 or      
  - localhost:8000/redoc

### You can also make new migrations to postgreSQL db:
 - alembic init alembic
 #### You can also start only the postgre container
 - db_postgres.bat 
 - alembic revision -m "init"
 - alembic upgrade head
