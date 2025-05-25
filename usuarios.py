import pwinput
import bcrypt
from db import get_connection

def inicializar_admin():
    """
    Garante que exista o usuário admin com senha '1234' (criptografada).
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM usuarios WHERE username = %s;", ('admin',))
        if not cur.fetchone():
            hash_admin = bcrypt.hashpw('1234'.encode(), bcrypt.gensalt()).decode()
            cur.execute(
                "INSERT INTO usuarios (username, senha_hash) VALUES (%s, %s);",
                ('admin', hash_admin)
            )
            conn.commit()

def login() -> str | None:
    """
    Faz login e retorna o username se der certo, ou None se falhar.
    """
    print("\n--- LOGIN ---")
    user = input("Usuário: ")
    senha = pwinput.pwinput(prompt='Senha: ', mask='*')

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT senha_hash FROM usuarios WHERE username = %s;", (user,))
        row = cur.fetchone()

    if row and bcrypt.checkpw(senha.encode(), row[0].encode()):
        print("✅ Login bem-sucedido!\n")
        return user

    print("❌ Usuário ou senha incorretos.\n")
    return None

def adicionar_usuario():
    """
    Cadastra novo usuário com senha criptografada.
    """
    print("\n--- CADASTRAR NOVO FUNCIONÁRIO ---")
    novo_user = input("Novo usuário: ")

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM usuarios WHERE username = %s;", (novo_user,))
        if cur.fetchone():
            print("⚠️ Usuário já existe!\n")
            return

        nova_senha = pwinput.pwinput(prompt="Nova senha: ", mask='*')
        hash_senha = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()

        cur.execute(
            "INSERT INTO usuarios (username, senha_hash) VALUES (%s, %s);",
            (novo_user, hash_senha)
        )
        conn.commit()

    print("✅ Usuário cadastrado com sucesso!\n")
