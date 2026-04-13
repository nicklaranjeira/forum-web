# 📌 Projeto: Fórum Web com FastAPI

## 📖 Descrição

Este projeto é uma aplicação web simples de fórum desenvolvida com **FastAPI**, onde é possível:

* Criar posts
* Visualizar posts
* Editar posts
* Excluir posts

Os dados são armazenados **em memória (sem banco de dados)**, conforme o requisito do projeto.

---

## 🚀 Tecnologias utilizadas

* Python
* FastAPI
* Jinja2 (templates HTML)
* HTML/CSS
---

## 📂 Estrutura do projeto

```
forum web/
│
├── app.py              # Arquivo principal da aplicação
├── templates/          # Páginas HTML (Jinja2)
│   ├── index.html
│   ├── create.html
│   ├── edit.html
│   └── delete.html
│
├── static/             # Arquivos estáticos (CSS, imagens, etc.)
│
└── venv/               # Ambiente virtual (não recomendado subir no Git)
```


### 🔹 Rotas principais

| Método | Rota      | Função           |
| ------ | --------- | ---------------- |
| GET    | `/`       | Listar posts     |
| GET    | `/create` | Tela de criação  |
| POST   | `/create` | Criar post       |
| GET    | `/edit`   | Tela de edição   |
| POST   | `/edit`   | Atualizar post   |
| GET    | `/delete` | Tela de exclusão |
| POST   | `/delete` | Remover post     |

---



## 👩‍💻 Autora

Projeto desenvolvido por **Nicolle Laranjeira** 💙
