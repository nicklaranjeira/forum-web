from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated



app = FastAPI()


DATABASE_URL = "mysql+pymysql://root:@localhost:3306/forum_web"
engine = create_engine(DATABASE_URL, echo=True) # é o que mantém as conexões com o banco de dados.


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) # field default none deixa o id automatico
    titulo: str
    resumo: str
    conteudo: str
    autor: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Criação de Session 
# Uma Session é o que armazena os objetos na memória e acompanha as alterações necessárias nos dados, para então usar o engine para se comunicar com o banco de dados.

SessionDep = Annotated[Session, Depends(get_session)]

# criar as tabelas do banco de dados quando o aplicativo for iniciado.
@app.on_event("startup")
def on_startup():
    create_db_and_tables()