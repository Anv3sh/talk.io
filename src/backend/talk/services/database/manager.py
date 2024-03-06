from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlmodel import Session, SQLModel, create_engine
from talk.api.logger import logger
from talk.services.database.models import (Group, GroupUserLink, Message, User,
                                           UserMessageLink)


class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        backend_dir = Path(__file__).parent.parent.parent
        self.script_location = backend_dir / "alembic"
        self.alembic_cfg_path = backend_dir / "alembic.ini"
        self.engine = create_engine(database_url)  # noqa

    def __enter__(self):
        self._session = Session(self.engine)
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:  # If an exception has been raised
            print(
                f"Session rollback because of exception: {exc_type.__name__} {exc_value}"  # noqa
            )
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()

    def get_session(self):
        with Session(self.engine) as session:
            yield session

    def run_migrations(self):
        logger.info(f"Running DB migrations in {self.script_location}")
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", str(self.script_location))
        alembic_cfg.set_main_option("sqlalchemy.url", self.database_url)
        command.upgrade(alembic_cfg, "head")

    def create_db_and_tables(self):
        print("Creating database and tables")
        try:
            SQLModel.metadata.create_all(self.engine)
        except Exception as exc:
            print(f"Error creating database and tables: {exc}")
            raise RuntimeError("Error creating database and tables") from exc

        from sqlalchemy import inspect

        inspector = inspect(self.engine)
        required_tables = [
            "user",
            "group",
            "message",
            "group_user_link",
            "user_message_link",
            "alembic_version",
        ]
        for table in inspector.get_table_names():
            if table not in required_tables:
                print(table)
                print("Something went wrong creating the database and tables.")
                print("Please check your database settings.")
                raise RuntimeError(
                    "Something went wrong creating the database and tables."
                )
        else:
            print("Database and tables created successfully")
        print(inspector.get_table_names())
