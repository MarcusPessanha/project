# START 

## Create you environment:
 - create your virtualenv
 - pip3 install -r requirements.txt

### Install the AWS SAM CLI to use Dynamodb
  - Step 4 in: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-windows.html
  - Go to AWS "MyAccount -> security credentials" and generate your aws access key id and aws secret access key
  - Use the command- aws configure -to configure your credentials
  - You can also configure your credentials byr modifying this file C:\Users\<user>\.aws

## Docker compose:
 - docker-compose up

## Start server:
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
