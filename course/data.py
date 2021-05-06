import pandas as pd
import networkx as nx
import matplotlib
from typing import List

SAMPLE_OBSERVATIONS = pd.DataFrame(
    [
        {'name': 'Kirk', 
        'species': 'human', 
        'gender': 'male',
        'rank': 'captain',
        'shows': set(['Star Trek', 'Star Trek: The Next Generation'])
        },
        {'name': 'Scotty', 
        'species': 'human', 
        'gender': 'male',
        'rank': 'lieutenant commander',
        'shows': set(['Star Trek', 'Star Trek: The Next Generation'])

        },
        {'name': 'Spock', 
        'species': 'half-human, half-vulcan', 
        'gender': 'male',
        'rank': 'first officer',
        'shows': set(['Star Trek', 'Star Trek: The Next Generation', 'Star Trek: Discovery'])
        },
        {'name': 'Picard', 
        'species': 'human', 
        'gender':'male',
        'rank': 'captain',
        'shows': set(['Star Trek: The Next Generation', 'Star Trek: Deep Space Nine'])
        },
        {'name': 'Janeway', 
        'species': 'human', 
        'gender': 'female',
        'rank': 'captain',
        'shows': set(['Star Trek: Voyager'])
        },
        {'name': 'Tuvok', 
        'species': 'vulcan', 
        'gender': 'male',
        'rank': 'science officer',
        'shows': set(['Star Trek: Voyager'])
        },
        {'name': 'Quark', 
        'species': 'ferengi', 
        'gender':'male',
        'rank': 'civilian',
        'shows': set(['Star Trek: Deep Space Nine'])
        },
        {'name': 'Tilly', 
        'species': 'human', 
        'gender':'female',
        'rank': 'lieutenant',
        'shows': set(['Star Trek: Discovery'])
        },
        {'name': 'Stamets', 
        'species': 'human', 
        'gender':'male',
        'rank': 'science officer',
        'shows': set(['Star Trek: Discovery'])
        },
        {'name': 'Worf', 
        'species': 'klingon', 
        'gender':'male',
        'rank': 'lieutenant commander',
        'shows': set(['Star Trek: The Next Generation', 'Star Trek: Deep Space Nine'])
        },
        {'name': 'Odo', 
        'species': 'changeling', 
        'gender':'unknown',
        'rank': 'civilian',    
        'shows': set(['Star Trek: Deep Space Nine'])
        },
    ]
)

CITIES = pd.DataFrame([
    {'name': 'Göteborg',
     'roads': {'E6', 'E20', 'E45'}
    },
    {'name': 'Uddevalla',
    'roads': {'E6', 'E45'}

    },
    {'name': 'Kungsbacka',
    'roads': {'E6'}

    },
    {'name': 'Trollhättan',
    'roads': {'E45'}

    },
    {'name': 'Karlstad',
    'roads': {'E18'}
    },

    {'name': 'Örebro',
    'roads': {'E18', 'E20'}
    },

    {'name': 'Stockholm',
    'roads': {'E20', 'E4', 'E18'}
    },

    {'name': 'Helsingborg',
    'roads': {'E6', 'E4'}
    },

    {'name': 'Jönköping',
    'roads': {'E4'}
    }

])


FLIGHTS = pd.DataFrame([
    {'from': 'Arlanda',
    'to': 'Kastrup'
    },
    {'from': 'Arlanda',
    'to': 'Oslo'
    },
    {'from': 'Landvetter',
    'to': 'Arlanda'
    },
    {'from': 'Landvetter',
    'to': 'Helsingfors'
    },
    {'from': 'Kastrup',
    'to': 'Landvetter'
    },
    {'from': 'Oslo',
    'to': 'Landvetter'
    },
    {'from': 'Oslo',
    'to': 'Helsingfors'
    },
    {'from': 'Helsingfors',
    'to': 'Arlanda'
    },
    {'from': 'Helsingfors',
    'to': 'Oslo'
    },
])

FAMILY = pd.DataFrame([
    {
        'name': 'Per',
        'children': {'Elias', 'Gudmund'},
        'x': 0.35,
        'y': 1.0
    },
    {
        'name': 'Gun',
        'children': {'Elias', 'Gudmund'}, 
        'x': 0.65,
        'y': 1.0   
    },
    {
        'name': 'Elias',
        'children': {'Siv'},   
        'x': 0.35,
        'y': 0.75
    },
    {
        'name': 'Adelia',
        'children': {'Siv'},    
        'x': 0.65,
        'y': 0.75
    },
    {
        'name': 'Gudmund',
        'children': {},
        'x': 0.05,
        'y': 0.75
    },
    {
        'name': 'Siv',
        'children': {},
        'x': 0.35,
        'y': 0.5
    }
])

FAMILY_E = pd.DataFrame([
    {'from': 'Per', 'to': 'Elias'},
    {'from': 'Per', 'to': 'Gudmund'},
    {'from': 'Gun', 'to': 'Elias'},
    {'from': 'Gun', 'to': 'Gudmund'},
    {'from': 'Elias', 'to': 'Siv'},
    {'from': 'Adelia', 'to': 'Siv'}
])


BRIDGES_V = [{
    'id': 1,
    'id': 2,
    'id': 3,
    'id': 4,
    'id': 5,
    'id': 6,
    'id': 7
}]

BRIDGES_E = [
    {'from': 1, 'to': 2},
    {'from': 1, 'to': 3},
    {'from': 1, 'to': 4},
    {'from': 4, 'to': 6},
    {'from': 5, 'to': 6},
    {'from': 4, 'to': 7},
    {'from': 3, 'to': 2},
    {'from': 7, 'to': 5}
]

def color_from_centrality(G, centrality=nx.degree_centrality, colormap='YlOrRd'):

    c = centrality(G.G)
    cmap = matplotlib.cm.get_cmap(colormap)
    norm = matplotlib.colors.Normalize(vmin=0, vmax=max(c.values()))

    hex = lambda x: matplotlib.colors.rgb2hex(x)
    return [hex(cmap(norm(v))) for k, v in c.items()]
    

def color_from_degree_centrality(G, colormap='YlOrRd') -> List:

    return color_from_centrality(G, nx.degree_centrality, colormap)

def color_from_betweenness_centrality(G, colormap='YlOrRd') -> List:

    return color_from_centrality(G, nx.betweenness_centrality, colormap)

def color_from_closeness_centrality(G, colormap='YlOrRd') -> List:

    return color_from_centrality(G, nx.closeness_centrality, colormap)