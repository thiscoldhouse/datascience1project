from scholarly import scholarly
import string
import io
import PyPDF2
import json
import requests
import os
from nltk import tokenize, FreqDist, bigrams
from nltk.corpus import stopwords
import itertools
from collections import Counter

import pdb
import pprint

search_data_dir = 'search_data/{fname}'
papers_dir = 'papers_data/'


def get_raw_data_from_web():
    print('Fetching...')
    # search = scholarly.search_pubs_custom_url(
    #     '/scholar?q=misinformation&hl=en&as_sdt=0%2C46&as_ylo=2015&as_yhi=2020'
    # )
    search = scholarly.search_pubs('teeth')
    print('Fetched!')
    data = []
    for i, item in enumerate(search):
        data.append(item)
        if i==0:
            continue
        if i % 20 == 0 or i+1 == len(search):
            print(f'Saving progress at {i}')
            all_data = load_data_from_file()
            all_data.extend(data)
            with open(
                    search_data_dir.format(fname='{i}.json'), 'w+'
            ) as f:
                f.write(json.dumps(all_data))
            data = []
            

def load_data_from_file():
    print('Loading data from file')
    with open(search_data_fname, 'r') as f:
        return json.loads(f.read())

    
def get_pdf_text_from_url(pdf_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'
    }
    response = requests.get(
        url=pdf_url, headers=headers, timeout=120
    )
    reader = PyPDF2.PdfReader(io.BytesIO(response.content))
    num_pages = len(reader.pages)
    all_text = []
    for page in reader.pages:
        text = page.extract_text() 
        all_text.append(text)
        
    return '\n'.join(all_text)


def extract_data_from_google_scholar_query(data):
    def save(papers, i):
        print(f'Saving at {i}')            
        with open(f'{papers_dir}{i}.json', 'w+') as f:
            f.write(json.dumps(papers))

    papers = []
    i = 0
    for paper in data:
        if 'eprint_url' in paper.keys():
            try:
                pdf_data = get_pdf_text_from_url(
                    paper['eprint_url']
                )
            except Exception as e:
                print(f'Failed to get eprint url with exception:')
                print(e)
                continue
            
            papers.append({
                'title': paper['bib']['title'],
                'year': paper['bib']['pub_year'],
                'pdf_data': pdf_data,
                'raw_data': paper,
            })
            if i % 10 == 0 and i > 1:
                save(papers, i)    
                papers = []
                
            print(i)
            i += 1

    save(papers, i)


def load_paper_data_from_files():
    papers = []
    for fname in os.listdir(papers_dir):
        filename = os.fsdecode(fname)
        print(f'Opening {fname}')
        with open(f'{papers_dir}{filename}', 'r') as f:
            papers.extend(json.loads(f.read()))
            
    return papers


                
def main():
    get_raw_data_from_web()
    # data = load_data_from_file()
    # extract_data_from_google_scholar_query(data)
    # data = load_paper_data_from_files()
    # results = []

    
if __name__ == '__main__':
    main()
