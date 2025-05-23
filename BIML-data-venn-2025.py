## A script to create venn diagrams BIML dataset using pandas and matplotlib
## Orginally run in python 3.12.6
## written by ZM Portman

import pandas as pd
pd.set_option('display.max_columns', None)  
import csv


#in here, we find the degree of overlap between the 3 datasets, but key point is AFTER filtering
#thank you to stack overflow: https://stackoverflow.com/questions/72919747/efficient-way-of-getting-unique-values-by-comparing-columns-in-two-dataframes-pa

#all of the bee genera from the US and Canada to filter the datos data, as it has a lot of non-bees
bee_genera = ['Agapanthinus', 'Agapostemon', 'Ancylandrena', 'Ancyloscelis', 'Andrena', 'Anthemurgus', 'Anthidiellum', 'Anthidium', 'Anthophora', 'Anthophorula', 'Apis', 'Ashmeadiella', 'Atoposmia', 'Augochlora', 'Augochlorella', 'Augochloropsis', 'Bombus', 'Brachymelecta', 'Brachynomada', 'Calliopsis', 'Caupolicana', 'Cemolobus', 'Centris', 'Ceratina', 'Chelostoma', 'Chilicola', 'Coelioxys', 'Colletes', 'Conanthalictus', 'Diadasia', 'Dianthidium', 'Dieunomia', 'Dioxys', 'Dufourea', 'Epeoloides', 'Epeolus', 'Ericrocis', 'Eucera', 'Euglossa', 'Eulaema', 'Eulonchopria', 'Exomalopsis', 'Florilegus', 'Gaesischia', 'Habropoda', 'Halictus', 'Heriades', 'Hesperapis', 'Hexepeolus', 'Holcopasites', 'Hoplitis', 'Hylaeus', 'Lasioglossum', 'Leiopodus', 'Lithurgopsis', 'Lithurgus', 'Macropis', 'Macrotera', 'Martinapis', 'Megachile', 'Megandrena', 'Melecta', 'Melissodes', 'Melissoptila', 'Melitoma', 'Melitta', 'Mesoplia', 'Mesoxaea', 'Mexalictus', 'Micralictoides', 'Neolarra', 'Neopasites', 'Nomada', 'Nomia', 'Odyneropsis', 'Oreopasites', 'Osmia', 'Panurginus', 'Paranomada', 'Paranthidium', 'Peponapis', 'Perdita', 'Protandrena', 'Protodufourea', 'Protosmia', 'Protoxaea', 'Pseudaugochlora', 'Pseudoanthidium', 'Pseudopanurgus', 'Ptiloglossa', 'Ptilothrix', 'Rhopalolemma', 'Simanthedon', 'Sphecodes', 'Sphecodosoma', 'Stelis', 'Svastra', 'Syntrichalonia', 'Temnosoma', 'Tetraloniella', 'Townsendiella', 'Trachusa', 'Triepeolus', 'Triopasites', 'Xenoglossa', 'Xeralictus', 'Xeroheriades', 'Xeromelecta', 'Xylocopa', 'Zacosmia', 'Zikanapis']



#get mid atlantic bees dataset. no filtering needed.
midatl = pd.read_csv("data/1OccurrenceLevel_AllBees.csv", sep=',', on_bad_lines='skip', index_col=False, dtype='unicode')
print(midatl.head())


#get anthropogenic bees dataset and filter

anthro = pd.read_csv("data/Datos1.csv", sep=',', on_bad_lines='skip', index_col=False, dtype='unicode')

#filter out everything that isn't in a bee genus  
anthro = anthro[anthro['Genus'].isin(bee_genera)] 
print(anthro.head())

#convert years to numeric and assign to a new column
anthro['year_numbers'] = pd.to_numeric(anthro['year1'], errors = 'coerce')
anthro.rename(columns={"gen_sp":"name"}, inplace=True)

#filtering out all years lower than 2001 because they are messing up my graphs and there are like 10 records
anthro = anthro[anthro['year_numbers'] > 2000] 




#compare mid atlantic and anthropogenic bees
print ("Number of Mid-Atlantic bees:", len(midatl.index))

print ("Number of Anthropogenic bees records after filtering (checked and good):", len(anthro.index))


in_anthro_not_midatl = anthro.loc[~anthro['IDs'].isin(midatl['identifier']), 'IDs'].unique()

print (in_anthro_not_midatl, len(in_anthro_not_midatl), "number in athro but not in mid atlantic")

in_anthro_and_midatl = anthro.loc[anthro['IDs'].isin(midatl['identifier']), 'IDs'].unique()

print (in_anthro_and_midatl, len(in_anthro_and_midatl), "number in athro AND mid atlantic")



midatl_not_anthro = midatl.loc[~midatl['identifier'].isin(anthro['IDs']), 'identifier'].unique()

print (midatl_not_anthro, len(midatl_not_anthro), "number in mid-atlantic but not in anthro")

#so just remove tilde to find true overlap 
trying = midatl.loc[midatl['identifier'].isin(anthro['IDs']), 'identifier'].unique()

print (trying, len(trying), "number in both mid-atlantic and anthro")



#now do BIML

#here is the simple gbif download, which is avaiable at https://doi.org/10.15468/dl.7kz274
#allbees = pd.read_csv("data/0011366-231120084113126_simple.csv", sep='\t', on_bad_lines='skip', index_col=False, dtype='unicode') #this is the 2023 new data #old
allbees = pd.read_csv("0001402-250221090833381-simple/0001402-250221090833381.csv", sep='\t', on_bad_lines='skip', index_col=False, dtype='unicode') #this is the 2023 new data #old



print ("file successfully read in!")
print ("GBIF dataset")

print ("Number of BIML GBIF raw records in dataset:", len(allbees.index))

#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year'], errors = 'coerce')

#filtering out anything that isn't in a bee family:
allbees = allbees[allbees['family'].isin(['Apidae', 'Andrenidae', 'Colletidae', 'Halictidae', 'Megachilidae', 'Melittidae'])] 

#Use only records from the US
allbees = allbees[allbees['countryCode'] == "US"] #Why the hell did this change??!?!?!

#filtering out all years lower than 2001 because there are very few and they are messing up my graphs
excluded = allbees[allbees['year_numbers'] < 2001] # want to count the number of excluded records
print ("Number of excluded pre 2001 BIML GBIF records:", len(excluded.index))
allbees = allbees[allbees['year_numbers'] > 2000] 

#filtering out all years over 2018 cuz there are only 47 -- updating to all years over 2022 with new dataset...
excluded = allbees[allbees['year_numbers'] > 2022] # want to count the number of excluded records
print ("Number of excluded post 2022 BIML GBIF records:", len(excluded.index))
allbees = allbees[allbees['year_numbers'] < 2023] 


###print ("CERATINA CALCARATA FEMALE GBIF:", pre_post_2010_female(allbees, "Ceratina calcarata", "FEMALE"))


print(allbees.head())
print ("Number of BIML GBIF records remaining after filtering:", len(allbees.index))

in_GBIF_not_midatl = allbees.loc[~allbees['catalogNumber'].isin(midatl['identifier']), 'catalogNumber'].unique()

print (in_GBIF_not_midatl, len(in_GBIF_not_midatl), "number in GBIF but not in mid atlantic")

in_GBIF_and_midatl = allbees.loc[allbees['catalogNumber'].isin(midatl['identifier']), 'catalogNumber'].unique()

print (in_GBIF_and_midatl, len(in_GBIF_and_midatl), "number in GBIF AND in mid atlantic")

in_midatl_not_GBIF = midatl.loc[~midatl['identifier'].isin(allbees['catalogNumber']), 'identifier'].unique()

print (in_midatl_not_GBIF, len(in_midatl_not_GBIF), "number in mid-atlantic but not in GBIF")


#compare anthro + GBIF
in_anthro_not_GBIF = anthro.loc[~anthro['IDs'].isin(allbees['catalogNumber']), 'IDs'].unique()

print (in_anthro_not_GBIF, len(in_anthro_not_GBIF), "number in athro but not in GBIF")

in_anthro_and_GBIF = anthro.loc[anthro['IDs'].isin(allbees['catalogNumber']), 'IDs'].unique()

print (in_anthro_and_GBIF, len(in_anthro_and_GBIF), "number in athro AND GBIF")


#last need to find shared accross all 3, you already  have in_anthro_and_GBIF, in_GBIF_and_midatl, and in_anthro_and_midatl

shared = set(in_anthro_and_GBIF) & set(in_GBIF_and_midatl) & set(in_anthro_and_midatl)

print(len(shared), "shared accross all 3 datasets")

#total = shared | set(in_anthro_and_GBIF) | set(in_anthro_not_GBIF) | set(in_midatl_not_GBIF) | set(in_midatl_and_GBIF) | set(in_GBIF_not_midatl)

#print(len(total), "total accross all 3 datasets, incomplete though since no GBIF-not-anthro")

#also calculate number shared by mid-atlantic and Anthro but not in GBIF

#mid_anthro_shared_unique = set(in_midatl_not_GBIF) & set(in_anthro_not_GBIF)
mid_anthro_shared_unique = list(set(in_midatl_not_GBIF).intersection(set(in_anthro_not_GBIF)))
print (len(mid_anthro_shared_unique), "number shared by mid atlantic and anthro but not in GBIF")

#need to do: unique to each one
unique_midatle = list(set(in_midatl_not_GBIF).intersection(set(midatl_not_anthro)))
print (len(unique_midatle), "Unique to mid atl")


print("all done")


#now graph
#now graph
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn import venn3_unweighted 

set1 = set(['A', 'B', 'C'])
set1 = set(anthro['IDs'])


set2 = set(['A', 'B', 'D'])
set2 = set(midatl['identifier'])


set3 = set(['A', 'E', 'F'])
set3 = set(allbees['catalogNumber'])


plt.figure(figsize=(15,15))

#venn3([set1, set2, set3], ('Anthropogenic', 'Mid-Atlantic', 'GBIF'))

#venn3_unweighted([set1, set2, set3], ('Anthropogenic', 'Mid-Atlantic', 'GBIF'))
venn3_unweighted([set1, set2, set3], 
                 set_labels=('Anthropogenic' + '\n' + str(len(anthro.index)) + '       ', 'Mid-Atlantic'+ '\n     ' + str(len(midatl.index)), 'BIML GBIF' + '\n' + str(len(allbees.index))       ),
                 subset_areas = (0.5,0.5,1,8,4,3,3))
                 #set_colors = ("indigo", "blue", "#6C000F"))
venn3_circles((0.5,0.5,1,8,4,3,3)) #ad outlines


#first is antho unique, should be 1
#second is mid-atlantic unique, should be 2
#third is antrho-midoverlap, should be 1
#fourth is GBIF standalong, should be 10
#fifth is anthro gbif overlap, try 3

#seventh is all overlap
plt.savefig('test.png', dpi=300)

plt.show()



"""
from BioVenn import *

biovenn = draw_venn(list(set1), list(set2), list(set3), xtitle="Anthropogenic", ytitle="Mid-Atlantic", ztitle="GBIF", title="", subtitle="", nrtype="abs", output="svg")

from venn import venn
plt.figure(figsize=(10,10))


venn({"Anthropogenic":set1,"Mid-Atlantic":set2,"GBIF":set3},cmap=["red","green","blue"])
plt.show()

"""
