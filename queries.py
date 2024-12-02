
SQL_INSERIR = """
   INSERT INTO usuario (nome, email) 
   VALUES (?, ?)
"""

SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_nascimento DATE,
    email TEXT NOT NULL,
    cpf TEXT,
    telefone INTEGER,
    endereco TEXT,
    senha TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL
);
"""

SQL_DROP_TABLE = """
DROP TABLE IF EXISTS usuario
"""

SQL_INSERIR_USUARIO = """
INSERT INTO usuario (nome, data_nascimento, email, cpf, telefone, endereco, senha, tipo_usuario)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""


SQL_VERIFICAR_USUARIO = """
SELECT * FROM usuario
WHERE email = ? AND senha = ?
"""

SQL_ALTERAR_NOME = """
UPDATE usuario
SET nome = ?
WHERE email = ?;
"""

SQL_DELETAR_USER = """
DELETE FROM usuario
WHERE email = ?;
"""


SQL_OBTER_POR_ID = """
SELECT * FROM usuario 
WHERE id = ?"""

SQL_OBTER_SENHA_POR_EMAIL = """
    SELECT senha
    FROM usuario
    WHERE email = ?
"""

SQL_OBTER_DADOS_POR_EMAIL = """
    SELECT id, nome, email, tipo_usuario
    FROM usuario
    WHERE email = ?
"""
