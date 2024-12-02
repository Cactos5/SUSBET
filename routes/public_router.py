from datetime import date, datetime
from mensagens import *
from encript import *
from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from banco import BancoDeDados, Usuario
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_root(request: Request):
    contexto = {"request": request, "index_ativo": "active"}
    return templates.TemplateResponse("index.html", contexto)


@router.get("/perfil")
def get_perfil(request: Request):
    usuario_id = request.session.get("id")  # Obtém o ID do usuário da sessão
    if not usuario_id:
        # Redireciona para a página de login se não estiver logado
        response = RedirectResponse(url="/login", status_code=303)
        response.set_cookie(key="mensagem", value="Faça login para acessar seu perfil.", httponly=True)
        return response

    # Obtém os dados do usuário
    banco = BancoDeDados()
    usuario = banco.obter_por_id(usuario_id)
    if not usuario:
        # Redireciona para a página de erro se o usuário não for encontrado
        response = RedirectResponse(url="/erro", status_code=303)
        response.set_cookie(key="mensagem", value="Usuário não encontrado.", httponly=True)
        return response

    # Renderiza o template do perfil do usuário
    return templates.TemplateResponse(
        "perfil.html",
        {"request": request, "usuario": usuario},
    )


@router.get("/sair")
def get_sair(request: Request):
    request.session.clear()
    response = RedirectResponse("/", status_code=303)
    msg_info(response, "Você não está mais autenticado.")
    return response


@router.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/post_login")
def post_login(
    request: Request, 
    email: str = Form(), 
    senha: str = Form()
):
    banco = BancoDeDados()
    senha_crpt = banco.obter_senha_por_email(email)

    if not senha_crpt:
        response = RedirectResponse("/login", status_code=303)
        msg_erro(response, "Credenciais inválidas!")
        return response

    if not bcrypt.checkpw(senha.encode(), senha_crpt if isinstance(senha_crpt, bytes) else senha_crpt.encode()):
        response = RedirectResponse("/login", status_code=303)
        msg_erro(response, "Credenciais inválidas!")
        return response

    usuario = banco.obter_dados_por_email(email)
    if not usuario:
        response = RedirectResponse("/login", status_code=303)
        msg_erro(response, "Usuário não encontrado!")
        return response

    # Salva dados do usuário na sessão
    request.session["usuario_id"] = usuario.id
    response = RedirectResponse("/", status_code=303)
    msg_sucesso(response, f"Olá, <b>{usuario.nome}</b>. Você está autenticado!")
    return response


@router.get("/cadastrar")
def get_cadastrar(request: Request):
    return templates.TemplateResponse("cadastrar.html", {"request": request})


@router.get("/cadastrar_recebido")
def post_cadastrar_recebido(request: Request):
    return templates.TemplateResponse("cadastrar_recebido.html", {"request": request})


@router.post("/post_cadastrar")
def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    data_nascimento: date = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    telefone: str = Form(...),
    endereco: str = Form(...),
    senha: str = Form(...),
    confirmacao_senha: str = Form(...),
):
    if senha != confirmacao_senha:
        response = RedirectResponse("/cadastrar", status_code=303)
        msg_erro(response, "Senha e confirmação de senha não conferem.")
        return response

    senha_crpt = cript(senha)
    if isinstance(senha_crpt, bytes):
        senha_crpt = senha_crpt.decode()

    novo_usuario = Usuario(
        id=None,
        nome=nome,
        data_nascimento=data_nascimento,
        email=email,
        cpf=cpf,
        telefone=telefone,
        endereco=endereco,
        senha=senha_crpt,
        tipo_usuario="cliente",
    )

    if novo_usuario:
        banco = BancoDeDados()
        banco.cadastrar_usuario(novo_usuario)
        response = RedirectResponse("/login", status_code=303)
        msg_sucesso(response, "Cadastro realizado com sucesso! Use suas credenciais para login.")
        return response

    response = RedirectResponse("/cadastrar", status_code=303)
    msg_erro(response, "Ocorreu algum problema ao tentar realizar seu cadastro. Tente novamente.")
    return response


@router.get("/instituicoes")
def get_instituicoes_mapa(request: Request):
    contexto = {"request": request, "instituicoes_ativo": "active"}
    return templates.TemplateResponse("mapa.html", contexto)


@router.get("/agenda")
def get_agenda(request: Request):
    return templates.TemplateResponse("agenda.html", {"request": request})
