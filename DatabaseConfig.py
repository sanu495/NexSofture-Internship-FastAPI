from sqlmodel import SQLModel, create_engine, Session

sqlite_url = f"sqlite:///./creator.db"
engine= create_engine(sqlite_url,echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
         yield session
         