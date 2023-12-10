import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine


def get_db_connection_url():
    load_dotenv(".env", override=True)

    is_prod_mode = os.getenv("PROD") or ""

    if is_prod_mode == "true":
        username = os.getenv("PROD_DB_USERNAME") or ""
        password = os.getenv("PROD_DB_PASSWORD") or ""
        host_url = os.getenv("PROD_DB_HOST_URL") or ""
        selected_db = os.getenv("PROD_SELECTED_DB") or ""
    else:
        username = os.getenv("DEV_DB_USERNAME") or ""
        password = os.getenv("DEV_DB_PASSWORD") or ""
        host_url = os.getenv("DEV_DB_HOST_URL") or ""
        selected_db = os.getenv("DEV_SELECTED_DB") or ""

    credentials = f"postgresql://{username}:{password}"
    database_url = credentials + host_url + selected_db
    return database_url


engine = create_engine(get_db_connection_url())


def get_db_session():
    with Session(engine) as session:
        yield session
