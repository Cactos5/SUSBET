from datetime import date, datetime
from mensagens import *
from encript import *
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from banco import * 

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_root(request: Request):
    contexto = {"request": request, "index_ativo": "active"}
    return templates.TemplateResponse("index.html", contexto)


@router.get("/checkup")
def get_check(request: Request):
    contexto = {"request": request, "checkup_ativo": "active"}
    return templates.TemplateResponse("consulta.html", contexto)

@router.get("/sair")
def get_sair(request: Request):
    request.session.clear()
    response = RedirectResponse("/", 303)
    msg_info(response, "Você não está mais autenticado.")
    return response


@router.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/post_login")
def post_login(
    request: Request, 
    email: str = Form(),
    senha: str = Form()):
    
    banco_de_dados = BancoDeDados()  # Criação da instância
    
    senha_crpt = banco_de_dados.obter_senha_por_email(email)  # Usando a instância para chamar o método
    
    if not senha_crpt:
        response = RedirectResponse("/login", 303)
        return response
    
    if not bcrypt.checkpw(senha.encode(), senha_crpt if isinstance(senha_crpt, bytes) else senha_crpt.encode()):
        response = RedirectResponse("/login", 303)
        msg_erro(response, "Credenciais inválidas!")
        return response
    
    usuario = banco_de_dados.obter_dados_por_email(email)
    
    if not usuario:  # Verifica se o usuário existe
        response = RedirectResponse("/login", 303)
        msg_erro(response, "Usuário não encontrado!")
        return response
    
    request.session["usuario"] = {
        "nome": usuario.nome,
        "email": usuario.email, 
        "tipo_usuario": usuario.tipo_usuario
    }
    
    response = RedirectResponse("/", 303)
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

    try:
    
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
            tipo_usuario="cliente"
        )
        print(novo_usuario)

        
        banco = BancoDeDados()  
        sucesso = banco.cadastrar_usuario(novo_usuario)  
        
        if sucesso:
            response = RedirectResponse("/login", status_code=303)
            msg_sucesso(response, "Cadastro realizado com sucesso! Use suas credenciais para login.")
            return response
        else:
            raise Exception("Erro ao inserir o usuário no banco de dados.")
    
    except Exception as e:
        print(f"Erro durante o cadastro: {e}")
        response = RedirectResponse("/cadastrar", status_code=303)
        msg_erro(response, "Ocorreu um problema ao tentar realizar seu cadastro. Tente novamente.")
        return response

@router.get("/instituicoes")
def get_instituicoes_mapa(request: Request):
    contexto = {"request": request, "instituicoes_ativo": "active"}
    return templates.TemplateResponse("mapa.html", contexto)

@router.get("/agenda")
def get_root(request: Request):
    return templates.TemplateResponse("agenda.html", {"request": request})
