<div align="center">
  <h1>🎬 Movie Review API</h1>
  <p>
    <strong>Uma API completa para gerenciamento de filmes, avaliações e listas de interesse.</strong>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python 3.13+">
    <img src="https://img.shields.io/badge/FastAPI-0.121.2-009688.svg" alt="FastAPI">
    <img src="https://img.shields.io/badge/SQLModel-0.0.27-blueviolet.svg" alt="SQLModel">
    <img src="https://img.shields.io/badge/Alembic-1.17.2-lightgrey.svg" alt="Alembic">
    <img src="https://img.shields.io/badge/PostgreSQL-blue.svg" alt="PostgreSQL">
  </p>
</div>

## Descrição
A **Movie Review API** é uma solução robusta para gerenciar filmes, atores, gêneros, avaliações e listas de interesse (`watchlists`). Construída com tecnologias modernas de Python, ela oferece uma base sólida e eficiente para aplicações focadas em cinema e entretenimento.

## ✨ Recursos Principais
- **Gerenciamento Completo**: Operações CRUD (Criar, Ler, Atualizar, Deletar) para filmes, atores, gêneros, usuários, avaliações e watchlists.
- **Documentação Automática**: Interface interativa com Swagger UI (`/docs`) e ReDoc (`/redoc`).
- **Migrações de Banco de Dados**: Controle de versão do schema do banco de dados com Alembic.
- **Validação de Dados**: Tipagem forte e validação com SQLModel (baseado em Pydantic).
- **Tratamento de Erros**: Handlers de exceção customizados para respostas de erro claras e consistentes.

## 🛠️ Tecnologias Utilizadas
| Tecnologia | Descrição |
|--------------|----------------------------------------------------------------------|
| **Python 3.13+** | Linguagem de programação principal. |
| **FastAPI** | Framework web de alta performance para construção de APIs. |
| **SQLModel** | Biblioteca que combina SQLAlchemy e Pydantic para interagir com o banco de dados. |
| **PostgreSQL** | Sistema de gerenciamento de banco de dados relacional. |
| **Alembic** | Ferramenta para gerenciar migrações de schema do banco de dados. |
| **Uvicorn** | Servidor ASGI (Asynchronous Server Gateway Interface) para executar a aplicação. |

## 🚀 Começando

### Pré-requisitos
- **Python 3.13** ou superior.
- **Git** para clonar o repositório.
- **PostgreSQL** instalado e em execução.
- **uv** (opcional, mas recomendado) para gerenciamento de dependências.
"
### Instalação
1.  **Clone o repositório**
    A branch principal de desenvolvimento é a `develop`. Clone o projeto e acesse o diretório:
    ```bash
    git clone -b develop https://github.com/seu-usuario/trabalho-ii-persistencia-2025.2.git
    git clone -b develop https://github.com/{SEU_USUARIO_OU_ORGANIZACAO}/trabalho-ii-persistencia-2025.2.git
    cd trabalho-ii-persistencia-2025.2
    ```

2.  **Crie um ambiente virtual e instale as dependências**
    Recomendamos o uso de `uv` para uma instalação mais rápida.
    ```bash
    # Crie o ambiente virtual
    python -m venv .venv
    # Ative o ambiente (Windows)
    .venv\Scripts\activate
    # Ative o ambiente (Linux/macOS)
    # source .venv/bin/activate
    
    # Instale as dependências com uv ou pip
    uv pip install -r requirements.txt 
    # ou: pip install -r requirements.txt
    ```
    > **Nota**: Se o arquivo `requirements.txt` não estiver presente, você pode gerá-lo a partir do `uv.lock` ou instalar as dependências manualmente.

3.  **Configure as Variáveis de Ambiente**
    Crie um arquivo `.env` na raiz do projeto, baseado no exemplo abaixo, e preencha com as credenciais do seu banco de dados PostgreSQL.
    
    **.env.example**
    ```env
    DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"
    ```

4.  **Execute as Migrações do Banco de Dados**
    Para criar ou atualizar as tabelas no banco de dados, execute:
    ```bash
    alembic upgrade head
    ```

## 🏃 Executando a Aplicação
Com o ambiente virtual ativado, inicie o servidor Uvicorn:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
uvicorn app.main:app --reload
```
A API estará disponível em `http://localhost:8000`.

### 📚 Documentação da API
Após iniciar o servidor, você pode acessar a documentação interativa da API nos seguintes endereços:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📂 Estrutura do Projeto
```
trabalho-ii-persistencia-2025.2/
├── alembic/              # Configurações e versões de migração do Alembic
├── app/                  # Código-fonte principal da aplicação
│   ├── crud/             # Lógica de acesso e manipulação de dados (CRUD)
│   ├── models/           # Modelos de dados (SQLModel)
│   ├── routers/          # Definição dos endpoints da API (rotas)
│   ├── schemas/          # Esquemas Pydantic para validação (se aplicável)
│   ├── database.py       # Configuração da conexão com o banco de dados
│   └── main.py           # Ponto de entrada da aplicação FastAPI
├── .env.example          # Arquivo de exemplo para variáveis de ambiente
├── main.py               # Script para iniciar a aplicação
└── README.md             # Este arquivo
```

## 🤝 Como Contribuir
Contribuições são bem-vindas! Para contribuir com o projeto, siga estes passos:

1.  Faça um **Fork** deste repositório.
2.  Crie uma nova branch a partir da `develop`: `git checkout -b feature/sua-feature`.
3.  Faça suas alterações e realize commits com mensagens claras.
4.  Envie suas alterações para o seu fork: `git push origin feature/sua-feature`.
5.  Abra um **Pull Request** para a branch `develop` do repositório original.

## 🧑‍💻 Contribuintes
- @paulohenrique04
- @Abraao8levi
- @JoaoAlves-Web
