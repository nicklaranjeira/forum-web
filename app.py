from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi.staticfiles import StaticFiles


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

@app.get("/", response_class=HTMLResponse)
async def editar_post(request:Request, session:SessionDep):
    posts = session.exec(select(Post)).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts":posts})

@app.post("/create")
async def criar_post(request: Request, session:SessionDep):
    form = await request.form()
    novo_post = Post(
        titulo = form.get("titulo"),
        resumo = form.get("resumo"),
        conteudo = form.get("conteudo"),
        autor = form.get("autor"),
    )
    session.add(novo_post)
    session.commit()
 
    return RedirectResponse(url="/", status_code=303)

@app.get("/create", response_class=HTMLResponse)
async def tela_criar_post(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html"
    )

@app.get("/edit", response_class=HTMLResponse)
def editar_post(request:Request, session:SessionDep):
        posts = session.exec(select(Post)).all() # busca o context post dentro do bd

        return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"posts":posts})

@app.post("/edit")
async def editar_post(request: Request, session: SessionDep):
    form = await request.form()
    id = int(form.get("id"))

    post = session.get(Post, id)

    if post:
        post.titulo = form.get("titulo")
        post.resumo = form.get("resumo")
        post.conteudo = form.get("conteudo")
        post.autor = form.get("autor")

        session.add(post)
        session.commit()

    return RedirectResponse(url="/", status_code=303)


@app.get("/delete", response_class=HTMLResponse)
async def tela_criar_post(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="delete.html"
    )


@app.post("/delete")
async def excluir_post(request: Request, session: SessionDep):
   
    form = await request.form()
    id = int(form.get("id"))

    post = session.get(Post, id)

    if post:
        session.delete(post)
        session.commit()

    return RedirectResponse(url="/", status_code=303)

# app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# posts = [
#     {
#         "id": 1,
#         "titulo": "Meu primeiro post",
#         "resumo": "Resumo...",
#         "conteudo": "Conteúdo completo...",
#         "autor": "Carlos"
#     }
# ]


# #vizualização
# @app.get("/", response_class=HTMLResponse)
# async def editar_post(request:Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html",
#         context={"posts":posts})


# #criação
# @app.post("/create")
# async def criar_post(request: Request):
#     form = await request.form()
#     novo_post = {
#         "id": len(posts) + 1,
#         "titulo": form.get("titulo"),
#         "resumo": form.get("resumo"),
#         "conteudo": form.get("conteudo"),
#         "autor": form.get("autor"),
#     }
#     posts.append(novo_post)
 
#     return RedirectResponse(url="/", status_code=303)

# @app.get("/create", response_class=HTMLResponse)
# async def criar_post(request:Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="create.html",
#         context={"posts":posts})

# # edição 
# @app.get("/edit", response_class=HTMLResponse)
# def editar_post(request:Request):
#          return templates.TemplateResponse(
#          request=request,
#          name="edit.html",
#          context={"posts":posts})



# @app.post("/edit", response_class=HTMLResponse)
# async def editar_post(request: Request):
#     form = await request.form()
#     id = int(form.get("id"))
    
#     for post in posts:
#         if post["id"] == id:
#             post["titulo"] = form["titulo"]
#             post["resumo"] = form["resumo"]
#             post["conteudo"] = form["conteudo"]
#             post["autor"] = form["autor"]

#     return RedirectResponse(url="/", status_code=303)


# #deletar 
# @app.get("/delete", response_class=HTMLResponse)
# def excluir_post(request:Request):
#         return templates.TemplateResponse(
#         request=request,
#         name="delete.html",
#         context={"posts":posts})
    
# @app.post("/delete", response_class=HTMLResponse)
# async def excluir_post(request:Request):
 
#     form = await request.form()
#     id = int(form.get("id"))
#     print(id)

    
#     for post in posts:
#         if post["id"] == id:
#             posts.remove(post)
#             break
    
#     return RedirectResponse(url="/", status_code=303)

