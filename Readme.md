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
 - alembic revision -m "init"
 - alembic upgrade head

 ### You can also start only the postgre container
  - db_postgres.bat 


# Sobre o Projeto:
  API utilizando Python 3.8.7 com fastAPI framework. Escolhi o fastAPI por ser um framework moderno que 
eu tinha interesse em aprender.
## Armazenazenamento:
  Todos os bancos foram implementados em containers Docker usando o Docker Compose.
### BASE A 
  A base de dados "A" seria utilizada para dados sensíveis e que precisam de altos níveis de segurança. Essa base não 
teria a necessidade de acesso rápido. 
A escolha foi o PostgreSQL por ser um BD seguro, que possui mais de 15 anos de desenvolvimento ativo e 
de alta reputação devido a sua estabilidade e integridade de dados.

  /alembic
  Cria as migrações para a BASE A (PostgreSQL)

### BASE B 
  A base de dados "B" seria utilizada para dados sensíveis também mas que necessitam de um acesso mais rápido que a base "A".
Essa base "B" também seria utilizada para algorítmos de aprendizado de máquina.
A escolha foi o Dynamodb por ser um BD performático e ao mesmo tempo seguro já que é controlado por tokens de acesso da AWS.
Esse BD também tem como característica um NoSQL Elástico, o que permite escalagem com alta performance e modelagens inteligentes 
que favorecem a disponibilidade de consultas rápidas e estáveis, o que seria ótimo para machine learning.
Esse banco normalmente é utilizado acessando a nuvem da AWS mas nesse projeto ele está implementando localmente com Docker.

  /docker/dynamodb
  Armazena localmente o .db gerado pelo dynamodb. 

### BASE C 
  A base de dados "C" seria utilizada para dados não críticos mas que precisariam de acesso extremamente rápido.
A escolha foi o Redis por ser um banco NoSQL que armazena dados em memória sendo extremamente rápido 
e de fácil implementação.


# Dentro de /app_credit temos:
### /database_config ###
Possui as configurações de conexão com os bancos de dados.

### /extra ###
Possui funções auxiliares para criptografia e hora atual.

### /models ###
Possui os modelos que representarão as tabelas dos bancos de dados .

### /routes ###
Recebe as requisições HTTP e executa funções para o respectivo enpoint chamado.

### /schema ###
Responsável por aplicar as regras de negócio onde os models serão aplicados, 
limitando atributos dos models, e dependendo de onde será aplicado faz o relacionamento entre os models.

### /service ###
Gerencia a lógica da regra de negócio e são chamados logo após o router para manipular, validar, ativar funções e atribuir 
informações aos objetos, e com isso gerar eventos no banco de dados como criação, obtenção, edição e exclusão de informações.