import os

ARQUIVO_SOLICITACOES = os.path.join('arquivos', 'solicitacoes.txt')



# garante que o arquvio realmente existe
if not os.path.exists(ARQUIVO_SOLICITACOES):
    with open(ARQUIVO_SOLICITACOES, 'w', encoding='utf-8') as f:
        f.write('id;id_usuario;produto;quantidade;status;motivo_reprova\n')



# função para obter o próximo id disponível
def proximo_id():
    if not os.path.exists(ARQUIVO_SOLICITACOES):
        return 1
    with open(ARQUIVO_SOLICITACOES, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    if len(linhas) <= 1:
        return 1
    ultimo = linhas[-1].split(';')[0]
    return int(ultimo) + 1




# função para fazer uma solicitação
def fazer_solicitacao(usuario):
    print('\n=== Fazer Solicitação ===')
    produto = input('Produto: ').strip()
    quantidade = input('Quantidade: ').strip()
    nova = f"{proximo_id()};{usuario['id']};{produto};{quantidade};pendente;\n"
    with open(ARQUIVO_SOLICITACOES, 'a', encoding='utf-8') as f:
        f.write(nova)
    print('\n\nSolicitação enviada com sucesso, aguarde aprovação do Administrador!')


# função para listar as solicitações do usuário
def listar_solicitacoes(usuario):
    print("\n=== MINHAS SOLICITAÇÕES ===")
    if not os.path.exists(ARQUIVO_SOLICITACOES):
        print("Nenhuma solicitação registrada.")
        return
    with open(ARQUIVO_SOLICITACOES, 'r', encoding='utf-8') as f:
        linhas = f.read().strip().splitlines()
    if len(linhas) <= 1:
        print("Nenhuma solicitação encontrada.")
        return
    for linha in linhas[1:]:
        partes = linha.split(';')
        if partes[1] == str(usuario['id']):
            print(f"ID: {partes[0]} | Produto: {partes[2]} | Quantidade: {partes[3]} | Status: {partes[4]}")
            if partes[4] == 'reprovado':
                print(f"   Motivo: {partes[5]}")


# menu do solicitante
def menu_solicitante(usuario):
    while True:
        print("\n=== ÁREA DO SOLICITANTE ===")
        print("1) Fazer nova solicitação")
        print("2) Ver minhas solicitações")
        print("0) Voltar")
        op = input("\n> ").strip()
        if op == '1':
            fazer_solicitacao(usuario)
        elif op == '2':
            listar_solicitacoes(usuario)
        elif op == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")