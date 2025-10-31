# main.py - Sistema de Gerenciamento de Doações em CMD (100% em Memória)

import datetime
import os
from typing import List, Dict, Any, Optional

# --- Funções de Utilidade ---

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
            # Captura CTRL+D/CTRL+Z se ocorrer
            return ""

# --- Classes Modelo (Representação dos Dados) ---

class Usuario:
    def __init__(self, id: int, nome: str, email: str, senha: str, tipo_usuario: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.__senha = senha 
        self.tipo_usuario = tipo_usuario # Ex: 'Instituicao', 'Doador', 'Admin'

    def verificar_senha(self, senha_digitada: str) -> bool:
        return self.__senha == senha_digitada
    
    def __str__(self) -> str:
        return f"ID: {self.id} | Nome: {self.nome.ljust(15)} | Tipo: {self.tipo_usuario}"

class Item:
    def __init__(self, nome_produto: str, quantidade: int, categoria: str):
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.categoria = categoria

    def __str__(self) -> str:
        return f"- {self.nome_produto.ljust(20)} | Qtd: {str(self.quantidade).ljust(5)} | Categoria: {self.categoria}"

class Solicitacao:
    def __init__(self, id: int, instituicao_email: str, justificativa: str, status: str, data_solicitacao: str, itens: List[Item]):
        self.id = id
        self.instituicao_email = instituicao_email
        self.justificativa = justificativa
        self.status = status
        self.data_solicitacao = data_solicitacao
        self.itens = itens
        
    def __str__(self) -> str:
        data_formatada = self.data_solicitacao.split(' ')[0]
        return (f"ID: {str(self.id).ljust(3)} | Status: {self.status.ljust(10)} | "
                f"Instituição: {self.instituicao_email.ljust(20)} | Data: {data_formatada}")

# --- Lógica de Negócios Central (Backend) ---

class SistemaDoacoes:
    """Gerencia todos os usuários e solicitações em memória."""
    
    def __init__(self):
        # O "Banco de Dados" em memória
        self.usuarios: List[Usuario] = []
        self.solicitacoes: List[Solicitacao] = []
        self.proximo_usuario_id: int = 1
        self.proxima_solicitacao_id: int = 1
        self.usuario_logado: Optional[Usuario] = None
        self._inicializar_dados_teste()

    def _inicializar_dados_teste(self):
        """Cria um usuário Administrador e uma Instituição para testes."""
        # Admin
        self.usuarios.append(Usuario(self.proximo_usuario_id, "Admin Master", "admin@doacao.com", "123", "Admin"))
        self.proximo_usuario_id += 1
        # Instituição
        self.usuarios.append(Usuario(self.proximo_usuario_id, "Casa de Apoio S.J.", "ong@apoio.org", "123", "Instituicao"))
        self.proximo_usuario_id += 1
        # Solicitacao de teste
        itens_teste = [
            Item("Arroz 5kg", 100, "Alimento"),
            Item("Sabão em Pó", 50, "Higiene")
        ]
        self.solicitacoes.append(Solicitacao(
            self.proxima_solicitacao_id, 
            "ong@apoio.org", 
            "Emergência de fim de ano para 50 famílias.",
            "Pendente",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            itens_teste
        ))
        self.proxima_solicitacao_id += 1
        print("✅ Dados iniciais (Admin e ONG de teste) carregados.")
        
    # --- Autenticação (Login/Cadastro) ---

    def cadastrar_usuario(self, nome: str, email: str, senha: str, tipo: str) -> Optional[Usuario]:
        """Cria e salva um novo usuário na memória."""
        if any(u.email == email for u in self.usuarios):
            print("❌ Erro: Email já cadastrado.")
            return None
        
        novo_usuario = Usuario(self.proximo_usuario_id, nome, email, senha, tipo)
        self.usuarios.append(novo_usuario)
        self.proximo_usuario_id += 1
        return novo_usuario

    def fazer_login(self, email: str, senha: str) -> Optional[Usuario]:
        """Autentica o usuário."""
        for usuario in self.usuarios:
            if usuario.email == email and usuario.verificar_senha(senha):
                self.usuario_logado = usuario
                return usuario
        return None

    def logout(self):
        self.usuario_logado = None
    
    # --- Gerenciamento de Solicitações ---

    def criar_solicitacao(self, justificativa: str, itens_dados: List[Item]) -> Optional[int]:
        """Cria uma nova solicitação."""
        if not self.usuario_logado or self.usuario_logado.tipo_usuario != 'Instituicao':
            return None # Apenas instituições podem solicitar
        
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        nova_solicitacao = Solicitacao(
            self.proxima_solicitacao_id,
            self.usuario_logado.email,
            justificativa,
            "Pendente",
            data_atual,
            itens_dados
        )

        self.solicitacoes.append(nova_solicitacao)
        self.proxima_solicitacao_id += 1
        return nova_solicitacao.id

    def listar_solicitacoes(self) -> List[Solicitacao]:
        """Lista solicitações baseado no tipo de usuário logado."""
        if not self.usuario_logado:
            return []

        if self.usuario_logado.tipo_usuario == 'Admin':
            # Admin vê todas
            lista = self.solicitacoes
        elif self.usuario_logado.tipo_usuario == 'Instituicao':
            # Instituição vê apenas as suas
            lista = [s for s in self.solicitacoes if s.instituicao_email == self.usuario_logado.email]
        else:
            # Doador vê todas, talvez apenas as 'Aprovadas' em um futuro
            lista = self.solicitacoes
        
        # Ordena pela data mais recente primeiro
        lista.sort(key=lambda x: x.data_solicitacao, reverse=True)
        return lista

    def visualizar_detalhes(self, solicitacao_id: int) -> Optional[Solicitacao]:
        """Busca os detalhes de uma solicitação por ID."""
        for s in self.solicitacoes:
            if s.id == solicitacao_id:
                return s
        return None

    def atualizar_status(self, solicitacao_id: int, novo_status: str) -> bool:
        """Atualiza o status de uma solicitação."""
        if not self.usuario_logado or self.usuario_logado.tipo_usuario != 'Admin':
            return False

        if novo_status not in ["Aprovado", "Reprovado", "Pendente"]:
            return False
        
        for s in self.solicitacoes:
            if s.id == solicitacao_id:
                s.status = novo_status
                return True
        
        return False

# --- Interface CMD (Fluxos) ---

sistema = SistemaDoacoes()

def menu_login_cadastro():
    """Simula as telas Login 1 e Login 2."""
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
                print(f"\nSeja bem-vindo(a), {usuario.nome} ({usuario.tipo_usuario})!")
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

# --- Menus de Usuário ---

def menu_instituicao():
    """Menu para Instituições."""
    while sistema.usuario_logado and sistema.usuario_logado.tipo_usuario == 'Instituicao':
        limpar_tela()
        print("-" * 35)
        print(f"  MENU INSTITUIÇÃO ({sistema.usuario_logado.nome})")
        print("-" * 35)
        print("1. Nova Solicitação (Desktop 4 e 5)")
        print("2. Visualizar Minhas Solicitações (Desktop 3)")
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
            visualizar_solicitacoes_doador()
        elif escolha == '2':
            sistema.logout()
            print("Logout realizado.")
            input("Pressione Enter...")
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")


# --- Funções de Ação ---

def nova_solicitacao():
    """Simula o modal de Nova Solicitação (Desktop 4 e 5)."""
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
            print("\n❌ Erro ao criar solicitação.")
    else:
        print("\n❌ Não é possível criar uma solicitação sem itens.")
        
    input("Pressione Enter para continuar...")

def exibir_lista_solicitacoes(solicitacoes: List[Solicitacao]):
    """Função auxiliar para imprimir a lista formatada."""
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

def visualizar_solicitacoes():
    """Visualiza solicitações para Instituição/Doador."""
    limpar_tela()
    print("--- MINHAS SOLICITAÇÕES ---")
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
        print("--- MINHAS SOLICITAÇÕES ---")
        exibir_lista_solicitacoes(solicitacoes) # Mostra a lista novamente

def visualizar_solicitacoes_doador():
    """Doador visualiza apenas APROVADAS (exemplo)."""
    limpar_tela()
    print("--- SOLICITAÇÕES APROVADAS PARA DOAÇÃO ---")
    
    # Filtra apenas as aprovadas para o Doador
    solicitacoes = [s for s in sistema.listar_solicitacoes() if s.status == "Aprovado"]
    
    if not exibir_lista_solicitacoes(solicitacoes):
        input("Pressione Enter para continuar...")
        return

    while True:
        print("\nDigite o ID da solicitação que deseja ajudar, ou 0 para voltar.")
        escolha_id = obter_entrada("ID: ", tipo=int)
        
        if escolha_id == 0:
            break
        
        solicitacao = sistema.visualizar_detalhes(escolha_id)
        if solicitacao and solicitacao.status == "Aprovado":
            visualizar_detalhes_solicitacao(escolha_id)
            print("\nNOTA: Em um sistema completo, aqui você veria o contato da Instituição.")
        else:
            print("\nID inválido ou solicitação não aprovada.")
            
        input("Pressione Enter para continuar a lista...")
        limpar_tela()
        print("--- SOLICITAÇÕES APROVADAS PARA DOAÇÃO ---")
        exibir_lista_solicitacoes(solicitacoes)

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
        print("0. Voltar")
        acao = obter_entrada("Opção: ")
        
        novo_status = None
        if acao == '1': novo_status = "Aprovado"
        elif acao == '2': novo_status = "Reprovado"
        elif acao == '3': novo_status = "Pendente"
        elif acao == '0':
            pass
        else:
            print("Opção inválida.")
            
        if novo_status:
            if sistema.atualizar_status(escolha_id, novo_status):
                print(f"✅ Status da Solicitação {escolha_id} alterado para '{novo_status}'.")
            else:
                print("❌ Erro ao alterar status.")
        
        input("Pressione Enter para voltar à lista...")
        limpar_tela()
        print("--- GERENCIAR SOLICITAÇÕES ---")
        solicitacoes = sistema.listar_solicitacoes() # Recarrega a lista atualizada
        exibir_lista_solicitacoes(solicitacoes)


# --- Ponto de Início da Aplicação ---
if __name__ == "__main__":
    menu_login_cadastro()