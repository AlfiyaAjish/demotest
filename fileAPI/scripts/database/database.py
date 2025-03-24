import configparser
from sqlmodel import create_engine, Session, SQLModel

# Load configurations
config = configparser.ConfigParser()
config.read("conf/application_conf.conf")

DATABASE_URL = config["database"]["url"]

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
