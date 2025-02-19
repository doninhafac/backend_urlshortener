# Projeto URL Shortener

Este projeto é um encurtador de URL desenvolvido em Django com PostgreSQL. Siga as instruções abaixo para configurar o ambiente e executar o projeto.

---

## 1️⃣ Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados:

- [Anaconda Python](https://www.anaconda.com/products/distribution)
- [VSCode](https://code.visualstudio.com/)
- [PostgreSQL 16+](https://www.postgresql.org/download/)
- [DBeaver](https://dbeaver.io/download/)
- [Git](https://git-scm.com/downloads)

---

## 2️⃣ Clonar o Repositório

Clone o projeto para o seu computador:

```bash
git clone git@github.com:doninhafac/backend_urlshortener.git
cd backend_urlshortener
```

---

## 3️⃣ Configurar o Ambiente Virtual

1. **Criar o ambiente Conda:**
   ```bash
   conda create -n encurtador python=3.11.9
   ```

2. **Ativar o ambiente:**
   ```bash
   conda activate encurtador
   ```

3. **Instalar as dependências:**
   ```bash
   pip install Django==4.1
   pip install psycopg2
   pip install psycopg2-binary
   ```

---

## 4️⃣ Configurar o Banco de Dados PostgreSQL

1. **Acessar o PostgreSQL:**
   ```bash
   sudo -u postgres psql
   ```

2. **Criar o banco de dados e conceder privilégios:**
   ```sql
   CREATE DATABASE db_encurtador;
   GRANT ALL PRIVILEGES ON DATABASE db_encurtador TO postgres;
   \q  -- Sair do PostgreSQL
   ```

---

## 5️⃣ Conectar ao Banco via DBeaver (opcional)

1. Abra o DBeaver e clique no ícone de nova conexão.
2. Preencha os campos de conexão:
   - **Host:** `localhost`
   - **Porta:** `5432`
   - **Banco de Dados:** `db_encurtador`
   - **Usuário:** `postgres`
   - **Senha:** (sua senha configurada no PostgreSQL)
3. Teste a conexão e salve.

---

## 6️⃣ Aplicar Migrações e Iniciar o Projeto

1. **Criar as migrações:**
   ```bash
   python manage.py makemigrations
   ```

2. **Aplicar as migrações:**
   ```bash
   python manage.py migrate
   ```

3. **Iniciar o servidor Django:**
   ```bash
   python manage.py runserver
   ```

Acesse o projeto em `http://localhost:8000/`.

---

## ✅ Pronto para o Desenvolvimento!

Agora você está pronto para desenvolver e testar o projeto `URL Shortener`! 🚀

Se tiver dúvidas ou problemas, consulte a documentação oficial do Django e PostgreSQL ou entre em contato com o mantenedor do projeto.

