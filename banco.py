from dataclasses import dataclass
from typing import Optional
import sqlite3
from queries import * 
from encript import * 

@dataclass
class Usuario:
    id: Optional[int] = None
    nome: Optional[str] = None
    data_nascimento: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[int] = None
    endereco: Optional[str] = None
    tipo_usuario: Optional[str] = None

class BancoDeDados:
    def __init__(self):
        self.path = 'database/database.db'
        self.conexao_banco = None
        self.cursor = None

    def conectar(self):
        try:
            self.conexao_banco = sqlite3.connect(self.path)
            # Configura o uso de Row para acessar os resultados como dicionários
            self.conexao_banco.row_factory = sqlite3.Row
            self.cursor = self.conexao_banco.cursor()
        except Exception as inst:
            print(f"Erro ao conectar no banco de dados: {inst}")
            
    def desconectar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao_banco:
            self.conexao_banco.close()

    def obter_senha_por_email(self, email: str) -> Optional[str]:
        try:
            self.conectar()
            self.cursor.execute(SQL_OBTER_SENHA_POR_EMAIL, (email,))
            dados = self.cursor.fetchone() 
            if dados is None:
                return None
            return dados["senha"]  
        except Exception as inst:
            print(f'Erro ao obter senha do banco de dados: {inst}')
        finally:
            self.desconectar()

    def obter_dados_por_email(self, email: str) -> Optional[Usuario]:
        try:
            self.conectar()
            self.cursor.execute(SQL_OBTER_DADOS_POR_EMAIL, (email,))
            dados = self.cursor.fetchone()
            if dados is None:
                return None
            return Usuario(**dados)  
        except Exception as inst:
            print(f'Erro ao obter dados do banco de dados: {inst}')
        finally:
            self.desconectar()
        
    def criar_banco(self):
        try:
            self.conectar()
            self.cursor.execute(SQL_CRIAR_TABELA)
            self.conexao_banco.commit()
        except Exception as inst:
            print(f'Erro ao criar a tabela no banco de dados: {inst}')  
        finally:
            self.desconectar()
            
    def cadastrar_usuario(self, user: Usuario):
        try:
            self.conectar()
            self.cursor.execute(SQL_INSERIR_USUARIO, (
            user.nome,
            user.data_nascimento,
            user.email,
            user.cpf,
            user.telefone,
            user.endereco,
            user.senha,
            user.tipo_usuario
        ))
            self.conexao_banco.commit()
        except Exception as inst:
            print(f'Erro ao inserir dados no banco de dados: {inst}')  
        finally:
            self.desconectar()
            
    def verificar_usuario(self, email: str, senha: str) -> bool:
        try:
            self.conectar()
            self.cursor.execute(SQL_VERIFICAR_USUARIO, (email, senha))
            resultado = self.cursor.fetchone()
            return bool(resultado)  
        except Exception as inst:
            print(f"Erro ao verificar o usuário no banco de dados: {inst}")
            return False
        finally:
            self.desconectar()


    def drop_banco(self):
        try:
            self.conectar()
            self.cursor.execute(SQL_DROP_TABLE)
            self.conexao_banco.commit()   
        except Exception as inst:
            print(f'Erro ao dropar tabela no banco de dados: {inst}')  
        finally:
            self.desconectar()


"""
usuarios_para_teste = [
    Usuario(
        nome="Marjory Novato",
        data_nascimento="13/06/2008",  # Corrigido: adicionado vírgula aqui
        email="marjory@dominio.com",
        senha=cript("senha123"),
        cpf="12345678901",
        telefone="31987654321",
        endereco="Rua A, 123 - Bairro Exemplo, Cidade/UF",
        tipo_usuario="cliente"
    ),
    Usuario(
        nome="Carlos Souza",
        data_nascimento="07/12/2003",
        email="carlos@dominio.com",
        senha=cript("senha456"),
        cpf="98765432100",
        telefone="31987651234",
        endereco="Rua B, 456 - Bairro Outro, Cidade/UF",
        tipo_usuario="admin"
    ),

        
]
adm = Usuario(
        nome="admin",
        email="administrador@system",
        senha=cript("admin"),
        tipo_usuario="admin"
    )
# Criar uma instância de Usuario
usuario = Usuario(
    nome="Marjory Novato",
    data_nascimento="2008-06-13",
    email="marjory@dominio.com",
    senha=cript("senha123"),  # Certifique-se de que a função cript() funciona corretamente
    cpf="12345678901",
    telefone=31987654321,
    endereco="Rua A, 123 - Bairro Exemplo, Cidade/UF",
    tipo_usuario="cliente"
)

# Criar uma instância do banco de dados
bd = BancoDeDados()
#bd.drop_banco()
bd.criar_banco()

# Cadastrar o usuário no banco de dados
bd.cadastrar_usuario(adm)

# Verificar se o usuário existe no banco de dados
if bd.verificar_usuario(usuario.email, usuario.senha):
    print("Usuário encontrado no banco de dados!")
else:
    print("Usuário não encontrado.")"""
