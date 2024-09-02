from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('sqlite:///books.db')
Session = sessionmaker(bind=engine)

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    cover_path = Column(String, nullable=True)

    pages = relationship("Page", back_populates="book")

class Page(Base):
    __tablename__ = 'pages'
    
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    title = Column(String, nullable=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    
    book = relationship("Book", back_populates="pages")

Base.metadata.create_all(engine)  # Create the tables.
