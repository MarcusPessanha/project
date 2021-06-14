from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./app_credit/data/app_credit.db'

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgrespassword@localhost/postgres"

docker_machine_ip = "192.168.99.100"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgrespassword@{docker_machine_ip}/postgres"

# connect_args={"check_same_thread": False} só é usado para sqlite. Esse parâmetro não é necessário para outros db.
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()