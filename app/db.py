import os
from sqlalchemy import create_engine,Column,Integer,String,Text
from sqlalchemy.orm import declarative_base,sessionmaker
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
load_dotenv()
database_url=os.getenv("DATABASE_URL")
engine=create_engine(database_url)
SessionLocal=sessionmaker(bind=engine)
Base = declarative_base()

EMBEDDING_DIM=384

class Chunk(Base):
    __tablename__="chunks"
    id=Column(Integer,primary_key=True)
    source_file=Column(String,nullable=False)
    section_title=Column(String,nullable=True)
    page_number=Column(Integer,nullable=True)
    content=Column(Text,nullable=False)
    embedding=Column(Vector(EMBEDDING_DIM),nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__=="__main__":
    init_db()
    print("Tables created.")