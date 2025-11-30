import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context

# Permite importar os módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Importa os modelos (não utilizados diretamente, mas necessários para SQLModel.metadata)
from models.models import Actor, Genre, Movie, MovieActor, MovieGenre  # noqa: F401

# Carrega variáveis do .env
load_dotenv()

# Arquivo alembic.ini
config = context.config

# Configura logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados que o Alembic vai usar para autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Executa migrações no modo offline."""
    url = os.getenv("DATABASE_URL")

    if not url:
        raise RuntimeError("DATABASE_URL não está definido no ambiente!")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações no modo online."""
    configuration = config.get_section(config.config_ini_section)

    # Sobrescreve sqlalchemy.url com o valor carregado do .env
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise RuntimeError("DATABASE_URL não está definido no ambiente!")

    configuration["sqlalchemy.url"] = db_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()