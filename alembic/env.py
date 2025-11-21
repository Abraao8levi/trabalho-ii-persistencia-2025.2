import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

import models  # noqa: F401 # usado para registrar os modelos no metadata
from alembic import context

# Garantir que o diretório do projeto esteja no sys.path para importar o pacote `models`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata para autogenerate (SQLModel)
target_metadata = SQLModel.metadata

# helper: prefer variável de ambiente DATABASE_URL se fornecida
def _get_database_url() -> str | None:
    # Prioridade: DATABASE_URL do ambiente, depois alembic.ini
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return database_url
    return config.get_main_option("sqlalchemy.url")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = _get_database_url()
    if url is None:
        raise ValueError("Database URL não encontrada. Configure DATABASE_URL ou sqlalchemy.url no alembic.ini")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Se DATABASE_URL estiver definida, sobrescreve a configuração
    database_url = _get_database_url()
    if database_url:
        configuration = config.get_section(config.config_ini_section, {})
        configuration['sqlalchemy.url'] = database_url
    else:
        configuration = config.get_section(config.config_ini_section, {})
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Detecta se é SQLite para habilitar render_as_batch
        dialect_name = connection.dialect.name
        is_sqlite = dialect_name == "sqlite"
        
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=is_sqlite,
            compare_type=True,  # Detecta mudanças nos tipos de colunas
            compare_server_default=True,  # Detecta mudanças em defaults
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()