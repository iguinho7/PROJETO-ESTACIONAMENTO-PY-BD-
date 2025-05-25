from usuarios import inicializar_admin, login, adicionar_usuario
from veiculos import (
    cadastrar_veiculo,
    listar_veiculos_cadastrado_por,
    atualizar_veiculo,
    deletar_veiculo,
    buscar_veiculos_por_placa,
    listar_veiculos_ordenados,
    listar_todos_veiculos
)

def menu_principal(usuario: str):
    while True:
        print("==== MENU PRINCIPAL ====")
        print("1. Cadastrar veículo")
        
        if usuario == 'admin':
            print("2. Listar veículos cadastrados pelo funcionário")
        else:
            print("2. Listar veículos cadastrados por mim")
        print("3. Atualizar veículo")
        print("4. Deletar veículo")
        print("5. Buscar veículo por placa")
        print("6. Listar veículos ordenados")
        print("7. Listar todos")
        print("8. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_veiculo(usuario)

        elif opcao == '2':
            if usuario == 'admin':
                # só o admin chega aqui
                funcionario = input("Digite o nome do funcionário: ")
                listar_veiculos_cadastrado_por(funcionario)
            else:
                # usuário comum
                listar_veiculos_cadastrado_por(usuario)

        elif opcao == '3':
            atualizar_veiculo(usuario)

        elif opcao == '4':
            deletar_veiculo(usuario)

        elif opcao == '5':
            buscar_veiculos_por_placa(usuario)

        elif opcao == '6':
            listar_veiculos_ordenados(usuario)

        elif opcao == '7':
            listar_todos_veiculos()

        elif opcao == '8':
            print("Encerrando sessão.\n")
            break

        else:
            print("Opção inválida. Tente novamente.\n")


def menu_inicial():
    inicializar_admin()
    while True:
        print("==== BEM-VINDO AO ESTACIONAMENTO PARK KEY ====")
        print("1. Entrar (Login)")
        print("2. Cadastrar novo funcionário")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            usuario = login()
            if usuario:
                menu_principal(usuario)

        elif opcao == '2':
            print("\n--- AUTENTICAÇÃO DE ADMIN ---")
            usuario = login()
            if usuario == 'admin':
                adicionar_usuario()
            else:
                print("❌ Acesso negado. Somente admin pode cadastrar novos funcionários.\n")

        elif opcao == '3':
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    menu_inicial()
