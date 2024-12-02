
import bcrypt


def cript(senha):
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        print(senha_hash)
        return senha_hash
    