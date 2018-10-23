from graph_tool.all import *

g = Graph(directed=False)

# load the network
g.load("networkwithweighteig.xml.gz")

# declare property map of vertex to store eigenvector of vertex
eig_vert = g.new_vertex_property("double")

graph_tool.centrality.eigenvector(g, weight=g.edge_properties['weight'], vprop=eig_vert, epsilon=1e-06, max_iter=None)

g.vertex_properties['VertesEigenvector'] = eig_vert

# save the final graph
g.save("networkwitheig.xml.gz")
