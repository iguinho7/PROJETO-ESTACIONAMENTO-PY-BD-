from db import get_connection


def cadastrar_veiculo(usuario: str):
    print("\n--- CADASTRAR VEÍCULO ---")
    placa = input("Placa: ").upper()

    # Verifica duplicata para este usuário
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM veiculos WHERE placa = %s AND criado_por = %s;",
            (placa, usuario)
        )
        if cur.fetchone():
            print("⚠️ Você já cadastrou esse veículo!\n")
            return

    try:
        cor      = input("Cor: ")
        modelo   = input("Modelo: ")
        marca    = input("Marca: ")
        nome     = input("Nome do proprietário: ")
        telefone = input("Telefone do proprietário: ")

        if any(char.isdigit() for char in cor + modelo + marca + nome):
            raise ValueError("Campos de texto não devem conter números.")
    except ValueError:
        print("❌ Dados inválidos. Verifique as entradas.\n")
        return

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO veiculos
              (placa, cor, modelo, marca,
               proprietario_nome, proprietario_telefone, criado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (placa, cor, modelo, marca, nome, telefone, usuario)
        )
        conn.commit()

    print("✅ Veículo cadastrado com sucesso!\n")


def listar_veiculos_cadastrado_por(usuario: str):
    print(f"\n--- VEÍCULOS CADASTRADOS POR {usuario} ---")
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT placa, marca, modelo, cor,
                   proprietario_nome, proprietario_telefone
              FROM veiculos
             WHERE criado_por = %s;
            """,
            (usuario,)
        )
        rows = cur.fetchall()

    if not rows:
        print(f"Não há veículos cadastrados por {usuario}.\n")
    else:
        for placa, marca, modelo, cor, nome, telefone in rows:
            print(f"Placa: {placa} | {marca} {modelo} - {cor}")
            print(f"  Proprietário: {nome} | Telefone: {telefone}\n")


def atualizar_veiculo(usuario: str):
    print("\n--- ATUALIZAR VEÍCULO ---")
    placa = input("Placa do veículo que deseja atualizar: ").upper()

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT cor, modelo, marca,
                   proprietario_nome, proprietario_telefone
              FROM veiculos
             WHERE placa = %s AND criado_por = %s;
            """,
            (placa, usuario)
        )
        row = cur.fetchone()
        if not row:
            print("❌ Veículo não encontrado ou não é seu.\n")
            return
        cor_atual, modelo_atual, marca_atual, nome_atual, tel_atual = row

    nova_cor    = input(f"Cor [{cor_atual}]: ") or cor_atual
    novo_modelo = input(f"Modelo [{modelo_atual}]: ") or modelo_atual
    nova_marca  = input(f"Marca [{marca_atual}]: ") or marca_atual
    novo_nome   = input(f"Nome do proprietário [{nome_atual}]: ") or nome_atual
    novo_tel    = input(f"Telefone [{tel_atual}]: ") or tel_atual

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE veiculos
               SET cor = %s,
                   modelo = %s,
                   marca = %s,
                   proprietario_nome = %s,
                   proprietario_telefone = %s
             WHERE placa = %s AND criado_por = %s;
            """,
            (nova_cor, novo_modelo, nova_marca,
             novo_nome, novo_tel, placa, usuario)
        )
        conn.commit()

    print("✅ Veículo atualizado com sucesso!\n")


def deletar_veiculo(usuario: str):
    print("\n--- DELETAR VEÍCULO ---")
    placa = input("Placa do veículo que deseja deletar: ").upper()

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM veiculos WHERE placa = %s AND criado_por = %s;",
            (placa, usuario)
        )
        if cur.rowcount == 0:
            print("❌ Veículo não encontrado ou não é seu.\n")
        else:
            conn.commit()
            print("✅ Veículo deletado com sucesso!\n")


def buscar_veiculos_por_placa(usuario: str):
    print("\n--- BUSCAR VEÍCULOS (LIKE) ---")
    padrao = input("Digite parte da placa para buscar: ").upper()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT placa, marca, modelo, cor
              FROM veiculos
             WHERE criado_por = %s
               AND placa LIKE %s;
            """,
            (usuario, f"%{padrao}%")
        )
        rows = cur.fetchall()

    if not rows:
        print(f"Nenhum veículo encontrado para '%{padrao}%'.\n")
    else:
        for placa, marca, modelo, cor in rows:
            print(f"{placa} | {marca} {modelo} - {cor}")
        print()


def listar_veiculos_ordenados(usuario: str):
    print("\n--- VEÍCULOS ORDENADOS (ORDER BY) ---")
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT placa, marca, modelo, cor
              FROM veiculos
             WHERE criado_por = %s
             ORDER BY marca, modelo;
            """,
            (usuario,)
        )
        rows = cur.fetchall()

    if not rows:
        print("Nenhum veículo cadastrado.\n")
    else:
        for placa, marca, modelo, cor in rows:
            print(f"{placa} | {marca} {modelo} - {cor}")
        print()


def listar_todos_veiculos():
    print("\n--- TODOS OS VEÍCULOS ---")
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT u.username, v.placa, v.marca, v.modelo, v.cor
              FROM usuarios u
             INNER JOIN veiculos v
                ON u.username = v.criado_por
             ORDER BY u.username;
            """
        )
        rows = cur.fetchall()

    if not rows:
        print("Nenhum veículo cadastrado no sistema.\n")
    else:
        for user, placa, marca, modelo, cor in rows:
            print(f"{user}: {placa} | {marca} {modelo} - {cor}")
        print()
