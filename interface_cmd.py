# interface_cmd.py

import os
from typing import List, Any
from system import SistemaDoacoes
from models import Item, Solicitacao

# A instância do sistema será criada no main.py e passada para as funções se necessário
# ou, para simplificar o uso em múltiplos arquivos, vamos instanciar aqui, 
# mas o ideal seria passá-la como argumento em projetos maiores.
sistema = SistemaDoacoes() 

def limpar_tela():
    """Limpa o terminal para uma experiência mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_entrada(prompt: str, tipo=str) -> Any:
    """Função utilitária para obter entrada do usuário com validação de tipo."""
    while True:
        try:
            entrada = input(prompt)
            if tipo == int:
                return int(entrada)
            return entrada
        except ValueError:
            print("❌ Entrada inválida. Por favor, tente novamente.")
        except EOFError:
            return ""

# --- Funções de Exibição e Ação ---

def exibir_lista_solicitacoes(solicitacoes: List[Solicitacao]):
    """Função auxiliar para imprimir a lista formatada (Desktop 3)."""
    if not solicitacoes:
        print("Nenhuma solicitação encontrada.")
        return False
    
    print("\n" + "=" * 65)
    print("ID | Status     | Instituição               | Data")
    print("-" * 65)
    for s in solicitacoes:
        print(str(s))
    print("=" * 65)
    return True

def visualizar_detalhes_solicitacao(solicitacao_id: int):
    """Simula o modal de Detalhes (Desktop 6) e exibe os dados."""
    solicitacao = sistema.visualizar_detalhes(solicitacao_id)
    if not solicitacao:
        print(f"\n❌ Solicitação ID {solicitacao_id} não encontrada.")
        return

    limpar_tela()
    print("=" * 40)
    print(f"  DETALHES DA SOLICITAÇÃO ID {solicitacao.id}")
    print("=" * 40)
    print(f"Instituição: {solicitacao.instituicao_email}")
    print(f"Data:        {solicitacao.data_solicitacao}")
    print(f"Status:      {solicitacao.status}")
    print("-" * 40)
    print("Justificativa:")
    print(f"  {solicitacao.justificativa}")
    print("-" * 40)
    print("ITENS SOLICITADOS:")
    if solicitacao.itens:
        for item in solicitacao.itens:
            print(str(item))
    else:
        print("  (Nenhum item listado)")
    print("=" * 40)

def nova_solicitacao():
    """Fluxo para criar uma nova Solicitação (Desktop 4 e 5)."""
    limpar_tela()
    print("--- NOVA SOLICITAÇÃO ---")
    justificativa = obter_entrada("Justificativa (max 100 caracteres): ")[:100]
    
    itens_solicitados: List[Item] = []
    while True:
        print("\n--- Adicionar Item ---")
        nome_produto = obter_entrada("Nome do Produto (Ex: Arroz): ")
        
        while True:
            quantidade = obter_entrada("Quantidade (unidades): ", tipo=int)
            if quantidade > 0:
                break
            print("A quantidade deve ser um número positivo.")

        categoria = obter_entrada("Categoria (Ex: Alimento, Higiene): ")
        
        itens_solicitados.append(Item(nome_produto, quantidade, categoria))
        
        continuar = obter_entrada("Adicionar outro item? (s/n): ").lower()
        if continuar != 's':
            break

    if itens_solicitados:
        solicitacao_id = sistema.criar_solicitacao(justificativa, itens_solicitados)
        if solicitacao_id:
            print(f"\n✅ Solicitação {solicitacao_id} criada com sucesso e está Pendente!")
        else:
            print("\n❌ Erro ao criar solicitação (Você está logado como Instituição?).")
    else:
        print("\n❌ Não é possível criar uma solicitação sem itens.")
        
    input("Pressione Enter para continuar...")

def visualizar_solicitacoes():
    """Visualiza solicitações para Instituição/Doador."""
    limpar_tela()
    print("--- SOLICITAÇÕES ---")
    
    # O sistema já filtra automaticamente
    solicitacoes = sistema.listar_solicitacoes() 
    
    if not exibir_lista_solicitacoes(solicitacoes):
        input("Pressione Enter para continuar...")
        return

    while True:
        print("\nDigite o ID da solicitação para ver Detalhes, ou 0 para voltar.")
        escolha_id = obter_entrada("ID: ", tipo=int)
        
        if escolha_id == 0:
            break
        
        visualizar_detalhes_solicitacao(escolha_id)
        input("Pressione Enter para continuar a lista...")
        limpar_tela()
        print("--- SOLICITAÇÕES ---")
        exibir_lista_solicitacoes(solicitacoes) # Mostra a lista novamente

def gerenciar_solicitacoes_admin():
    """Admin lista e muda o status das solicitações."""
    limpar_tela()
    print("--- GERENCIAR SOLICITAÇÕES ---")
    
    solicitacoes = sistema.listar_solicitacoes()
    
    if not exibir_lista_solicitacoes(solicitacoes):
        input("Pressione Enter para continuar...")
        return

    while True:
        print("\nDigite o ID da solicitação para ver Detalhes/Mudar Status, ou 0 para voltar.")
        escolha_id_str = obter_entrada("ID: ")
        
        if escolha_id_str == '0':
            break
        
        try:
            escolha_id = int(escolha_id_str)
        except ValueError:
            print("Por favor, digite um número.")
            continue

        visualizar_detalhes_solicitacao(escolha_id)
        
        print("\n--- AÇÃO ADMINISTRATIVA ---")
        print("1. Aprovar")
        print("2. Reprovar")
        print("3. Manter Pendente")
        print("0. Voltar ao menu principal")
        acao = obter_entrada("Opção: ")
        
        novo_status = None
        if acao == '1': novo_status = "Aprovado"
        elif acao == '2': novo_status = "Reprovado"
        elif acao == '3': novo_status = "Pendente"
        
        if novo_status:
            if sistema.atualizar_status(escolha_id, novo_status):
                print(f"✅ Status da Solicitação {escolha_id} alterado para '{novo_status}'.")
            else:
                print("❌ Erro ao alterar status (Permissão negada ou ID incorreto).")
        
        input("Pressione Enter para voltar à lista...")
        limpar_tela()
        print("--- GERENCIAR SOLICITAÇÕES ---")
        solicitacoes = sistema.listar_solicitacoes() # Recarrega a lista atualizada
        exibir_lista_solicitacoes(solicitacoes)

# --- Menus Principais ---

def menu_instituicao():
    """Menu para Instituições."""
    while sistema.usuario_logado and sistema.usuario_logado.tipo_usuario == 'Instituicao':
        limpar_tela()
        print("-" * 35)
        print(f"  MENU INSTITUIÇÃO ({sistema.usuario_logado.nome})")
        print("-" * 35)
        print("1. Nova Solicitação")
        print("2. Visualizar Minhas Solicitações")
        print("3. Sair / Logout")
        print("-" * 35)
        
        escolha = obter_entrada("Sua opção: ")
        
        if escolha == '1':
            nova_solicitacao()
        elif escolha == '2':
            visualizar_solicitacoes()
        elif escolha == '3':
            sistema.logout()
            print("Logout realizado.")
            input("Pressione Enter...")
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

def menu_admin():
    """Menu para o Administrador."""
    while sistema.usuario_logado and sistema.usuario_logado.tipo_usuario == 'Admin':
        limpar_tela()
        print("-" * 35)
        print(f"  MENU ADMINISTRADOR ({sistema.usuario_logado.nome})")
        print("-" * 35)
        print("1. Gerenciar Solicitações (Aprovar/Reprovar)")
        print("2. Sair / Logout")
        print("-" * 35)
        
        escolha = obter_entrada("Sua opção: ")
        
        if escolha == '1':
            gerenciar_solicitacoes_admin()
        elif escolha == '2':
            sistema.logout()
            print("Logout realizado.")
            input("Pressione Enter...")
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

def menu_doador():
    """Menu para o Doador."""
    while sistema.usuario_logado and sistema.usuario_logado.tipo_usuario == 'Doador':
        limpar_tela()
        print("-" * 35)
        print(f"  MENU DOADOR ({sistema.usuario_logado.nome})")
        print("-" * 35)
        print("1. Visualizar Solicitações Aprovadas")
        print("2. Sair / Logout")
        print("-" * 35)
        
        escolha = obter_entrada("Sua opção: ")
        
        if escolha == '1':
            visualizar_solicitacoes() # Já filtra automaticamente as 'Aprovadas'
        elif escolha == '2':
            sistema.logout()
            print("Logout realizado.")
            input("Pressione Enter...")
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

def menu_login_cadastro():
    """Ponto de entrada do sistema (Login/Cadastro)."""
    while sistema.usuario_logado is None:
        limpar_tela()
        print("=" * 35)
        print("  Sistema de Doações (Terminal)")
        print("=" * 35)
        print("1. [Login] Entrar")
        print("2. [Cadastro] Criar Conta")
        print("3. Sair")
        print("-" * 35)
        
        escolha = obter_entrada("Sua opção: ")

        if escolha == '1':
            limpar_tela()
            print("--- LOGIN ---")
            email = obter_entrada("Email: ")
            senha = obter_entrada("Senha: ")
            usuario = sistema.fazer_login(email, senha)
            
            if usuario:
                print(f"\nSeja bem-vindo(a), {usuario.nome}!")
                input("Pressione Enter para continuar...")
                if usuario.tipo_usuario == 'Admin':
                    menu_admin()
                elif usuario.tipo_usuario == 'Instituicao':
                    menu_instituicao()
                else:
                    menu_doador()
            else:
                print("\n❌ Erro: Email ou senha incorretos.")
                input("Pressione Enter para tentar novamente...")

        elif escolha == '2':
            limpar_tela()
            print("--- CADASTRO ---")
            nome = obter_entrada("Nome Completo: ")
            email = obter_entrada("Email: ")
            senha = obter_entrada("Senha: ")
            
            print("\nTipo de Usuário:")
            print("1. Instituição/ONG")
            print("2. Doador/Pessoa Física")
            tipo_escolha = obter_entrada("Opção (1 ou 2): ")
            
            tipo = "Instituicao" if tipo_escolha == '1' else "Doador"
            
            resultado = sistema.cadastrar_usuario(nome, email, senha, tipo)
            
            if resultado:
                print(f"\n✅ Cadastro realizado! Usuário: {tipo}.")
            
            input("Pressione Enter para continuar...")

        elif escolha == '3':
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")