from sqlmodel import create_engine, SQLModel

sqlite_db_name = "databse.db"
sqlite_url = f"sqlite:///{sqlite_db_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)