import pandas as pd
from graph_tool.all import *

# read data from a hdf5 file
df = pd.read_hdf('data.h5', 'df')
# first [0] and second [1] columns are nodes, the third [2] column is weight

# get first two columns to build network
testsamples = df.iloc[:,0:2].values

# declare the graph
g = Graph(directed=False)

# using the pair of nodes to build a network (without weight yet)
# Since we used hash, the returning object is a map storing the name of each vertex
namemap = g.add_edge_list(testsamples, hashed=True, string_vals=False)

# incorporate the map into the graph as a property
g.vertex_properties['name'] = namemap

# save the unweighted graph with a map of name
g.save("networkwithname.xml.gz")



# declare a property map of edges to store weight
wtmp = g.new_edge_property("double")

# assign the third [2] column to the weight map
wtmp.a = df.iloc[:,2]
# incorporate the weight map into the graph as a property
g.edge_properties['weight'] = wtmp


# declare property map of vertex to store betweenness of vertex
bet_vert = g.new_vertex_property("double")
# declare property map of edge to store betweenness of edge
bet_edge = g.new_edge_property("double")


# save weight along with the network
g.save("networkwithweight.xml.gz")
