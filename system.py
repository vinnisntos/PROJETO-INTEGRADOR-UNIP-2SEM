# sistema.py

import datetime
from typing import List, Optional
from models import Usuario, Solicitacao, Item

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
        
        # Doador
        self.usuarios.append(Usuario(self.proximo_usuario_id, "Carlos Doador", "carlos@doador.com", "123", "Doador"))
        self.proximo_usuario_id += 1

        # Solicitacao de teste (Pendente)
        itens_teste_1 = [
            Item("Arroz 5kg", 100, "Alimento"),
            Item("Sabão em Pó", 50, "Higiene")
        ]
        self.solicitacoes.append(Solicitacao(
            self.proxima_solicitacao_id, 
            "ong@apoio.org", 
            "Emergência de fim de ano para 50 famílias.",
            "Pendente",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            itens_teste_1
        ))
        self.proxima_solicitacao_id += 1

        # Solicitacao de teste (Aprovada)
        itens_teste_2 = [
            Item("Cadeiras", 10, "Móveis"),
            Item("Agasalhos G", 30, "Vestuário")
        ]
        self.solicitacoes.append(Solicitacao(
            self.proxima_solicitacao_id, 
            "ong@apoio.org", 
            "Renovação de mobília e doação de roupas de inverno.",
            "Aprovado",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            itens_teste_2
        ))
        self.proxima_solicitacao_id += 1
        
        print("✅ Dados iniciais (Admin, ONG e Doador de teste) carregados.")
        
    # --- Autenticação (Login/Cadastro) ---

    def cadastrar_usuario(self, nome: str, email: str, senha: str, tipo: str) -> Optional[Usuario]:
        if any(u.email == email for u in self.usuarios):
            return None
        
        novo_usuario = Usuario(self.proximo_usuario_id, nome, email, senha, tipo)
        self.usuarios.append(novo_usuario)
        self.proximo_usuario_id += 1
        return novo_usuario

    def fazer_login(self, email: str, senha: str) -> Optional[Usuario]:
        for usuario in self.usuarios:
            if usuario.email == email and usuario.verificar_senha(senha):
                self.usuario_logado = usuario
                return usuario
        return None

    def logout(self):
        self.usuario_logado = None
    
    # --- Gerenciamento de Solicitações ---

    def criar_solicitacao(self, justificativa: str, itens_dados: List[Item]) -> Optional[int]:
        if not self.usuario_logado or self.usuario_logado.tipo_usuario != 'Instituicao':
            return None
        
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
        if not self.usuario_logado:
            return []

        if self.usuario_logado.tipo_usuario == 'Admin':
            lista = self.solicitacoes
        elif self.usuario_logado.tipo_usuario == 'Instituicao':
            lista = [s for s in self.solicitacoes if s.instituicao_email == self.usuario_logado.email]
        else:
            # Doador/Outro: Pode ver todas, mas vamos focar nas 'Aprovadas'
            lista = [s for s in self.solicitacoes if s.status == 'Aprovado']
        
        # Ordena pela data mais recente
        lista.sort(key=lambda x: x.data_solicitacao, reverse=True)
        return lista

    def visualizar_detalhes(self, solicitacao_id: int) -> Optional[Solicitacao]:
        for s in self.solicitacoes:
            if s.id == solicitacao_id:
                return s
        return None

    def atualizar_status(self, solicitacao_id: int, novo_status: str) -> bool:
        if not self.usuario_logado or self.usuario_logado.tipo_usuario != 'Admin':
            return False

        if novo_status not in ["Aprovado", "Reprovado", "Pendente"]:
            return False
        
        for s in self.solicitacoes:
            if s.id == solicitacao_id:
                s.status = novo_status
                return True
        
        return False