from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

PaperAuthor = Table(
    'paper_author', Base.metadata,
    Column('paper_id', ForeignKey('papers.doi'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True)
)

class Paper(Base):
    __tablename__ = 'papers'

    doi = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    authors = relationship(
        "Author",
        secondary=PaperAuthor,
        back_populates="papers"
    )

    def __repr__(self):
        return f"<Paper({self.title})>"


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    papers = relationship(
        "Paper",
        secondary=PaperAuthor,
        back_populates="authors"
    )

    def __repr__(self):
        return f"<Author({self.name})>"
        


engine = create_engine(
    "sqlite:///output/papers.db",
    #echo=True
)
SessionFactory = sessionmaker(bind=engine)
