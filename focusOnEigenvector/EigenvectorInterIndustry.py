import pandas as pd
import os
from graph_tool.all import *
from multiprocessing import Pool

# get a df and return the graph with a list of names of nodes
def calc(tup):

    indexNumber = tup[0]
    company = tup[1]
    country = tup[2]
    # extract information from the input tuple

    dlist = pd.DataFrame ({'director':pd.unique(inputdf[(inputdf.Node1 == company)& (inputdf.cat2 == 'D')].Node2)})
    # build a dataframe of all director of the company
    dlist['mk'] = 1
    # set a marker of directors

    df = df.join(dlist.set_index('director'), on = 'Node2')
    # Join the director dataframe to the original dataframe, i.e., mark the relationships of those directors
    del dlist

    df = df[~(((df.Node1ind == ind) & (df.Node2ind == ind)) | ((df.Node1 != company) & (df.mk == 1) & (df.Node1ind == ind)))]
    # First part: industry which are NOT the current country are kept, jump to else directly
        # Same industry will give a TRUE and short circuit the inner expression, and get opposite when come outside
    # Second part: get a TRUE when
            # the relationship is about those directors of the company, and,
            # the other node is not the company, and,
            # the other node is in the same industry
        # and then the relationship will be dumped when come outside

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
    del df

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
inputdf = pd.read_pickle("3relwithindustry.pkl")
companylist = pd.read_pickle("batch8.pkl").reset_index().values

#read existing csvfiles and get vertexlist already calculated
vertexlist = []
filelist = os.listdir()
for item in filelist:
        vertexlist.append(item[7:-4])

# build a  list  of tuples, test all record in pickled DataFrame against existing file
# and add those not calculated to tuple list.
tuples = []
for company in companylist:
    if company[1] not in vertexlist:
        tuples.append(tuple(company))
    else:
        print (company[1]+' is skipped')


p = Pool(4)
p.map(calc,tuples)
