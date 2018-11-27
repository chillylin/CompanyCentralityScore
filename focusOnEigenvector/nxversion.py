import pandas as pd
import networkx as nx

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

    G = nx.from_pandas_edgelist(df, 'Node1', 'Node2', ['Weight'])
    centrality = nx.eigenvector_centrality(G ,max_iter=500, weight = 'Weight' )

    print (centrality[company])
    

inputdf = pd.read_pickle("3relwithcountryrevised.pkl")

# test one case
calc((0,'C15',173))
