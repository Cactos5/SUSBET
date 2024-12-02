def add_msg(response, mensagem, tipo):
    response.set_cookie(
        key=f"mensagem_{tipo}",
        value=mensagem,
        max_age=3,
        httponly=True,
        samesite="strict",
    )

def msg_sucesso(response, mensagem):
    add_msg(response, mensagem, "sucesso")

def msg_info(response, mensagem):
    add_msg(response, mensagem, "info")

def msg_aviso(response, mensagem):
    add_msg(response, mensagem, "aviso")

def msg_erro(response, mensagem):
    add_msg(response, mensagem, "erro")