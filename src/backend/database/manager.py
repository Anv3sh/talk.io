from sqlmodel import create_engine, Session, SQLModel
from backend.database.connections import get_db_connection_url
from backend.database.models import user, pfp

class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
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

    def create_db_and_tables(self):
        print("Creating database and tables")
        try:
            SQLModel.metadata.create_all(self.engine)
        except Exception as exc:
            print(f"Error creating database and tables: {exc}")
            raise RuntimeError("Error creating database and tables") from exc
        
        from sqlalchemy import inspect

        inspector = inspect(self.engine)
        required_tables = ["user","pfp"]
        for table in inspector.get_table_names():
            if table not in required_tables:
                print("Something went wrong creating the database and tables.")
                print("Please check your database settings.")
                raise RuntimeError("Something went wrong creating the database and tables.")
        else:
            print("Database and tables created successfully")
        print(inspector.get_table_names())
