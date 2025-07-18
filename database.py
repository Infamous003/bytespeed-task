from sqlmodel import create_engine, SQLModel, Session

sqlite_db_name = "databse.db"
sqlite_url = f"sqlite:///{sqlite_db_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session