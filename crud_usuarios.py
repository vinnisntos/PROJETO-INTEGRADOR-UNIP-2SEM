import os

CAMINHO_USUARIOS = "arquivos/usuarios.txt"

def listar_usuarios():
    if not os.path.exists(CAMINHO_USUARIOS):
        print("Arquivo de usuários não encontrado.")
        return
    with open(CAMINHO_USUARIOS, "r", encoding="utf-8") as f:
        linhas = f.readlines()
        for linha in linhas:
            print(linha.strip())

def adicionar_usuario(id, nome, login, senha, papel, ativo=True):
    with open(CAMINHO_USUARIOS, "a", encoding="utf-8") as f:
        f.write(f"{id};{nome};{login};{senha};{papel};{ativo}\n")
    print(f"Usuário '{nome}' adicionado com sucesso!")

if __name__ == "__main__":
    listar_usuarios()
    adicionar_usuario(1, "Admin", "admin", "1234", "gerente")
