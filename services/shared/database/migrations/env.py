from logging.config import fileConfig
from sqlalchemy import engine_from_config
from alembic import context
from services.shared.database.models import Base
from config.settings.base import Settings

settings = Settings()

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = engine_from_config(configuration, prefix="sqlalchemy.")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()