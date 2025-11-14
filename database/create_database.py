from models import Paper, Author, Keyword, SessionFactory
import json
import csv


class CreateDB:
    def __init__(self):
        self.session = SessionFactory()
        
    def main(self):
        reader = None
        with open('input/data.csv', 'r') as f:
            reader = csv.reader(f)

            columns = next(reader)
            col_to_i = {
                col: i for i, col in enumerate(columns)
            }
            for row in reader:
                paper = self.get_paper(
                    row[col_to_i['DOI']],
                    row[col_to_i['Title']],
                    row[col_to_i['Abstract']],
                )
                
                if paper is None:
                    continue
                
                self.session.add(paper)
                authors = self.get_authors(
                    row[col_to_i['Authors']],
                    row[col_to_i['Author(s) ID']],
                )
                for author in authors:
                    if paper not in author.papers:
                        author.papers.append(paper)
                    self.session.add(author)

                keywords = self.get_keywords(
                    row[col_to_i['Author Keywords' ]].split(';'),
                    row[col_to_i['Index Keywords']].split(';')
                )
                for keyword in keywords:
                    if keyword not in paper.keywords:
                        paper.keywords.append(keyword)
                        
                self.session.commit()

    def get_paper(self, doi, title, abstract):
        if doi is None:
            return 
        paper = self.session.query(Paper).filter(
            Paper.doi == doi
        ).all()
        if len(paper) > 1:
            raise ValueError()
        elif len(paper) == 0:
            paper = Paper(
                doi=doi,
                title=title,
                abstract=abstract
            )
        else:
            paper = paper[0]

        return paper
        

    def get_authors(self, author_names, author_ids):
        author_names = author_names.split(';')
        author_ids = author_ids.split(';')
        if len(author_names) > len(author_ids):
            raise ValueError()
        elif len(author_names) < len(author_ids):
            author_names.extend([
                '' for _ in range(
                    len(author_ids) - len(author_names)
                )
            ])
            
        for i, author_name in enumerate(author_names):
            author_id = author_ids[i]
            if author_id == '' and author_name == '':
                continue
            
            author_id = int(author_id)            
            author = self.session.query(Author).filter(
                Author.id==int(author_id)
            ).all()

            if len(author) > 1:
                raise ValueError()            
            elif len(author) == 0:
                author = Author(
                    id=int(author_id),
                    name=author_name
                )
            else:
                author = author[0]
                
            yield author

    def get_keywords(self, author_keywords, index_keywords):
        keyword_lists = (author_keywords, index_keywords)
        for i, keyword_type in enumerate(('author', 'index')):
            keywords = keyword_lists[i]
            for keyword_name in keywords:
                if keyword_name is None or keyword_name=='':
                    continue
                
                keyword_name = keyword_name.lower().strip()
                
                keyword = self.session.query(Keyword).filter(
                    Keyword.keyword==keyword_name,
                    keyword_type==keyword_type
                ).all()
                if len(keyword) > 1:
                    raise ValueError()
                elif len(keyword) == 1:
                    keyword = keyword[0]
                else:
                    keyword = Keyword(
                        keyword=keyword_name,
                        keyword_type=keyword_type
                    )
                yield keyword

            
if __name__ == '__main__':
    CreateDB().main()
