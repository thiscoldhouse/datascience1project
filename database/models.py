from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


Base = declarative_base()


class Author(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)


class Paper(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    abstract = Column(Text, nullable=True)    



engine = create_engine("sqlite:///database/papers.db")
SessionFactory = sessionmaker(bind=engine)
    
