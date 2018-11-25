import pandas as pd
from graph_tool.all import *
from multiprocessing import Pool

# get a df and return the graph with a list of names of nodes
def calc(tup):

    indexNumber = tup[0]
    company = tup[1]
    country = tup[2]

    df = inputdf[~(((inputdf.iloc[:,3] == country) & (inputdf.iloc[:,4] == country)) & ((inputdf.iloc[:,0] != company ) | (inputdf.iloc[:,6] =='C')))]
    # First part: countries which are NOT the current country are kept, jump to else directly
    # Second parenses: (both countries are current country)
            # if the company side is not the company, drop (ignoring the other side)
            # if the company side is the company but the other side is a company drop, too.
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

    ee, eigp = eigenvector(g, weight = g.edge_properties['weight'])

    # save to dataframe
    resultdf = pd.DataFrame({'code':namelist,'VertesEigenvector':eigp.a})

#    resultdf.to_pickle(company+'.pkl')

    resultdf[resultdf.code == company].to_csv( str(indexNumber).zfill(7) +company+'.csv', index = False, header = None)
#    print (company)


#read file
inputdf = pd.read_pickle("3relwithcountryrevised.pkl")
c2cty = pd.read_pickle("c2ctyBatch2.pkl")
tuples = [tuple(x) for x in c2cty.reset_index().values]

p = Pool(72)
p.map(calc,tuples)
