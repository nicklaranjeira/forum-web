from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "titulo": "Meu primeiro post",
        "resumo": "Resumo...",
        "conteudo": "Conteúdo completo...",
        "autor": "Carlos"
    }
]

#vizualização
@app.get("/", response_class=HTMLResponse)
async def editar_post(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts":posts})


#criação
@app.post("/create")
async def criar_post(request: Request):
    form = await request.form()
    novo_post = {
        "id": len(posts) + 1,
        "titulo": form.get("titulo"),
        "resumo": form.get("resumo"),
        "conteudo": form.get("conteudo"),
        "autor": form.get("autor"),
    }
    posts.append(novo_post)
 
    return RedirectResponse(url="/", status_code=303)

@app.get("/create", response_class=HTMLResponse)
async def criar_post(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={"posts":posts})

# edição 
@app.get("/edit", response_class=HTMLResponse)
def editar_post(request:Request):
         return templates.TemplateResponse(
         request=request,
         name="edit.html",
         context={"posts":posts})



@app.post("/edit", response_class=HTMLResponse)
async def editar_post(request: Request):
    form = await request.form()
    id = int(form.get("id"))
    
    for post in posts:
        if post["id"] == id:
            post["titulo"] = form["titulo"]
            post["resumo"] = form["resumo"]
            post["conteudo"] = form["conteudo"]
            post["autor"] = form["autor"]


#deletar 
@app.get("/delete", response_class=HTMLResponse)
def excluir_post(request:Request):
        return templates.TemplateResponse(
        request=request,
        name="delete.html",
        context={"posts":posts})
    
@app.post("/delete", response_class=HTMLResponse)
async def excluir_post(request:Request):
 
    form = await request.form()
    id = int(form.get("id"))
    print(id)

    for post in posts:
        if post["id"] == id:
            posts.remove(post)
            break
    return RedirectResponse(url="/", status_code=303)

