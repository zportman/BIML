## A script to create figures of the BIML dataset using pandas and matplotlib
## Orginally run in python 3.10
## written by ZM Portman

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)  
import csv


def count_by_year(allbees, year1, year2, species_name):
    ###Given a start year, end year (inclusive), and species name, return a table of the counts of that bee per year    
    
    #step 1: get all the records of a given bee
    species = allbees[allbees['name'] == species_name]
    
    #step 2: get the index of counts
    species_summary = species['year_numbers'].value_counts()
    
    #step 3: fill in the zero years
    year_list = list(range(year1, year2+1))
    for year in year_list:
        if year not in species_summary:
            species_summary.loc[year] = 0    
            
    #sort the year summary
    species_summary = species_summary.sort_index()
    
    return species_summary

#graph colors: stats dataset is 'rebeccapurple', GBIF is brown, and mid atlantic dataset is #1f77b4


#remove top and right borders for all plots
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False

#all of the bee genera from the US and Canada to filter the datos data, as it has a lot of non-bees
bee_genera = ['Agapanthinus', 'Agapostemon', 'Ancylandrena', 'Ancyloscelis', 'Andrena', 'Anthemurgus', 'Anthidiellum', 'Anthidium', 'Anthophora', 'Anthophorula', 'Apis', 'Ashmeadiella', 'Atoposmia', 'Augochlora', 'Augochlorella', 'Augochloropsis', 'Bombus', 'Brachymelecta', 'Brachynomada', 'Calliopsis', 'Caupolicana', 'Cemolobus', 'Centris', 'Ceratina', 'Chelostoma', 'Chilicola', 'Coelioxys', 'Colletes', 'Conanthalictus', 'Diadasia', 'Dianthidium', 'Dieunomia', 'Dioxys', 'Dufourea', 'Epeoloides', 'Epeolus', 'Ericrocis', 'Eucera', 'Euglossa', 'Eulaema', 'Eulonchopria', 'Exomalopsis', 'Florilegus', 'Gaesischia', 'Habropoda', 'Halictus', 'Heriades', 'Hesperapis', 'Hexepeolus', 'Holcopasites', 'Hoplitis', 'Hylaeus', 'Lasioglossum', 'Leiopodus', 'Lithurgopsis', 'Lithurgus', 'Macropis', 'Macrotera', 'Martinapis', 'Megachile', 'Megandrena', 'Melecta', 'Melissodes', 'Melissoptila', 'Melitoma', 'Melitta', 'Mesoplia', 'Mesoxaea', 'Mexalictus', 'Micralictoides', 'Neolarra', 'Neopasites', 'Nomada', 'Nomia', 'Odyneropsis', 'Oreopasites', 'Osmia', 'Panurginus', 'Paranomada', 'Paranthidium', 'Peponapis', 'Perdita', 'Protandrena', 'Protodufourea', 'Protosmia', 'Protoxaea', 'Pseudaugochlora', 'Pseudoanthidium', 'Pseudopanurgus', 'Ptiloglossa', 'Ptilothrix', 'Rhopalolemma', 'Simanthedon', 'Sphecodes', 'Sphecodosoma', 'Stelis', 'Svastra', 'Syntrichalonia', 'Temnosoma', 'Tetraloniella', 'Townsendiella', 'Trachusa', 'Triepeolus', 'Triopasites', 'Xenoglossa', 'Xeralictus', 'Xeroheriades', 'Xeromelecta', 'Xylocopa', 'Zacosmia', 'Zikanapis']



#Read in midatlantic bees dataset

print ("code is running! beep boop")
#Read in data ===== this is the Kammerer et al. (2020) dataset. Available from https://doi.org/10.6084/m9.figshare.c.4728725.v1
allbees = pd.read_csv("1OccurrenceLevel_AllBees.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
print ("file successfully read in!")
#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year'], errors = 'coerce')



Ag_virescens = count_by_year(allbees, 2002, 2016, "Agapostemon virescens") #This is for mid atlantic dataset
La_coreopsis = count_by_year(allbees, 2002, 2016, "Lasioglossum coreopsis") #This is for mid atlantic dataset
Au_aurata = count_by_year(allbees, 2002, 2016, "Augochlorella aurata") #This is for mid atlantic dataset

C_calcarata_atlantic = count_by_year(allbees, 2002, 2016, "Ceratina calcarata") #This is for mid atlantic dataset
C_dupla_atlantic = count_by_year(allbees, 2002, 2016, "Ceratina dupla") #This is for mid atlantic dataset
C_mikmaqi_atlantic = count_by_year(allbees, 2002, 2016, "Ceratina mikmaqi") #This is for mid atlantic dataset



#set up baseline figure 0

fig0, ax0 = plt.subplots(nrows=3, ncols=3, figsize=(11, 8))
fig0.tight_layout(pad=1)

#add atl bees to zero
atl_bees_per_year = allbees['year_numbers'].value_counts()
ax0[0,0].bar(atl_bees_per_year.index, atl_bees_per_year.tolist(), color='#1f77b4')
ax0[0,0].set_xticks(list(range(2002, 2017)))
ax0[0,0].tick_params(axis='x', labelrotation=45)
ax0[0,0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor')
ax0[0,0].set_ylabel('# Records', fontsize=13)
ax0[0,0].set_title('All Mid-Atlantic bees', y=1, pad = 2)

#add viresens to zero
ax0[1,0].set_xticks(list(range(2002, 2017)))
ax0[1,0].tick_params(axis='x', labelrotation=45)
ax0[1,0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor')
ax0[1,0].set_ylabel('# Records', fontsize=13)
ax0[1,0].set_title('Mid-Atlantic Ag. virescens', y=1, pad = 2)
ax0[1,0].bar(Ag_virescens.index, Ag_virescens.tolist(), color='#1f77b4')

#add coreopsis to zero
ax0[2,0].set_xticks(list(range(2002, 2017)))
ax0[2,0].tick_params(axis='x', labelrotation=45)
ax0[2,0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor')
ax0[2,0].set_ylabel('# Records', fontsize=13)
ax0[2,0].set_title('Mid-Atlantic L. coreopsis', y=1, pad = 2)
ax0[2,0].bar(La_coreopsis.index, La_coreopsis.tolist(), color='#1f77b4')


#Second figure, for Ceratina
fig1, ax1 = plt.subplots(nrows=3, ncols=2, figsize=(7.5, 8))
fig1.tight_layout(pad=1)

#ax[0].set_xticks(ax[0].get_xticks())

ax1[0,0].set_xticks(list(range(2002, 2017)))
ax1[0,0].tick_params(axis='x', labelrotation=45)
ax1[0,0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor')
ax1[0,0].set_ylabel('# Records', fontsize=13)
ax1[0,0].set_title('Mid-Atlantic C. calcarata', y=1, pad = 2)
ax1[0,0].bar(C_calcarata_atlantic.index, C_calcarata_atlantic.tolist(), color='#1f77b4')

ax1[1,0].set_xticks(list(range(2002, 2017)))
ax1[1,0].tick_params(axis='x', labelrotation=45)
ax1[1,0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor')
ax1[1,0].set_ylabel('# Records', fontsize=13)
ax1[1,0].set_title('Mid-Atlantic C. dupla', y=1, pad=-2)
ax1[1,0].bar(C_dupla_atlantic.index, C_dupla_atlantic.tolist(), color='#1f77b4')

ax1[2,0].set_xticks(list(range(2002, 2017)))
ax1[2,0].tick_params(axis='x', labelrotation=45)
ax1[2,0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor')
ax1[2,0].set_ylabel('# Records', fontsize=13)
ax1[2,0].set_title('Mid-Atlantic C. mikmaqi', y=1, pad=-2)
ax1[2,0].bar(C_mikmaqi_atlantic.index, C_mikmaqi_atlantic.tolist(), color='#1f77b4')


fig1.tight_layout(pad=1)
###plt.show()


#plt.bar(results.index, results.tolist(), width= 0.8, color='#1f77b4') # 



#Now we do figure 3
fig2, ax2 = plt.subplots(nrows=5, ncols=3, figsize=(12, 11))
fig2.tight_layout(pad=1)


#also will load up figure 4 at the same time -- this is the substantial change bees
fig3, ax3 = plt.subplots(nrows=4, ncols=3, figsize=(11, 9))
fig3.tight_layout(pad=1)


#first do mid-atlantic bees dataset and load in first column

atl_ephialtum = count_by_year(allbees, 2002, 2016, "Lasioglossum ephialtum") #This is for mid atlantic dataset
atl_gotham = count_by_year(allbees, 2002, 2016, "Lasioglossum gotham") #This is for mid atlantic dataset
atl_trigeminum = count_by_year(allbees, 2002, 2016, "Lasioglossum trigeminum") #This is for mid atlantic dataset
atl_floridanum = count_by_year(allbees, 2002, 2016, "Lasioglossum floridanum") #This is for mid atlantic dataset
atl_leucocomum = count_by_year(allbees, 2002, 2016, "Lasioglossum leucocomum") #This is for mid atlantic dataset

atl_abanci = count_by_year(allbees, 2002, 2016, "Lasioglossum abanci") #This is for mid atlantic dataset
atl_admirandum = count_by_year(allbees, 2002, 2016, "Lasioglossum admirandum") #This is for mid atlantic dataset
atl_oblongum = count_by_year(allbees, 2002, 2016, "Lasioglossum oblongum") #This is for mid atlantic dataset
atl_versatum = count_by_year(allbees, 2002, 2016, "Lasioglossum versatum") #This is for mid atlantic dataset

    
ax2[0, 0].set_xticks(list(range(2002, 2017)))
ax2[0, 0].tick_params(axis='x', labelrotation=45)
ax2[0, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[0, 0].set_ylabel('# Records', fontsize=13)
ax2[0, 0].set_title('L. ephialtum - Mid-Atlantic bees', y=1, pad = 2)
ax2[0, 0].bar(atl_ephialtum.index, atl_ephialtum.tolist(), color='#1f77b4')

ax2[1, 0].set_xticks(list(range(2002, 2017)))
ax2[1, 0].tick_params(axis='x', labelrotation=45)
ax2[1, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[1, 0].set_ylabel('# Records', fontsize=13)
ax2[1, 0].set_title('L. gotham - Mid-Atlantic bees', y=1, pad = 2)
ax2[1, 0].bar(atl_gotham.index, atl_gotham.tolist(), color='#1f77b4')

ax2[2, 0].set_xticks(list(range(2002, 2017)))
ax2[2, 0].tick_params(axis='x', labelrotation=45)
ax2[2, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[2, 0].set_ylabel('# Records', fontsize=13)
ax2[2, 0].set_title('L. trigeminum - Mid-Atlantic bees', y=1, pad = 2)
ax2[2, 0].bar(atl_trigeminum.index, atl_trigeminum.tolist(), color='#1f77b4')

ax2[3, 0].set_xticks(list(range(2002, 2017)))
ax2[3, 0].tick_params(axis='x', labelrotation=45)
ax2[3, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[3, 0].set_ylabel('# Records', fontsize=13)
ax2[3, 0].yaxis.get_major_locator().set_params(integer=True) #get rid of decimal y axis values
ax2[3, 0].set_title('L. floridanum - Mid-Atlantic bees', y=1, pad = 2)
ax2[3, 0].bar(atl_floridanum.index, atl_floridanum.tolist(), color='#1f77b4')

ax2[4, 0].set_xticks(list(range(2002, 2017)))
ax2[4, 0].tick_params(axis='x', labelrotation=45)
ax2[4, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[4, 0].set_ylabel('# Records', fontsize=13)
ax2[4, 0].set_title('L. leucocomum - Mid-Atlantic bees', y=1, pad = 2)
ax2[4, 0].bar(atl_leucocomum.index, atl_leucocomum.tolist(), color='#1f77b4')

#Lasioglossum species that were often misidentified
ax3[0, 0].set_xticks(list(range(2002, 2017)))
ax3[0, 0].tick_params(axis='x', labelrotation=45)
ax3[0, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[0, 0].set_ylabel('# Records', fontsize=13)
ax3[0, 0].set_title('L. abanci - Mid-Atlantic bees', y=1, pad = 2)
ax3[0, 0].bar(atl_abanci.index, atl_abanci.tolist(), color='#1f77b4')

ax3[1, 0].set_xticks(list(range(2002, 2017)))
ax3[1, 0].tick_params(axis='x', labelrotation=45)
ax3[1, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[1, 0].set_ylabel('# Records', fontsize=13)
ax3[1, 0].set_title('L. admirandum - Mid-Atlantic bees', y=1, pad = 2)
ax3[1, 0].bar(atl_admirandum.index, atl_admirandum.tolist(), color='#1f77b4')

ax3[2, 0].set_xticks(list(range(2002, 2017)))
ax3[2, 0].tick_params(axis='x', labelrotation=45)
ax3[2, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[2, 0].set_ylabel('# Records', fontsize=13)
ax3[2, 0].set_title('L. oblongum - Mid-Atlantic bees', y=1, pad = 2)
ax3[2, 0].bar(atl_oblongum.index, atl_oblongum.tolist(), color='#1f77b4')

ax3[3, 0].set_xticks(list(range(2002, 2017)))
ax3[3, 0].tick_params(axis='x', labelrotation=45)
ax3[3, 0].set_xticklabels([2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[3, 0].set_ylabel('# Records', fontsize=13)
ax3[3, 0].set_title('L. versatum - Mid-Atlantic bees', y=1, pad = 2)
ax3[3, 0].bar(atl_versatum.index, atl_versatum.tolist(), color='#1f77b4')



#ok now we move onto the anthropogenic bees dataset, downloaded from: https://datadryad.org/stash/dataset/doi:10.5061%2Fdryad.8md5419
allbees = pd.read_csv("Datos1-2.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
print ("file successfully read in!")

print ("Total number of records in the dataset:", len(allbees))

#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year1'], errors = 'coerce')
allbees.rename(columns={"gen_sp":"name"}, inplace=True)

#filter out everything that isn't in a bee genus
allbees = allbees[allbees['Genus'].isin(bee_genera)] 

#filtering out all years lower than 2001 because they are messing up my graphs and there are like 10 records
allbees = allbees[allbees['year_numbers'] > 2000] 

# Common newly described species
anthro_ephialtum = count_by_year(allbees, 2001, 2015, "Lasioglossum ephialtum") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_gotham = count_by_year(allbees, 2001, 2015, "Lasioglossum gotham") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_trigeminum = count_by_year(allbees, 2001, 2015, "Lasioglossum trigeminum") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_floridanum = count_by_year(allbees, 2001, 2015, "Lasioglossum floridanum") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_leucocomum = count_by_year(allbees, 2001, 2015, "Lasioglossum leucocomum") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out

# The "oftenn misidentified" Lasioglossum species
anthro_abanci = count_by_year(allbees, 2001, 2015, "Lasioglossum abanci") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_admirandum = count_by_year(allbees, 2001, 2015, "Lasioglossum near_admirandum") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_oblongum = count_by_year(allbees, 2001, 2015, "Lasioglossum oblongum") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_versatum = count_by_year(allbees, 2001, 2015, "Lasioglossum versatum") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out

# Consistent taxonomy species for figure 1
anthro_virescens = count_by_year(allbees, 2001, 2015, "Agapostemon virescens") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_aurata = count_by_year(allbees, 2001, 2015, "Augochlorella aurata") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out
anthro_coreopsis = count_by_year(allbees, 2001, 2015, "Lasioglossum coreopsis") #This is range for anthropogenic bees -- though it does have some 1999 records that we will have already filtered out



#add Anthropogenic bees to zero (Figure 1)
anthro_bees_per_year = allbees['year_numbers'].value_counts()
ax0[0,1].bar(anthro_bees_per_year.index, anthro_bees_per_year.tolist(), color='rebeccapurple')
ax0[0,1].set_xticks(list(range(2001, 2016)))
ax0[0,1].tick_params(axis='x', labelrotation=45)
#ax0[0,1].set_xticklabels([2001,'', 2003,'', 2005,'', 2007,'', 2009,'', 2011,'', 2013,'', 2015], ha='right', minor=False, rotation_mode='anchor')
ax0[0,1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor')
ax0[0,1].set_title('All Anthropogenic bees', y=1, pad = 2)

#add viresens to zero (Figure 1)
ax0[1,1].set_xticks(list(range(2001, 2016)))
ax0[1,1].tick_params(axis='x', labelrotation=45)
ax0[1,1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor')
ax0[1,1].set_title('Anthropogenic Ag. virescens', y=1, pad = 2)
ax0[1,1].bar(anthro_virescens.index, anthro_virescens.tolist(), color='rebeccapurple')

#add coreopsis to zero (Figure 1)
ax0[2,1].set_xticks(list(range(2001, 2016)))
ax0[2,1].tick_params(axis='x', labelrotation=45)
ax0[2,1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor')
ax0[2,1].set_title('Anthropogenic L. coreopsis', y=1, pad = 2)
ax0[2,1].bar(anthro_coreopsis.index, anthro_coreopsis.tolist(), color='rebeccapurple')


# adding to newly described species figure 
ax2[0, 1].set_xticks(list(range(2001, 2016)))
ax2[0, 1].tick_params(axis='x', labelrotation=45)
##ax2[0, 1].set_xticklabels(list(range(2001, 2016)), ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[0, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[0, 1].set_title('L. ephialtum - Anthropogenic bees', y=1, pad = 2)
ax2[0, 1].bar(anthro_ephialtum.index, anthro_ephialtum.tolist(), color='rebeccapurple')

ax2[1, 1].set_xticks(list(range(2001, 2016)))
ax2[1, 1].tick_params(axis='x', labelrotation=45)
ax2[1, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[1, 1].set_title('L. gotham - Anthropogenic bees', y=1, pad = 2)
ax2[1, 1].bar(anthro_gotham.index, anthro_gotham.tolist(), color='rebeccapurple')

ax2[2, 1].set_xticks(list(range(2001, 2016)))
ax2[2, 1].tick_params(axis='x', labelrotation=45)
ax2[2, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[2, 1].set_title('L. trigeminum - Anthropogenic bees', y=1, pad = 2)
ax2[2, 1].bar(anthro_trigeminum.index, anthro_trigeminum.tolist(), color='rebeccapurple')

ax2[3, 1].set_xticks(list(range(2001, 2016)))
ax2[3, 1].tick_params(axis='x', labelrotation=45)
ax2[3, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[3, 1].set_title('L. floridanum - Anthropogenic bees', y=1, pad = 2)
ax2[3, 1].bar(anthro_floridanum.index, anthro_floridanum.tolist(), color='rebeccapurple')

ax2[4, 1].set_xticks(list(range(2001, 2016)))
ax2[4, 1].tick_params(axis='x', labelrotation=45)
ax2[4, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[4, 1].set_title('L. leucocomum - Anthropogenic bees', y=1, pad = 2)
ax2[4, 1].bar(anthro_leucocomum.index, anthro_leucocomum.tolist(), color='rebeccapurple')


ax3[0, 1].set_xticks(list(range(2001, 2016)))
ax3[0, 1].tick_params(axis='x', labelrotation=45)
ax3[0, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[0, 1].set_title('L. abanci - Anthropogenic bees', y=1, pad = 2)
ax3[0, 1].bar(anthro_abanci.index, anthro_abanci.tolist(), color='rebeccapurple')

ax3[1, 1].set_xticks(list(range(2001, 2016)))
ax3[1, 1].tick_params(axis='x', labelrotation=45)
ax3[1, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[1, 1].set_title('L. nr admirandum - Anthropogenic bees', y=1, pad = 2)
ax3[1, 1].bar(anthro_admirandum.index, anthro_admirandum.tolist(), color='rebeccapurple')

ax3[2, 1].set_xticks(list(range(2001, 2016)))
ax3[2, 1].tick_params(axis='x', labelrotation=45)
ax3[2, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[2, 1].set_title('L. oblongum - Anthropogenic bees', y=1, pad = 2)
ax3[2, 1].bar(anthro_oblongum.index, anthro_oblongum.tolist(), color='rebeccapurple')

ax3[3, 1].set_xticks(list(range(2001, 2016)))
ax3[3, 1].tick_params(axis='x', labelrotation=45)
ax3[3, 1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014, ''], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[3, 1].set_title('L. versatum - Anthropogenic bees', y=1, pad = 2)
ax3[3, 1].bar(anthro_versatum.index, anthro_versatum.tolist(), color='rebeccapurple')



# Read in the GBIF dataset
print ("code is running!")
#allbees = pd.read_csv("usgs-data.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode', header = None, 
#                      names = ['num', 'code', 'web_address', 'animal', 'arthropod', 'insecta', 'order', 'family', 'genus', 'name', 'mystery', 'ID_level', 'scientific name', 'name_again',
#                               'blank','country','blank2','state', 'blank3', 'blank4', 'code2', 'lat', 'lon', 'elev_maybe', 'y', 'z', 'aa', 'ab', 'ac', 'full_date', 'day', 'month', 'year',
#                               'another_number', 'same_number_again', 'preserved_specimen', 'bison', 'inst_code',  'event_and_DRO_num', 'an', 'collector', 'ID_date',
#                               'cc', 'ar', 'identifier', 'au', 'time','geode' ])

## column headers: gbifID	datasetKey	occurrenceID	kingdom	phylum	class	order	family	genus	species	infraspecificEpithet	taxonRank	scientificName	verbatimScientificName	verbatimScientificNameAuthorship	countryCode	locality	stateProvince	occurrenceStatus	individualCount	publishingOrgKey	decimalLatitude	decimalLongitude	coordinateUncertaintyInMeters	coordinatePrecision	elevation	elevationAccuracy	depth	depthAccuracy	eventDate	day	month	year	taxonKey	speciesKey	basisOfRecord	institutionCode	collectionCode	catalogNumber	recordNumber	identifiedBy	dateIdentified	license	rightsHolder	recordedBy	typeStatus	establishmentMeans	lastInterpreted	mediaType	issue

#USGS BIML dataset from https://doi.org/10.15468/dl.2e5ugx
allbees = pd.read_csv("0086423-210914110416597.csv", sep='\t', error_bad_lines=False, index_col=False, dtype='unicode')
print ("file successfully read in!")

#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year'], errors = 'coerce')
#allbees['identifier'] = allbees['web_address'].str.replace("http://www.discoverlife.org/mp/20l?id=", "")

# changing column scientificName to name for consistency with other datasets
#allbees = allbees.rename(columns = {'scientificName': 'name'})
allbees['name']= allbees['species']

#filtering out anything that isn't in a bee family:
allbees = allbees[allbees['family'].isin(['Apidae', 'Andrenidae', 'Colletdiae', 'Halictidae', 'Megachilidae', 'Melittidae'])] 

#Use only records from the US
allbees = allbees[allbees['countryCode'] == "US"] 

#filtering out all years lower than 2001 because there are very few and they are messing up my graphs
excluded = allbees[allbees['year_numbers'] < 2001] # want to count the number of excluded records
print ("Number of excluded pre 2001 BIML GBIF records:", len(excluded.index))
allbees = allbees[allbees['year_numbers'] > 2000] 

#filtering out all years over 2018 cuz there are only 47
excluded = allbees[allbees['year_numbers'] > 2018] # want to count the number of excluded records
print ("Number of excluded post 2018 BIML GBIF records:", len(excluded.index))
allbees = allbees[allbees['year_numbers'] < 2019] 

print(allbees.head())
print ("Number of BIML GBIF records remaining after filtering:", len(allbees.index))


gbif_ephialtum = count_by_year(allbees, 2001, 2018, "Lasioglossum ephialtum") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_gotham = count_by_year(allbees, 2001, 2018, "Lasioglossum gotham") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_trigeminum = count_by_year(allbees, 2001, 2018, "Lasioglossum trigeminum") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_floridanum = count_by_year(allbees, 2001, 2018, "Lasioglossum floridanum") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_leucocomum = count_by_year(allbees, 2001, 2018, "Lasioglossum leucocomum") #This is the range for gbif dataset -- leaving out pre-2001 records because so few

print (gbif_floridanum)
species = allbees[allbees['name'] =="Lasioglossum floridanum"]
print (species)
species.to_csv('floridaum.csv')



gbif_abanci = count_by_year(allbees, 2001, 2018, "Lasioglossum abanci") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_admirandum = count_by_year(allbees, 2001, 2018, "Lasioglossum admirandum") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_oblongum = count_by_year(allbees, 2001, 2018, "Lasioglossum oblongum") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_versatum = count_by_year(allbees, 2001, 2018, "Lasioglossum versatum") #This is the range for gbif dataset -- leaving out pre-2001 records because so few

# The taxonomic consistent species for figure 1
gbif_virescens = count_by_year(allbees, 2001, 2018, "Agapostemon virescens") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_aurata = count_by_year(allbees, 2001, 2018, "Augochlorella aurata") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_coreopsis = count_by_year(allbees, 2001, 2018, "Lasioglossum coreopsis") #This is the range for gbif dataset -- leaving out pre-2001 records because so few

#Ceratina species
gbif_calcarata = count_by_year(allbees, 2001, 2018, "Ceratina calcarata") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_dupla = count_by_year(allbees, 2001, 2018, "Ceratina dupla") #This is the range for gbif dataset -- leaving out pre-2001 records because so few
gbif_mikmaqi = count_by_year(allbees, 2001, 2018, "Ceratina mikmaqi") #This is the range for gbif dataset -- leaving out pre-2001 records because so few



#add gbif bees to zero (Figure 1)
gbif_bees_per_year = allbees['year_numbers'].value_counts()
print ("GBIF BEES PER YEAR", gbif_bees_per_year)
ax0[0,2].bar(gbif_bees_per_year.index, gbif_bees_per_year.tolist(), color='brown')
ax0[0,2].set_xticks(list(range(2001, 2019)))
ax0[0,2].tick_params(axis='x', labelrotation=45)
ax0[0,2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor')
ax0[0,2].set_title('All BIML GBIF bees', y=1, pad = 2)

#add virescens to zero (Figure 1)
ax0[1,2].set_xticks(list(range(2001, 2019)))
ax0[1,2].tick_params(axis='x', labelrotation=45)
ax0[1,2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor')
ax0[1,2].set_title('BIML GBIF Ag. virescens', y=1, pad = 2)
ax0[1,2].bar(gbif_virescens.index, gbif_virescens.tolist(), color='brown')

#add coreopsis to zero (Figure 1)
ax0[2,2].set_xticks(list(range(2001, 2019)))
ax0[2,2].tick_params(axis='x', labelrotation=45)
ax0[2,2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor')
ax0[2,2].set_title('BIML GBIF L. coreopsis', y=1, pad = 2)
ax0[2,2].bar(gbif_coreopsis.index, gbif_coreopsis.tolist(), color='brown')


#add C. calcarata to Figure 2
ax1[0,1].set_xticks(list(range(2001, 2019)))
ax1[0,1].tick_params(axis='x', labelrotation=45)
ax1[0,1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor')
ax1[0,1].set_title('BIML GBIF C. calcarata', y=1, pad = 2)
ax1[0,1].bar(gbif_calcarata.index, gbif_calcarata.tolist(), color='brown')

#add C. dupla to Figure 2
ax1[1,1].set_xticks(list(range(2001, 2019)))
ax1[1,1].tick_params(axis='x', labelrotation=45)
ax1[1,1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor')
ax1[1,1].set_title('BIML GBIF C. dupla', y=1, pad = 2)
ax1[1,1].bar(gbif_dupla.index, gbif_dupla.tolist(), color='brown')

#add C. mikmaqi to Figure 2
ax1[2,1].set_xticks(list(range(2001, 2019)))
ax1[2,1].tick_params(axis='x', labelrotation=45)
ax1[2,1].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor')
ax1[2,1].set_title('BIML GBIF C. mikmaqi', y=1, pad = 2)
ax1[2,1].bar(gbif_mikmaqi.index, gbif_mikmaqi.tolist(), color='brown')



ax2[0, 2].set_xticks(list(range(2001, 2019)))
ax2[0, 2].tick_params(axis='x', labelrotation=45)
ax2[0, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[0, 2].set_title('L. ephialtum - BIML GBIF', y=1, pad = 2)
ax2[0, 2].bar(gbif_ephialtum.index, gbif_ephialtum.tolist(), color='brown')

ax2[1, 2].set_xticks(list(range(2001, 2019)))
ax2[1, 2].tick_params(axis='x', labelrotation=45)
ax2[1, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[1, 2].set_title('L. gotham - BIML GBIF', y=1, pad = 2)
ax2[1, 2].bar(gbif_gotham.index, gbif_gotham.tolist(), color='brown')

ax2[2, 2].set_xticks(list(range(2001, 2019)))
ax2[2, 2].tick_params(axis='x', labelrotation=45)
ax2[2, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[2, 2].set_title('L. trigeminum - BIML GBIF', y=1, pad = 2)
ax2[2, 2].bar(gbif_trigeminum.index, gbif_trigeminum.tolist(), color='brown')

ax2[3, 2].set_xticks(list(range(2001, 2019)))
ax2[3, 2].tick_params(axis='x', labelrotation=45)
ax2[3, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[3, 2].set_title('L. floridanum - BIML GBIF', y=1, pad = 2)
ax2[3, 2].bar(gbif_floridanum.index, gbif_floridanum.tolist(), color='brown')

ax2[4, 2].set_xticks(list(range(2001, 2019)))
ax2[4, 2].tick_params(axis='x', labelrotation=45)
ax2[4, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax2[4, 2].set_title('L. leucocomum - BIML GBIF', y=1, pad = 2)
ax2[4, 2].bar(gbif_leucocomum.index, gbif_leucocomum.tolist(), color='brown')


ax3[0, 2].set_xticks(list(range(2001, 2019)))
ax3[0, 2].tick_params(axis='x', labelrotation=45)
ax3[0, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[0, 2].set_title('L. abanci - BIML GBIF', y=1, pad = 2)
ax3[0, 2].bar(gbif_abanci.index, gbif_abanci.tolist(), color='brown')

ax3[1, 2].set_xticks(list(range(2001, 2019)))
ax3[1, 2].tick_params(axis='x', labelrotation=45)
ax3[1, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[1, 2].set_title('L. admirandum - BIML GBIF', y=1, pad = 2)
ax3[1, 2].bar(gbif_admirandum.index, gbif_admirandum.tolist(), color='brown')

ax3[2, 2].set_xticks(list(range(2001, 2019)))
ax3[2, 2].tick_params(axis='x', labelrotation=45)
ax3[2, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[2, 2].set_title('L. oblongum - BIML GBIF', y=1, pad = 2)
ax3[2, 2].bar(gbif_oblongum.index, gbif_oblongum.tolist(), color='brown')

ax3[3, 2].set_xticks(list(range(2001, 2019)))
ax3[3, 2].tick_params(axis='x', labelrotation=45)
ax3[3, 2].set_xticklabels(['', 2002,'', 2004,'', 2006,'', 2008,'', 2010,'', 2012,'', 2014,'', 2016,'', 2018], ha='right', minor=False, rotation_mode='anchor', fontsize=8)
ax3[3, 2].set_title('L. versatum - BIML GBIF', y=1, pad = 2)
ax3[3, 2].bar(gbif_versatum.index, gbif_versatum.tolist(), color='brown')


# make figures tight layout
fig0.tight_layout(pad=1)
fig1.tight_layout(pad=1)
fig2.tight_layout(pad=1)
fig3.tight_layout(pad=1)

#this spacing increases vertical padding. May need to increase slightly...
fig0.subplots_adjust(hspace=0.55) 
fig1.subplots_adjust(hspace=0.55) 
fig2.subplots_adjust(hspace=0.55) 
fig3.subplots_adjust(hspace=0.55) 

#save the figures
fig0.savefig( 'Figure 1 - control', dpi=300)    
fig1.savefig( 'Figure 2', dpi=300)    
fig2.savefig( 'Figure 3-5-rows', dpi=300)    
fig3.savefig( 'Figure 4', dpi=300)    


plt.show()
