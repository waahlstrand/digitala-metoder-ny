import networkx as nx
from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd
import itertools
from bokeh.io import output_file, show, output_notebook
from bokeh.models import (ZoomInTool, ZoomOutTool, Circle, EdgesAndLinkedNodes, HoverTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool, PanTool, NodesOnly)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

# Make visible in notebook
output_notebook()

SAMPLE_V = [
    {'id': 1},
    {'id': 2},
    {'id': 3},
    {'id': 4},
    {'id': 5},
    {'id': 6},
    {'id': 7}
]

SAMPLE_E = [
    {'from': 1, 'to': 2},
    {'from': 1, 'to': 3},
    {'from': 1, 'to': 4},
    {'from': 2, 'to': 3},
    {'from': 2, 'to': 4},
    {'from': 3, 'to': 4},
    {'from': 6, 'to': 5},
    {'from': 1, 'to': 2}

]

class Network:

    def __init__(self, V: List[Dict], E: List[Dict]) -> None:
        
        self.V = V
        self.E = E

        self.keys = []

        for v in self.V:
            self.keys.extend(v.keys())

        self.keys = set(self.keys)

        # Check if the nodes have specified x, y positions
        self.has_layout = all([('x' in v.keys() and 'y' in v.keys()) for v in self.V])

        self.G = nx.Graph()

        self.G.add_nodes_from([(v['id'], v) for v in self.V])
        self.G.add_edges_from([e.values() for e in self.E])

        if self.has_layout:
            self.layout = { v['id']: [ v['x'], v['y'] ] for v in self.V }

    def plot(self, layout = None, fig_size=(400,400), node_size=15, fill_color=None, title='Interactive graph', scale=0.5, 
       center=(0.5, 0.5), **kwargs):

        if layout is None:
            if self.has_layout:
                # layout = lambda x: self.layout
                g = from_networkx(self.G, self.layout, scale=scale, center=center, **kwargs)

            else:
                layout = nx.random_layout
                g = from_networkx(self.G, layout, center=(0,0))
        
        else:
            g = from_networkx(self.G, layout, scale=scale, center=center, **kwargs)


        # Create canvas area
        plot = Plot(plot_width=fig_size[0], 
                    plot_height=fig_size[1], 
                    x_range=Range1d(-0.1,1.1), 
                    y_range=Range1d(-0.1,1.1)
                    )
        
        plot.title.text = title
        plot.add_tools(PanTool(), 
                       HoverTool(tooltips=[(key, f"@{key}") for key in self.keys]), 
                       TapTool(), 
                       ZoomInTool(),
                       ZoomOutTool())


        # Settings for rendering the graph
        if fill_color is not None:
            g.node_renderer.data_source.data['colors'] = fill_color

            g.node_renderer.glyph = Circle(size=node_size, fill_color='colors', fill_alpha=0.5)
        else: 

            g.node_renderer.glyph = Circle(size=node_size, fill_color=Spectral4[0], fill_alpha=0.5)

        g.node_renderer.selection_glyph = Circle(size=node_size, fill_color=Spectral4[2])
        g.node_renderer.hover_glyph = Circle(size=node_size, fill_color=Spectral4[1])

        g.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.5, line_width=2)
        g.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=2)
        g.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=2)

        # Make nodes and edges selectable and hoverable
        g.selection_policy = NodesAndLinkedEdges()
        g.inspection_policy = NodesOnly()

        plot.renderers.append(g)

        # show(plot)

        return plot


    def nodes(self):

        return self.V

    def edges(self):

        return self.E

    @classmethod
    def from_networkx(cls, G):
        V = [{'id': v} for v in G.nodes()]
        E = [{'from': e[0], 'to': e[1]} for e in G.edges()]

        return cls(V, E)

SAMPLE_NETWORK = Network(SAMPLE_V, SAMPLE_E)

def pairwise_intersection(d: List, attribute: str, identifier: str):

    # Generate indexes of all observations
    idxs = range(len(d))

    # Create all pairs of indexes
    pairs = itertools.combinations(idxs, 2)

    # Function to check pairwise set interaction
    overlap = lambda i, j: bool(d[i][attribute].intersection(d[j][attribute]))
    
    return ({'from': d[i][identifier], 'to': d[j][identifier]} for i,j in pairs if overlap(i,j))


def from_excel_files(nodes_file, edges_file):
    
    df_V = pd.read_excel(nodes_file)
    df_E = pd.read_excel(edges_file)

    V = df_V.to_dict('records')
    E = df_E.to_dict('records')

    return V, E

