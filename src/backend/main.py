from backend.api.router import router
from fastapi import FastAPI
from backend.database.connections import get_db_connection_url
from backend.database.manager import DatabaseManager


DATABASE_URL = get_db_connection_url()


def initialize_database():
    db_manager = DatabaseManager(DATABASE_URL)
    db_manager.create_db_and_tables()


def create_app():
    app = FastAPI()
    app.on_event("startup")(initialize_database)
    app.include_router(router)

    return app