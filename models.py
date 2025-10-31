# modelos.py

from typing import List
from datetime import datetime

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