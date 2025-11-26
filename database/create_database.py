from models import Paper, Author, Keyword, SessionFactory, Citation
import urllib
import requests
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
                    row[col_to_i['Year']],                    
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

    def get_paper(self, doi, title, abstract, year):
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
                abstract=abstract,
                year=int(year)
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

    def get_citations(self):
        dois = set([
            p.doi for p in self.session.query(Paper).all()
        ])
        papers_to_fetch = self.session.query(Paper).filter(
            Paper.citations_fetched!=True
        ).all()

        for i, paper in enumerate(papers_to_fetch):
            if i % 50 == 0:
                self.session.commit()
                print(f'On {i} of {len(papers_to_fetch)}')
                
            citations = self.get_citations_in_paper(
                paper.doi
            )
            for doi in citations:
                if doi in dois:
                    self.session.add(
                        Citation(
                            citing_paper_doi=paper.doi,
                            cited_paper_doi=doi,
                        )
                    )
            paper.citations_fetched = True
            self.session.add(paper)
        self.session.commit()

    def get_citations_in_paper(self, doi):        
        if doi is None or doi == '':
            return []
        try:
            url = 'https://opencitations.net/index/coci/api/v1/references/{doi}'
            url = url.format(
                doi=urllib.parse.quote_plus(doi)
            )
            r = requests.get(
                url,
                allow_redirects=True,
                headers = {
                    'User-Agent': 'Alejandro Ruiz (mailto:alejandro.ruiz@uvm.edu)'
                },
            )
            if r.status_code != 200:
                print('Something went wrong')
                print(f'Status code {r.status_code} for url {url}')
                return []

            data = None
            try:
                data = r.json()
            except Exception as e:
                print('===============')
                print('Status code is 200 but response is not json')
                print('url :', url)
                print('Response:')
                print(r.text[:200])
                print('===============')
            dois = []
            for row in data:
                yield row['cited']
        except Exception as e:
            print('****************')
            print('****************')            
            print('Warning! Unexpected error getting citations')
            print(e)
            print('****************')
            print('****************')
            return []
        

            
if __name__ == '__main__':
    #CreateDB().main()
    CreateDB().get_citations()
