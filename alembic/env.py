import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context

# Adiciona o diretório atual ao path para importar os modelos
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importa TODOS os modelos para registro no metadata
from models.genre import Genre  # noqa: F401
from models.user import User  # noqa: F401
from models.watchlist import Watchlist  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = SQLModel.metadata

def get_url():
    """Obtem a URL do banco de dados com suporte a SQLite e PostgreSQL"""
    database_url = os.getenv("DATABASE_URL", "sqlite:///./movie_app.db")

    # Log para debug
    print(f"Usando database: {database_url}")

    # Para PostgreSQL, garante que esta usando psycopg2
    if database_url.startswith("postgresql://") and "postgresql+psycopg2://" not in database_url:
        database_url = database_url.replace("postgresql://", "postgresql+psycopg2://")
        print(f"Database URL ajustada para: {database_url}")

    return database_url

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()