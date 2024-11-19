from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from mod.model.idp_classes import Base, engine  # Import Base and engine from your models

# This is the Alembic Config object, which provides access to .ini values
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData object for autogenerate support
target_metadata = Base.metadata



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    
    Configures the context with just a database URL.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,  # Enables type changes detection
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    
    Configures the context with an actual database connection.
    """
    connectable = engine  # Use your existing engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Enables type changes detection
        )

        with context.begin_transaction():
            context.run_migrations()


# Decide whether to run offline or online migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
