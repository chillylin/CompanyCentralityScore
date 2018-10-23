from graph_tool.all import *

g = Graph(directed=False)

# load the network
g.load("networkwithweightclo.xml.gz")

# declare property map of vertex to store closeness of vertex
clo_vert = g.new_vertex_property("double")

graph_tool.centrality.closeness(g, weight=g.edge_properties['weight'], source=None, vprop=clo_vert, norm=True, harmonic=False)

g.vertex_properties['VertexCloseness'] = clo_vert

# save the final graph
g.save("networkwithclo.xml.gz")