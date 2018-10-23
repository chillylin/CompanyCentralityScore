import pandas as pd
from graph_tool.all import *
import pickle
from multiprocessing import Pool
from threading import Thread

# get a df and return the graph with a list of names of nodes
def networkbuilding(df):
    
    # first [0] and second [1] columns are nodes, the third [2] column is weight

    # declare the graph
    g = Graph(directed=False)

    # using the pair of nodes to build a network (without weight yet)
    # Since we used hash, the returning object is a map storing the name of each vertex
    namemap = g.add_edge_list(df.iloc[:,0:2].values, hashed=True, string_vals=False)

    # incorporate the map into the graph as a property
    g.vertex_properties['name'] = namemap

    # declare a property map of edges to store weight
    wtmp = g.new_edge_property("double")

    # assign the third [2] column to the weight map
    wtmp.a = df.iloc[:,2]
    # incorporate the weight map into the graph as a property
    g.edge_properties['weight'] = wtmp
    
    #build a list of names of the nodes
    namelist= []
    for i in namemap:
        namelist.append(i)

    return g, namelist




def process(odf):
    
    g, names = networkbuilding(odf) # using networkbuilding function to build graph and the name of nodes
   
    country = odf.iloc[0,3] # get country code from the dataframe
  
    # create three threads to calculate each network centrality score 
    Thread(target = calc,args=('bet', g, names,country)).start()
    Thread(target = calc,args=('clo', g, names,country)).start()
    Thread(target = calc,args=('eig', g, names,country)).start()



# the multi-functions function 
# arguments:
#   calctype: 'bet' for betweenness; 'clo' for closeness; 'eig' for eigenvector
#   g: the graph
#   names: a list of names of each nodes
#   country: country code for naming the dataframe
def calc(calctype, g, names, country): 
    
    # for betweenness    
    if calctype == 'bet': 
    
        # declare property map of vertex to store betweenness of vertex
        bet_vert = g.new_vertex_property("double")
        # declare property map of edge to store betweenness of edge
        bet_edge = g.new_edge_property("double")

        # Calculate the betweenness; Using wtmp as weight, 
        # return the betweenness of vertex to bet_vert, 
        # return the betweenness of edge to bet_edge,
        graph_tool.centrality.betweenness(g, pivots=None, vprop=bet_vert, eprop=bet_edge, 
                                          weight=g.edge_properties['weight'], norm=False)
        
        # save to dataframe
        resultdf = pd.DataFrame({'code':names,'betweenness':bet_vert.a})
        
    # for closeness
    elif calctype =='clo': 
        # declare property map of vertex to store closeness of vertex
        clo_vert = g.new_vertex_property("double")
        
        #calculation
        graph_tool.centrality.closeness(g, weight=g.edge_properties['weight'], source=None, 
                                        vprop=clo_vert, norm=True, harmonic=False)
        
        # save to dataframe
        resultdf = pd.DataFrame({'code':names,'closeness':clo_vert.a})
    
    elif calctype == 'eig':

        # declare property map of vertex to store eigenvector of vertex
        eig_vert = g.new_vertex_property("double")
        
        #calculation
        graph_tool.centrality.eigenvector(g, weight=g.edge_properties['weight'], 
                                          vprop=eig_vert, epsilon=1e-06, max_iter=None)
        # save to dataframe
        resultdf = pd.DataFrame({'code':names,'VertesEigenvector':eig_vert.a})
    
    else:
        return 0
    
    # save to files
    resultdf.to_pickle(calctype+country+'.pkl')

#read file 
# loc.pkl is a list of dataframes. the dataframes' columns are:
# |node1 | node2 | weight | node1country | ……|
loc = pickle.load( open( "loc.pkl", "rb" ) ) 

# create 16 threads
p = Pool(16)

# using 16 threads to process all elements in loc
p.map(process, loc)

