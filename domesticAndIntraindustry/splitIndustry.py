
# coding: utf-8

# In[1]:


import re
import pandas as pd
import numpy as np


# # read relationship file

# In[2]:


maindf = pd.read_hdf(r'C:\Users\Chilly Lin\Documents\coding\RA-Combine\03 NetworkBuilding\3rel.h5', 'df')


# #### Change the columns value of maindf to single layer

# In[3]:


maindf.columns = ['Node1', 'Node2', 'Weight']


# # Read Director/Company info

# In[4]:


#siccode = ['AGRI', 'MINE', 'CONS', 'NOTU', 'MANU', 'INFR', 'WHOL', 'RETL', 'FINA', 'SERV', 'PUBA', 'NONC', 'NODT', 'HUMN']
siccode = range(14)

def siccoder(sic):
    
    if sic <1000:
        return siccode[0] #'Agriculture, Forestry and Fishing'
    elif sic < 1500:
        return siccode[1]# 'Mining'
    elif sic < 1800:
        return siccode[2]#'Construction'
    elif sic < 2000:
        return siccode[3]#'not used'
        # drop 3
    elif sic < 4000:
        return siccode[4]#'Manufacturing'
    elif sic < 5000:
        return siccode[5]#'Transportation, Communications, Electric, Gas and Sanitary service'
    elif sic < 5200:
        return siccode[6] #Wholesale Trade
    elif sic < 6000:
        return siccode[7]# Retail Trade
    elif sic < 7000:
        return siccode[8]# Finance, Insurance and Real Estate
    elif sic < 9000:
        return siccode[9] # Services
    elif sic < 9900:
        return siccode[10] # Public Administration
    elif sic < 10000:
        return siccode[11] # Nonclassifiable
        # drop 11
    else:
        return siccode[12] # no data available
        # drop 12
        


# In[7]:


companyinfo = pd.read_csv(r'C:\Users\Chilly Lin\Documents\coding\RA-Combine\04 BvD\imported\companybasicinfo.csv',
                             )[['mk','Primary US SIC code']]
companyinfo['Ccode'] = 'C' + companyinfo.iloc[:,0].map(str) # add 'C' before company mark number
companyinfo.drop('mk',inplace = True, axis = 1) # drop company mark number
#companyinfo.columns = ['ComCtyCode','ComCode'] # change columns' names.
companyinfo['industry'] =companyinfo['Primary US SIC code'].apply(siccoder)
companyinfo.drop('Primary US SIC code', axis =1, inplace = True)


# In[40]:


companyinfo[~((companyinfo.industry == 3) | (
                companyinfo.industry == 11) | (
                companyinfo.industry == 12))].to_pickle('c2ind.pkl')


# In[8]:


directorinfo = pd.read_csv(r'C:\Users\Chilly Lin\Documents\coding\RA-Combine\04 BvD\imported\directorpersonalinfo.csv'
                             )[['dmccode']]
directorinfo['DirectorCode'] = 'D' + directorinfo.iloc[:,0].map(str)
directorinfo.drop('dmccode',inplace = True, axis = 1) # drop company mark number
directorinfo['industry'] = siccode[13]


# In[9]:


# Combine director and company

companyinfo.columns = ['vertex','industry']
directorinfo.columns = ['vertex','industry']
a2i = pd.concat([companyinfo,directorinfo])
a2i.set_index('vertex', inplace = True) # all vertex to country


# # Add country columns to maindf

# In[10]:


maindfwithfirstnodeind = maindf.join(
    a2i,
    on = 'Node1'
)
maindfwithfirstnodeind.columns = ['Node1', 'Node2', 'Weight','Node1ind']

maindfwithbothnodeind = maindfwithfirstnodeind.join(
    a2i,
    on = 'Node2'
)
maindfwithbothnodeind.columns = ['Node1', 'Node2', 'Weight','Node1ind','Node2ind']


# In[11]:





# In[30]:


dropcolumn = ~((maindfwithbothnodeind.Node1ind == 3) | (
                maindfwithbothnodeind.Node1ind == 11) | (
                maindfwithbothnodeind.Node1ind == 12) | (
                maindfwithbothnodeind.Node2ind == 3) | (
                maindfwithbothnodeind.Node2ind == 11) | (
                maindfwithbothnodeind.Node2ind == 12) )


# In[35]:


maindfwithbothnodeind[dropcolumn].to_pickle('3relwithindustry.pkl')


# In[31]:


dropcolumn[dropcolumn==False]


# ####
# def industryDecider(row):
#     if row['Node1ind'] in ['NOTU', 'NONC', 'NODT'] or (row['Node2ind'] in ['NOTU', 'NONC', 'NODT']):
#         return 'DROP'
#         #bad data for the companies whose industry is unknown
#         
#     elif row['Node2ind'] == 'HUMN':
#         return row['Node1ind'] 
#         # if the second node is human, accept the relationship and classify it according to the company 
#         
#     elif row['Node2ind'] == row['Node1ind']:
#         return row['Node1ind']
#         # if the second node is NOT human, check whether the companies are in the same industry, 
#         # if same, return one of them
#     else:
#         return 'DROP'
#         # companies are in different industries




maindfwithbothnodeind['relationindustry'] = maindfwithbothnodeind.apply (lambda row: industryDecider(row),axis=1)
sameindustryrelationship = maindfwithbothnodeind[maindfwithbothnodeind['relationindustry']!='DROP']





maindfwithbothnodeind


# # Reform the dataframe to a list of dataframes, each dataframe represents a country




df4split = sameindustryrelationship[['Node1', 'Node2', 'Weight','relationindustry']]





df4split





loi = []
for industry in np.unique(df4split.relationindustry):
    loi.append(df4split[df4split.relationindustry == industry])





for df in loc:
    print (df.iloc[0,3])





loc[10]





import pickle
pickle.dump(loi, open( "loi.data", "wb" ) )





retail =  df4split[df4split.relationindustry == 'RETL']





retail





retail.to_pickle('RETL.pkl')





def extract (df,industrycode):
    dfforprocess = df[df.relationindustry == industrycode]

    namedict = pd.DataFrame(
                    np.unique(
                        pd.concat(
                            [dfforprocess.Node1,
                             dfforprocess.Node2])))
    namedict['code'] = range(len(namedict))
    namedict.columns = ['nodename','nodecode']
    namedict.set_index('nodename', inplace = True)
    
    dftemp1 = dfforprocess.join(
                namedict,
                on = 'Node1')
    dftemp1.columns  =['Node1', 'Node2', 'Weight', 'relationindustry','node1']

    dftemp2 = dftemp1.join(
                namedict,
                on = 'Node2')
    
    dftemp2.columns  =['Node1', 'Node2', 'Weight', 'relationindustry','node1','node2']
    returningdf = dftemp2 [['node1','node2','Weight']]


    return returningdf, namedict





retlfinal, retldict = extract(df4split, "RETL")    





retlfinal.to_csv("retl.csv",index = False, header = None)

