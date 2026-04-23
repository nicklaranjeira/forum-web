from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi.staticfiles import StaticFiles

from dao import *


app = FastAPI()
templates = Jinja2Templates(directory="templates")


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