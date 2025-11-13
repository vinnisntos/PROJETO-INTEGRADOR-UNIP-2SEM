# 📦 Projeto Integrador (UNIP 2º Sem.): Sistema de Doações

![Status](https://img.shields.io/badge/status-concluído-brightgreen)

Este repositório contém o código-fonte do Projeto Integrador desenvolvido para o 2º Semestre do curso de **Análise e Desenvolvimento de Sistemas (ADS)** da Universidade Paulista (UNIP).

O projeto consiste em um sistema de console (CMD) para gerenciar solicitações e entregas de doações, conectando doadores a pessoas que precisam de itens.

## 📌 Funcionalidades Principais

* **Cadastro de Usuários:** Permite o registro de dois tipos de usuários (Doador e Receptor).
* **Login de Usuários:** Autenticação para acessar as funções do sistema.
* **Registro de Itens:** Doadores podem cadastrar itens que desejam doar.
* **Solicitação de Itens:** Receptores podem visualizar itens disponíveis e solicitá-los.
* **Listagem:** Exibição de listas de itens disponíveis, solicitações pendentes, etc.

## 💻 Tecnologias Utilizadas

* **[Python 3](https://www.python.org/)**: Linguagem principal do projeto.
* **Interface de Linha de Comando (CMD)**: Toda a interação do usuário é feita via console.

## 🔧 Estrutura dos Arquivos

O projeto foi organizado da seguinte forma para separar as responsabilidades:

* `main.py`: Ponto de entrada principal da aplicação. É o arquivo que deve ser executado.
* `interface_cmd.py`: Controla toda a lógica de exibição de menus e interação com o usuário no console.
* `system.py`: Contém as regras de negócio e a lógica central do sistema (ex: como um cadastro é feito, como uma solicitação é processada).
* `models.py`: Define as classes e estruturas de dados do projeto (ex: classe `Usuario`, classe `Doacao`, etc.).
* `.gitignore`: Arquivo de configuração do Git para ignorar arquivos desnecessários (como `__pycache__`).

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para executar o sistema em sua máquina local.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/vinnisntos/PROJETO-INTEGRADOR-UNIP-2SEM.git](https://github.com/vinnisntos/PROJETO-INTEGRADOR-UNIP-2SEM.git)
    ```

2.  **Acesse a pasta do projeto:**
    ```bash
    cd PROJETO-INTEGRADOR-UNIP-2SEM
    ```

3.  **(Opcional, mas recomendado) Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv venv
    
    # Ativar no Windows (PowerShell/CMD)
    .\venv\Scripts\activate
    ```

4.  **Execute o sistema:**
    ```bash
    python main.py
    ```

## 🧑‍💻 Autor

* **Vinnicius Gabriel Matos Dos Santos** - [vinnisntos](https://github.com/vinnisntos)
