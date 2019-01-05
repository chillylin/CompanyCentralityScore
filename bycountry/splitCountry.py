
# coding: utf-8




import re
import pandas as pd
import numpy as np


# # read relationship file




maindf = pd.read_hdf(r'C:\Users\Chilly Lin\Documents\coding\RA-Combine\NetworkBuilding\3rel.h5', 'df')


# #### Change the columns value of maindf to single layer




maindf.columns = ['Node1', 'Node2', 'Weight']


# # Read Director/Company info




companyinfo = pd.read_csv(r'C:\Users\Chilly Lin\Documents\coding\RA-Combine\BvD\imported\companybasicinfo.csv',
                             )[['mk','countrycode']]
companyinfo['Ccode'] = 'C' + companyinfo.iloc[:,0].map(str) # add 'C' before company mark number
companyinfo.drop('mk',inplace = True, axis = 1) # drop company mark number
companyinfo.columns = ['ComCtyCode','ComCode'] # change columns' names.





directorinfo = pd.read_csv(r'C:\Users\Chilly Lin\Documents\coding\RA-Combine\BvD\imported\directorpersonalinfo.csv'
                             )[['dmccode','dmccountrycode']]
directorinfo['DirectorCode'] = 'D' + directorinfo.iloc[:,0].map(str)
directorinfo.drop('dmccode',inplace = True, axis = 1) # drop company mark number


# # Read country code and remove country code with country ISO code

# ### Read country code




dictDirectorCountry = pd.read_csv(r'C:\Users\Chilly Lin\Documents\coding\RA-Combine\dividedbycountry\dictDMCcountrycode.csv'
                             )[['dmccountrycode','countrycode']]
dictCompanyCountry = pd.read_csv(r'C:\Users\Chilly Lin\Documents\coding\RA-Combine\BvD\imported\countrydict.csv'
                             )[['countrycode','index']]





dictDirectorCountry


# ### Replace country code 




c2cty = companyinfo.join(
    dictCompanyCountry.set_index('countrycode'),
    on = 'ComCtyCode'
).drop('ComCtyCode',axis = 1)





d2cty = directorinfo.join(
    dictDirectorCountry.set_index('dmccountrycode'),
    on = 'dmccountrycode'
).drop('dmccountrycode', axis = 1)





d2cty.columns = ['vertex','cty']
c2cty.columns = ['vertex','cty']





a2cty = pd.concat([d2cty,c2cty])





a2cty.set_index('vertex', inplace = True) # all vertex to country





d2cty.dropna().to_pickle("d2cty.pkl")





c2cty.dropna().to_pickle("c2cty.pkl")





a2cty.dropna()


# # Add country columns to maindf




maindfwithfirstnodecty = maindf.join(
    a2cty,
    on = 'Node1'
)





maindfwithfirstnodecty.columns = ['Node1', 'Node2', 'Weight','Node1Cty']





maindfwithbothnodecty = maindfwithfirstnodecty.join(
    a2cty,
    on = 'Node2'
)





maindfwithbothnodecty.columns = ['Node1', 'Node2', 'Weight','Node1Cty','Node2Cty']





maindfwithbothnodecty





maindfwithbothnodecty.dropna().to_pickle('3relwithcountry.pkl')





maindfwithbothnodecty['samecountry'] = maindfwithbothnodecty.Node1Cty == maindfwithbothnodecty.Node2Cty





sameCountryRelationship = maindfwithbothnodecty[maindfwithbothnodecty.samecountry].copy()





sameCountryRelationship





t = sameCountryRelationship.Node1.copy()





t = t.append(sameCountryRelationship.Node2)


# # Reform the dataframe to a list of dataframes, each dataframe represents a country




loc = []
for country in np.unique(sameCountryRelationship.Node1Cty):
    loc.append(sameCountryRelationship[sameCountryRelationship.Node1Cty == country])





import pickle
pickle.dump(loc, open( "loc.pkl", "wb" ) )

