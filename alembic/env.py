from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models
from src.db.models import Base
from src.db.iteration_models import IterationLog

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Prefer Supabase PostgreSQL with SQLite fallback
supabase_url = os.getenv('DATABASE_URL')
try:
    if supabase_url and 'postgresql' in supabase_url:
        # Escape % characters for ConfigParser
        supabase_url = supabase_url.replace('%', '%%')
        config.set_main_option('sqlalchemy.url', supabase_url)
        print("[INFO] Using Supabase PostgreSQL")
    else:
        raise Exception("No PostgreSQL URL found")
except Exception as e:
    print(f"[WARN] Supabase not available ({e}), using SQLite fallback")
    config.set_main_option('sqlalchemy.url', 'sqlite:///prompt_to_json.db')

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
