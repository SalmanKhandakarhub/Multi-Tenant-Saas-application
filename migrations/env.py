from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# Import your models
from src.models.master_models import Base as MasterBase
from src.models.tenant_models import Base as TenantBase
from src.core.config import settings

# This is the Alembic Config object, which provides access to the .ini file.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Get the target database from Alembic extra arguments
extra_args = context.get_x_argument(as_dictionary=True)
target_db = extra_args.get("db_name", "master")  # Default to "master" if not provided

# Define master and tenant-specific migration configurations
if target_db == "master":
    target_metadata = MasterBase.metadata
    db_url = str(settings.SQLALCHEMY_DATABASE_URI()).replace('%', '%%')
    version_folder = "migrations/master"
else:
    target_metadata = TenantBase.metadata
    db_url = str(settings.SQLALCHEMY_DATABASE_URI(target_db)).replace('%', '%%')
    version_folder = "migrations/tenant"

# Set script location dynamically
context.script.__dict__.pop('_version_locations', None)
context.script.version_locations = [version_folder]

# Set the SQLAlchemy URL dynamically
config.set_main_option("sqlalchemy.url", db_url)

# Function for running migrations offline
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

# Function for running migrations online
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine if running online or offline migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
