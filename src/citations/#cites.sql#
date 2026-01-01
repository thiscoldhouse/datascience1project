select p2.year, p2.community, p2.doi, p2.title
from paper p1
inner join citation c
on c.cited_paper_doi = p1.doi
inner join paper p2
on p2.doi = citing_paper_doi
where p1.community=1432
and p2.community =6075
order by p2.year;
