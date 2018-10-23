from graph_tool.all import *

g = Graph(directed=False)

# load the network
g.load("networkwithweightbet.xml.gz")

# declare property map of vertex to store betweenness of vertex
bet_vert = g.new_vertex_property("double")
# declare property map of edge to store betweenness of edge
bet_edge = g.new_edge_property("double")

# Calculate the betweenness; Using wtmp as weight, 
# return the betweenness of vertex to bet_vert, 
# return the betweenness of edge to bet_edge,
graph_tool.centrality.betweenness(g, pivots=None, vprop=bet_vert, eprop=bet_edge, weight=g.edge_properties['weight'], norm=False)

# incorprate the betweeness map (both edge and vertex) into the graph
g.edge_properties['EdgeBetweenness'] = bet_edge
g.vertex_properties['VertesBetweenness'] = bet_vert

# save the final graph
g.save("networkwithbet.xml.gz")
