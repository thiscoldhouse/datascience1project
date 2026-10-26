from create_database import CreateDB

if __name__ == '__main__':
    cdb = CreateDB()
    #cdb.older_papers_backfill()
    cdb.get_citations()
    cdb.session.commit()
    
