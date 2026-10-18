
def main():
    data = None
    with open('output/tables0.text', 'w+') as f:
        data = f.read()

    final_table = {}
    for i, line in enumerate(data.split('\n')):
        try:
            community, terms = line.split('&')
            terms = terms.replace('\\', '')
            final_table[community] = {
                'Unigram',
                'Bigram',
                'Trigram',
            }
            for term in terms.split(','):
                final_table[community]
            
        
