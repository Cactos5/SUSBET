from datetime import date, datetime
from mensagens import *
from encript import *
from fastapi import APIRouter, Form, Request, Depends, Path
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from banco import * 

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/perfil")
def get_perfil(request: Request):

    usuario_sessao = request.session.get("usuario")
    if not usuario_sessao or "email" not in usuario_sessao:
        response = RedirectResponse("/login", 303)
        msg_erro(response, "Você precisa estar autenticado para acessar o perfil.")
        return response

    email = usuario_sessao["email"]

    banco_de_dados = BancoDeDados()
    usuario = banco_de_dados.obter_dados_por_email(email)
    
    if not usuario:
        response = RedirectResponse("/login", 303)
        msg_erro(response, "Usuário não encontrado. Faça login novamente.")
        return response

    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "usuario": usuario
    })

