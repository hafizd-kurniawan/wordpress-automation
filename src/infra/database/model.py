from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def migrate(databaseUrl: str):
    global Base
    engine = create_engine(databaseUrl)
    inspector = inspect(engine)
    existingTables = inspector.get_table_names()
    tablesToCreate = [
        table for table in Base.metadata.tables.keys() if table not in existingTables
    ]
    if tablesToCreate:
        print(f"Migrating tables: {tablesToCreate}")
        Base.metadata.create_all(engine)
    else:
        print("All tables already exist, no migration needed")
    Session = sessionmaker(bind=engine)
    return Session()


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False, index=True)
    url = Column(Text, nullable=False, unique=True)
    category = Column(Text, nullable=True)
    tag = Column(Text, nullable=True)
    template = Column(Text, nullable=True)
    internal_link = Column(Integer, nullable=True)
    scraping_date = Column(DateTime, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
