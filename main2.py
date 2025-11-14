"""
SISTEMA MANUS - Exemplos de Funções Principais em Python
Projeto Integrador Multidisciplinar (PIM)
"""

from datetime import datetime

# ==================== 1. CADASTRO DE PRODUTOS ====================

def cadastrar_produto():
    """
    Função para cadastrar um novo produto no estoque.
    Requisito Funcional: Cadastro de Produtos
    """
    print("\n=== CADASTRO DE PRODUTO ===")
    
    # Coleta os dados do produto
    nome = input("Nome do produto: ")
    categoria = input("Categoria (Alimento/Higiene/Vestuário): ")
    quantidade = int(input("Quantidade: "))
    validade = input("Data de validade (DD/MM/AAAA): ")
    
    # Cria um dicionário com os dados do produto
    produto = {
        'nome': nome,
        'categoria': categoria,
        'quantidade': quantidade,
        'validade': validade,
        'data_cadastro': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    print(f"\n✓ Produto '{nome}' cadastrado com sucesso!")
    return produto


# ==================== 2. CADASTRO DE USUÁRIOS ====================

def cadastrar_usuario():
    """
    Função para cadastrar um novo usuário no sistema.
    Requisito Funcional: Cadastro de Usuários
    """
    print("\n=== CADASTRO DE USUÁRIO ===")
    
    nome = input("Nome completo: ")
    email = input("Email: ")
    senha = input("Senha: ")
    
    print("\nTipo de usuário:")
    print("1 - Solicitante")
    print("2 - Doador")
    print("3 - Administrador")
    tipo = input("Escolha o tipo: ")
    
    # Converte a opção para o tipo correto
    tipos = {
        '1': 'solicitante',
        '2': 'doador',
        '3': 'administrador'
    }
    
    usuario = {
        'nome': nome,
        'email': email,
        'senha': senha,
        'tipo': tipos.get(tipo, 'solicitante'),
        'data_cadastro': datetime.now().strftime("%d/%m/%Y")
    }
    
    print(f"\n✓ Usuário '{nome}' cadastrado como {usuario['tipo']}!")
    return usuario


# ==================== 3. REGISTRO DE MOVIMENTAÇÕES ====================

def registrar_movimentacao(produto_nome, tipo_movimentacao, quantidade, responsavel):
    """
    Função para registrar entrada ou saída de produtos.
    Requisito Funcional: Registro de Movimentações
    
    Args:
        produto_nome: Nome do produto
        tipo_movimentacao: 'entrada' ou 'saida'
        quantidade: Quantidade movimentada
        responsavel: Email do usuário responsável
    """
    movimentacao = {
        'produto': produto_nome,
        'tipo': tipo_movimentacao,
        'quantidade': quantidade,
        'responsavel': responsavel,
        'data': datetime.now().strftime("%d/%m/%Y"),
        'hora': datetime.now().strftime("%H:%M:%S")
    }
    
    print(f"\n✓ {tipo_movimentacao.upper()} registrada:")
    print(f"   Produto: {produto_nome}")
    print(f"   Quantidade: {quantidade}")
    print(f"   Responsável: {responsavel}")
    
    return movimentacao


# ==================== 4. CONTROLE DE ESTOQUE ====================

def atualizar_estoque(estoque, produto_nome, quantidade, operacao):
    """
    Função para atualizar a quantidade de produtos no estoque.
    Requisito Funcional: Controle de Estoque
    
    Args:
        estoque: Lista de produtos no estoque
        produto_nome: Nome do produto a atualizar
        quantidade: Quantidade a adicionar ou remover
        operacao: 'adicionar' ou 'remover'
    """
    # Busca o produto no estoque
    produto_encontrado = False
    
    for produto in estoque:
        if produto['nome'].lower() == produto_nome.lower():
            produto_encontrado = True
            
            if operacao == 'adicionar':
                produto['quantidade'] += quantidade
                print(f"\n✓ Adicionado {quantidade} unidades de {produto_nome}")
            elif operacao == 'remover':
                if produto['quantidade'] >= quantidade:
                    produto['quantidade'] -= quantidade
                    print(f"\n✓ Removido {quantidade} unidades de {produto_nome}")
                else:
                    print(f"\n✗ Estoque insuficiente! Disponível: {produto['quantidade']}")
            
            print(f"   Quantidade atual: {produto['quantidade']}")
            break
    
    if not produto_encontrado:
        print(f"\n✗ Produto '{produto_nome}' não encontrado no estoque!")


# ==================== 5. CONSULTAS E FILTROS ====================

def consultar_produtos(estoque, filtro='todos', valor=''):
    """
    Função para consultar produtos com filtros.
    Requisito Funcional: Consultas e Filtros
    
    Args:
        estoque: Lista de produtos
        filtro: 'nome', 'categoria', 'todos'
        valor: Valor a buscar
    """
    print("\n=== RESULTADOS DA CONSULTA ===")
    
    resultados = []
    
    for produto in estoque:
        if filtro == 'todos':
            resultados.append(produto)
        elif filtro == 'nome' and valor.lower() in produto['nome'].lower():
            resultados.append(produto)
        elif filtro == 'categoria' and valor.lower() == produto['categoria'].lower():
            resultados.append(produto)
    
    if resultados:
        for prod in resultados:
            print(f"\nProduto: {prod['nome']}")
            print(f"Categoria: {prod['categoria']}")
            print(f"Quantidade: {prod['quantidade']}")
            print("-" * 40)
    else:
        print("\nNenhum produto encontrado.")
    
    return resultados


# ==================== 6. ALERTAS AUTOMÁTICOS ====================

def verificar_alertas(estoque, limite_estoque=10):
    """
    Função para verificar produtos com estoque baixo.
    Requisito Funcional: Alertas Automáticos
    
    Args:
        estoque: Lista de produtos
        limite_estoque: Quantidade mínima antes do alerta
    """
    print("\n=== VERIFICAÇÃO DE ALERTAS ===")
    
    alertas = []
    
    for produto in estoque:
        if produto['quantidade'] <= limite_estoque:
            alerta = {
                'produto': produto['nome'],
                'quantidade_atual': produto['quantidade'],
                'tipo': 'ESTOQUE BAIXO'
            }
            alertas.append(alerta)
            print(f"\n⚠️  ALERTA: {produto['nome']}")
            print(f"   Quantidade atual: {produto['quantidade']}")
            print(f"   Status: CRÍTICO - Reabastecer urgente!")
    
    if not alertas:
        print("\n✓ Todos os produtos estão com estoque adequado.")
    
    return alertas


# ==================== 7. AUTENTICAÇÃO (LOGIN) ====================

def fazer_login(usuarios, email, senha):
    """
    Função para autenticar usuário no sistema.
    Requisito Não Funcional: Segurança
    
    Args:
        usuarios: Lista de usuários cadastrados
        email: Email do usuário
        senha: Senha do usuário
    """
    for usuario in usuarios:
        if usuario['email'] == email and usuario['senha'] == senha:
            print(f"\n✓ Login realizado com sucesso!")
            print(f"   Bem-vindo(a), {usuario['nome']}!")
            print(f"   Tipo de acesso: {usuario['tipo'].upper()}")
            return usuario
    
    print("\n✗ Email ou senha incorretos!")
    return None


# ==================== 8. CRIAR SOLICITAÇÃO ====================

def criar_solicitacao(instituicao, produtos_solicitados, justificativa, solicitante):
    """
    Função para criar uma nova solicitação de doação.
    Funcionalidade específica do perfil Solicitante
    
    Args:
        instituicao: Nome da instituição
        produtos_solicitados: Lista de produtos necessários
        justificativa: Motivo da solicitação
        solicitante: Email do solicitante
    """
    solicitacao = {
        'id': id(instituicao + datetime.now().strftime("%d%m%Y%H%M%S")),
        'instituicao': instituicao,
        'produtos': produtos_solicitados,
        'justificativa': justificativa,
        'solicitante': solicitante,
        'status': 'Pendente',
        'data': datetime.now().strftime("%d/%m/%Y")
    }
    
    print(f"\n✓ Solicitação criada com sucesso!")
    print(f"   Instituição: {instituicao}")
    print(f"   Produtos solicitados: {len(produtos_solicitados)}")
    print(f"   Status: Pendente")
    
    return solicitacao


# ==================== 9. GERAR RELATÓRIO ====================

def gerar_relatorio(estoque, movimentacoes):
    """
    Função para gerar relatório do estoque.
    Requisito Funcional: Relatórios
    
    Args:
        estoque: Lista de produtos
        movimentacoes: Lista de movimentações
    """
    print("\n" + "=" * 50)
    print("RELATÓRIO DE ESTOQUE")
    print("=" * 50)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Resumo do estoque
    print(f"\n📦 Total de produtos cadastrados: {len(estoque)}")
    
    quantidade_total = sum(p['quantidade'] for p in estoque)
    print(f"📊 Quantidade total de itens: {quantidade_total}")
    
    # Produtos por categoria
    categorias = {}
    for produto in estoque:
        cat = produto['categoria']
        if cat in categorias:
            categorias[cat] += 1
        else:
            categorias[cat] = 1
    
    print("\n📋 Produtos por categoria:")
    for categoria, qtd in categorias.items():
        print(f"   {categoria}: {qtd} produto(s)")
    
    # Últimas movimentações
    print(f"\n📝 Total de movimentações: {len(movimentacoes)}")
    
    print("\n" + "=" * 50)


# ==================== EXEMPLO DE USO ====================

def exemplo_uso():
    """Demonstração de como usar as funções"""
    
    print("\n" + "=" * 50)
    print("SISTEMA MANUS - DEMONSTRAÇÃO")
    print("=" * 50)
    
    # Criar listas vazias para armazenar dados
    estoque = []
    usuarios = []
    movimentacoes = []
    solicitacoes = []
    
    # 1. Cadastrar um usuário
    print("\n\n--- 1. CADASTRANDO USUÁRIO ---")
    usuario1 = {
        'nome': 'João Silva',
        'email': 'joao@email.com',
        'senha': '123',
        'tipo': 'administrador',
        'data_cadastro': datetime.now().strftime("%d/%m/%Y")
    }
    usuarios.append(usuario1)
    print(f"✓ Usuário '{usuario1['nome']}' cadastrado!")
    
    # 2. Fazer login
    print("\n\n--- 2. FAZENDO LOGIN ---")
    usuario_logado = fazer_login(usuarios, 'joao@email.com', '123')
    
    # 3. Cadastrar produtos
    print("\n\n--- 3. CADASTRANDO PRODUTOS ---")
    produto1 = {
        'nome': 'Arroz',
        'categoria': 'Alimento',
        'quantidade': 50,
        'validade': '31/12/2025'
    }
    produto2 = {
        'nome': 'Feijão',
        'categoria': 'Alimento',
        'quantidade': 5,  # Estoque baixo para testar alerta
        'validade': '30/06/2025'
    }
    estoque.append(produto1)
    estoque.append(produto2)
    print(f"✓ {len(estoque)} produtos cadastrados!")
    
    # 4. Atualizar estoque
    print("\n\n--- 4. ATUALIZANDO ESTOQUE ---")
    atualizar_estoque(estoque, 'Arroz', 20, 'adicionar')
    
    # 5. Registrar movimentação
    print("\n\n--- 5. REGISTRANDO MOVIMENTAÇÃO ---")
    mov = registrar_movimentacao('Arroz', 'entrada', 20, 'joao@email.com')
    movimentacoes.append(mov)
    
    # 6. Consultar produtos
    print("\n\n--- 6. CONSULTANDO PRODUTOS ---")
    consultar_produtos(estoque, 'categoria', 'Alimento')
    
    # 7. Verificar alertas
    print("\n\n--- 7. VERIFICANDO ALERTAS ---")
    verificar_alertas(estoque, limite_estoque=10)
    
    # 8. Gerar relatório
    print("\n\n--- 8. GERANDO RELATÓRIO ---")
    gerar_relatorio(estoque, movimentacoes)
    
    print("\n\n" + "=" * 50)
    print("FIM DA DEMONSTRAÇÃO")
    print("=" * 50)


# Executar exemplo
if __name__ == "__main__":
    exemplo_uso()
