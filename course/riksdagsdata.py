import json
from typing import Dict, List
import requests
import itertools

class Motion:

    def __init__(self, id, doc_id, date, title, subtitle, authors) -> None:
        
        self.id = id
        self.doc_id = doc_id
        self.date = date
        self.title = title
        self.subtitle = subtitle
        self.authors = authors

    @classmethod
    def from_response(cls, **kwargs):

        date = kwargs.get('datum', None)
        id   = kwargs.get('id', None)
        title = kwargs.get('titel', None)
        subtitle = kwargs.get('undertitel', None)
        doc_id = kwargs.get('dok_id', None)

        author_list = kwargs.get('dokintressent') 

        if author_list is not None:

            author_params = author_list.get('intressent', None)
            authors = [Person(**a) for a in author_params if a is not None]
        
        else:
            authors = []

        return cls(id, doc_id, date, title, subtitle, authors)

    def __str__(self):
        return f'Motion: {self.title}'

    def __repr__(self):
        return str(self)


class Person:
    def __init__(self, roll, namn, partibet, intressent_id) -> None:
        self.id = intressent_id
        self.name = namn
        self.party = partibet
        self.role = roll

    def __str__(self):
        return f'{self.name} ({self.party})'

    def __repr__(self):
        return str(self)

class Riksdagsdata:

    def __init__(self, api) -> None:
        self.api = api
        self.content = 'dokumentlista'
        self.next_page = '@nasta_sida'
        self.documents = 'dokument'

    def get(self, kind, query, start_date, end_date, sort='datum', match=False, limit=100):
        
        # Use appropriate parameter names
        kind = normalize_kind(kind)

        params = {
            'sok': query,
            'doktyp': kind,
            'from': start_date,
            'tom': end_date,
            'utformat': 'iddump'
        }

        # Make request for all ids
        response = requests.get(self.api, params=params)

        # Get all matching motions
        ids = [id for id in response.text.split(',')]
        count = 0

        params = {
            'id': None,
            'utformat': 'json'
        }

        for id in ids:

            params['id'] = id

            # Get the individual document
            response = requests.get(self.api, params=params)
            print(response.url)
            response = response.json()

            
            # Parse content
            document = response.get(self.content)\
                               .get(self.documents)
            document = document[0]

            # Create document type
            m = Motion.from_response(**document)

            count += 1

            yield m

            if count >= limit:
                break
        


    def motions(self, query, start_date, end_date, sort='datum', match=False, limit=100):

        params = {
            'sok': query,
            'doktyp': 'mot',
            'from': start_date,
            'tom': end_date,
            'sort': sort,
            'exakt': int(match),
            'utformat': 'json'
        }
        
        return self._get_motions(params, limit=limit)
    
    def _get_motions(self, params: Dict, limit: int):

        n_motions = 0
        page = 1
        has_more = 1
        while has_more:

            # Make call to API
            response = self._get_response(params, page)

            # Parse content
            content = response.get(self.content)
            documents = content.get(self.documents)

            # Check if there is a next page
            has_next_page = self.next_page in content.keys()
            
            for d in documents:

                # Create document type
                m = Motion.from_response(**d)
                
                yield m

            # Increase counters towards limit and test yield
            page += 1
            n_motions += len(documents)
            has_more = (n_motions < limit) and has_next_page

    def _get_response(self, params: Dict, page: int):

        # Perform the HTTP request, using page=page
        params['p'] = page

        response = requests.get(self.api, params=params)

        # print(response.url)

        return response.json()


party_color = {'V' : "#DA291C",
                   'S' : "#E8112d",
                   'MP' : "#83CF39",
                   'C' : "#009933",
                   'FP' : "#006AB3",
                   'L' : "#006AB3",
                   'M' : "#52BDEC",
                   'KD' : "#000077",
                   'NYD': 'pink',
                   'KDS' : "#000077",
                   'SD' : "#DDDD00",
                   'FI' : "#CD1B68",
                   'PP' : "#572B85",
                   '-' : "gray"
                }


def nodes_and_edges_from_motions(motions: List[Motion]):

    all_authors = []
    author_ids  = set()

    nodes = []
    edges = []

    for motion in motions:
        for author in motion.authors:
            if author.id not in author_ids:
                all_authors.append(author)
                author_ids.add(author.id)

                nodes.append({
                    'id': author.id,
                    'name': author.name,
                    'party': f'{author.party}'
                })

        if len(motion.authors) < 2:
            edges.extend({'from': a.id, 'to': a.id} for a in motion.authors)
        else:
            edges.extend([{'from': k.id, 'to': v.id} for k, v in itertools.combinations(motion.authors,2)])
            
    return nodes, edges


def color_from_party(G) -> List:
    
    return [party_color[v['party'].upper()] for v in G.nodes()]


def normalize_kind(kind):

    normalization = {
        'motion': 'mot',
        'mot': 'mot'
        }

    return normalization[kind]