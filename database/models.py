from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Text, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

PaperAuthor = Table(
    'paper_author', Base.metadata,
    Column('paper_id', ForeignKey('paper.doi'), primary_key=True),
    Column('author_id', ForeignKey('author.id'), primary_key=True)
)

PaperKeyword = Table(
    'paper_keyword', Base.metadata,
    Column('paper_id', ForeignKey('paper.doi'), primary_key=True),
    Column('keyword_id', ForeignKey('keyword.id'), primary_key=True)
)


class Paper(Base):
    __tablename__ = 'paper'
    doi = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    year = Column(Integer, nullable=False)
    authors = relationship(
        "Author",
        secondary=PaperAuthor,
        back_populates="papers"
    )
    keywords = relationship(
        "Keyword",
        secondary=PaperKeyword,
        back_populates="papers"
    )

    def __repr__(self):
        return f"<paper({self.title})>"


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    papers = relationship(
        "Paper",
        secondary=PaperAuthor,
        back_populates="authors"
    )

    def __repr__(self):
        return f"<author({self.name})>"


    
keyword_types = ('author', 'index')    

class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False)
    keyword_type = Column(String, nullable=False)

    papers = relationship(
        "Paper",
        secondary=PaperKeyword,
        back_populates="keywords"
    )

    @property
    def keyword_type(self):
        return self._keyword_type

    @keyword_type.setter
    def keyword_type(self, value):
        if value not in keyword_types:
            raise ValueError(
                f'{value} not in {keyword_types}'
            )
        self._keyword_type = value


engine = create_engine(
    "sqlite:///output/papers.db",
    #echo=True
)
SessionFactory = sessionmaker(bind=engine)
