## START ##

 - create your virtualenv
 - pip3 install -r requirements.txt
 
 - alembic init alembic
 - docker run --name postgres_name -p 5432:5432 -e POSTGRES_PASSWORD=postgrespassword -e POSTGRES_DB=name -v /db_data:/var/lib/postgresql/db_data -d postgres
 - alembic revision -m "init"
 - alembic upgrade head

 - uvicorn main:app
 - localhost:8000/docs     
 or      
  - localhost:8000/redoc