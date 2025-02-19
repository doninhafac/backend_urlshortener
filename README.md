# Encurtador de URL

Este projeto foi desenvolvido por **Daniel Reis** e **Andressa Lopes** como parte da disciplina de **Desenvolvimento Web**, ministrada pelo professor **Ciniro Nametala**. O objetivo do projeto é criar um encurtador de URL utilizando uma stack moderna, com Django no backend e PostgreSQL como banco de dados.

## Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes requisitos instalados em sua máquina:

-   **Anaconda Python**: Para gerenciar o ambiente Python.
-   **VSCode**: Para edição de código.
-   **PostgreSQL 16+**: Como banco de dados.
-   **DBeaver**: Para gerenciar o banco de dados.
-   **Git**: Para controle de versão.

### Instalando o Anaconda Python

1. **Windows/Mac**:

    - Acesse o site oficial do [Anaconda](https://www.anaconda.com/products/distribution).
    - Baixe a versão apropriada para o seu sistema operacional.
    - Siga as instruções do instalador.

2. **Linux**:

    - Abra o terminal e execute os seguintes comandos:
        ```bash
        wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh
        bash Anaconda3-2023.03-Linux-x86_64.sh
        ```

3. **Verificando a instalação**:
    - Após a instalação, verifique se o Anaconda foi instalado corretamente:
        ```bash
        conda --version
        ```

## Instalando e Rodando o Projeto

### 1. Clonando o Repositório

Primeiro, clone o repositório do backend do projeto para sua máquina:

```bash
git clone https://github.com/doninhafac/backend_urlshortener
cd backend_urlshortener
```

### 2. Criando e Ativando o Ambiente Conda

Crie e ative um ambiente Conda para o projeto:

```bash
conda create --name urlshortener python=3.9
conda activate urlshortener
```

### 3. Instalando Dependências

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configurando o Banco de Dados

Certifique-se de que o PostgreSQL está rodando e crie um banco de dados para o projeto. Você pode usar o DBeaver para gerenciar o banco de dados.

### 5. Aplicando Migrações

Aplique as migrações para configurar o banco de dados:

```bash
python manage.py migrate
```

### 6. Rodando o Servidor de Desenvolvimento

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O backend deve estar rodando em [http://localhost:8000](http://localhost:8000).

### 7. Rodando o Frontend

Clone o repositório do frontend do projeto e siga as instruções para rodar o frontend:

```bash
git clone https://github.com/doninhafac/frontend_urlshortener
cd frontend_urlshortener
```

Siga as instruções no README do repositório do frontend para configurar e rodar o frontend.

## Estrutura do Projeto

-   **backend/**: Contém o código do servidor backend, responsável por gerenciar as URLs encurtadas.
-   **frontend/**: Contém o código do frontend, desenvolvido com React e Vite.

Feito com ❤️ por Daniel Reis e Andressa Lopes.
