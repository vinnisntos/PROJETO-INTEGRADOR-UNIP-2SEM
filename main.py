# login e cadastro simples 
import os
import datetime
import crud.adm as adm
import crud.doador as doador
import crud.solicitante as solicitante

#definir caminho do arquivo de usuarios
USUARIOS_PATH = os.path.join('arquivos', 'usuarios.txt')


#função para ler usuarios do arquivo
def ler_usuarios():
    usuarios = []
    if not os.path.exists(USUARIOS_PATH):
        return usuarios
    with open(USUARIOS_PATH, 'r', encoding='utf-8') as f:
        linhas = f.read().strip().splitlines()
    if len(linhas) <= 1:
        return usuarios
    for linha in linhas[1:]:
        partes = linha.split(';')
        usuarios.append({
            'id': int(partes[0]),
            'nome': partes[1],
            'login': partes[2],
            'senha': partes[3],
            'papel': partes[4],
            'ativo': partes[5] == '1'
        })
    return usuarios

#função para salvar usuarios no arquivo
def salvar_usuarios(usuarios):
    with open(USUARIOS_PATH, 'w', encoding='utf-8') as f:
        f.write('id;nome;login;senha;papel;ativo\n')
        for usuario in usuarios:
            linha = f"{usuario['id']};{usuario['nome']};{usuario['login']};{usuario['senha']};{usuario['papel']};{'1' if usuario['ativo'] else '0'}\n"
            f.write(linha)


#função para obter o próximo id disponível
def proximo_id(usuarios):
    if not usuarios:
        return 1
    return max(u['id'] for u in usuarios) + 1



#função para cadastrar novo usuario
def cadastrar():
    usuarios = ler_usuarios()
    print("\n=== Cadastro de Usuário ===")
    nome = input("Nome: ").strip()
    login = input("Login: ").strip()
    if any(u['login'] == login for u in usuarios):
        print("Login já existe. Tente novamente.")
        return
    senha = input("Senha: ").strip()
    papel = input("Papel (solicitante|doador|adm): ").strip().lower()
    if papel not in ['solicitante', 'doador', 'adm']:
        print("Papel inválido. Tente novamente.")
        return
    novo = {
        'id': proximo_id(usuarios),
        'nome': nome,
        'login': login,
        'senha': senha,
        'papel': papel,
        'ativo': True
    }
    usuarios.append(novo)
    salvar_usuarios(usuarios)
    print(f"Usuário {nome} cadastrado com id {novo['id']}.")



#função para login de usuario
def login():
    usuarios = ler_usuarios()
    print("\n=== Login ===")
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    usuario = next((u for u in usuarios if u['login'] == login and u['senha'] == senha and u['ativo']), None)
    if not usuario:
        print("Login ou senha inválidos, ou usuário inativo.")
        return None
    print(f"Bem-vindo, {usuario['nome']}! Papel: {usuario['papel']}")
    return usuario



#função principal
def main():
    while True:
        print("\n1) Cadastrar \n2) Login \n0) Sair")
        op = input('\n\n> ').strip()
        if op == '1':
            cadastrar()
        elif op == '2':
            usuario = login()

            
            #redirecionar conforme papel
            if usuario:
                if usuario['papel'] == 'solicitante':
                    solicitante.menu_solicitante(usuario)
                elif usuario['papel'] == 'doador':
                    doador.menu_doador(usuario)
                elif usuario['papel'] == 'adm':
                    adm.menu_adm(usuario)


        #opção de sair com limpeza de tela
        elif op == '0':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == '__main__':
    main()