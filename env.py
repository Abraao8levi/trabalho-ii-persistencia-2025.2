import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Importa todos os modelos para que o Alembic autogenerate os reconheça
# Certifique-se de que todos os seus modelos SQLModel sejam importados em algum lugar
# que seja alcançável a partir daqui.
# from app.models import Movie, User # Exemplo de importação de modelos

# esta é a configuração do Alembic, que fornece acesso aos
# valores .ini dentro do script de configuração.
config = context.config

# Interpreta o arquivo de configuração para o logging do Python.
# Esta linha basicamente configura os loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# adicione o MetaData do seu modelo aqui para suporte ao 'autogenerate'
# Para SQLModel, o metadata está em SQLModel.metadata
target_metadata = SQLModel.metadata

# outras opções da configuração, tiradas da seção [alembic]:
# ... etc.


def get_url():
    """
    Retorna a URL do banco de dados a partir da variável de ambiente DATABASE_URL.
    Usa um valor padrão se a variável não estiver definida.
    """
    default_url = "sqlite:///./movie_app.db"
    return os.getenv("DATABASE_URL", default_url)


def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline'.

    Isso configura o contexto apenas com uma URL
    e não um Engine, embora um Engine também seja aceitável
    aqui. Ao pular a criação do Engine, não precisamos
    nem mesmo de um DBAPI disponível.

    As chamadas para context.execute() aqui emitem a string fornecida para a
    saída do script.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações no modo 'online'.

    Neste cenário, precisamos criar um Engine
    e associar uma conexão com o contexto.

    """
    # Define a URL do banco de dados no objeto de configuração do Alembic
    # a partir da variável de ambiente.
    configuration = config.get_section(config.config_main_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()