import matplotlib.pyplot as plt

import pandas as pd
pd.set_option('display.max_columns', None)  
import csv

def fill_zero_years(series, year1, year2):
    #Given a series of years and counts, fills in zeros for the years that aren't included in the original series
    year_list = list(range(year1, year2+1))
    for year in year_list:
        if year not in series:
            series.loc[year] = 0
            
    #sort and return it
    series = series.sort_index()
    
    return series

def count_by_year(allbees, year1, year2, species_name):
    ###Given a start year, end year (inclusive), and species name, return a table of the counts of that bee per year
    # TODO update so that it takes the dataframe as in input to make complete incapsulated
    
    
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


def series_to_graph(year_series, species_name):
    ###Given a Series (which is made by the count_by_year function), it makes a bar graph. Species name is a string that will be the graph title and filename
    #does all that stuff even work in a method?? Let's find out!
    #set fig size
    plt.rcParams["figure.figsize"] = (9,5)
    
    ## To reset fig size, use: plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]
    
    
    # scatter plot
    ##plt.plot(Lgotham_summary.index.values.tolist(), Lgotham_summary['year_numbers'].values.tolist(), 'ro')
    ###################plt.plot(results, '-o') #working code for scatter
    
    #stats dataset is 'rebeccapurple', I think GBIF is brown????, and kam is #1f77b4, 2011 version is green
    plt.bar(results.index, results.tolist(), width= 0.8, color='brown') # For a bar gotta do this weird thing because results is a pandas Series. A Series! Which has special properties, etc. God I have no idea how this code works
    #plt.plot(results, 'or-')
    ##plt.xlabel('xlabel', fontsize=18)
    
    #old settings
    #plt.xlabel('Year', fontsize=14)
    #plt.xticks(results.index)
    #plt.xticks(rotation = 45, ha='right', rotation_mode='anchor')
    #plt.ylabel('# Records', fontsize=14)
    
    #new settings for Lasio fig
    plt.xlabel('Year', fontsize=22) #was 24 previously
    plt.yticks(fontsize=20)
    plt.xticks(results.index)
    
    plt.xticks(rotation = 45, ha='right', rotation_mode='anchor', fontsize=14)
    plt.ylabel('# Records', fontsize=24)    
    
    #this is supposed to keep the axes as integers
    plt.locator_params(axis="y", integer=True)
    
    ##ax = plt.gca()
    ##ax.set_xlim([2000, None])
    ##plt.xlim(xmin=2000)
    ##plt.rcParams['axes.xmargin'] = 0
    
    # set the title
    plt.title(species_name, fontsize=16)
    ###plt.ylim(ymin=-1)#only use -1 for scatter plot
    plt.ylim(ymin=0)
    
    #adjusting margin so tick marks don't start so far from begininging of x axis
    plt.margins(x=0.02)
    
    
    #plt.ylabel("x",labelpad=10)    
    
    # prevents x axis label from being cut off
    plt.tight_layout()
    
    

    
    plt.subplots_adjust(left=0.15, right=0.98, top=0.9, bottom=0.25)
    
    #save the plot
    plt.savefig( 'figures/' + species_name.replace('/', '-').replace('?', 'question_mark') + '_2023-gbif.png', dpi=300)    
    
    # show the plot
    #plt.show()    
    
    #close the plot so they  don't stack
    plt.close()


def graph_proportion_bad(allbees, year1, year2, graph_color, dataset_name, all_data = False):
    plt.rcParams["figure.figsize"] = (9,5)
    
    #Given a dataset, start year, end year, and maybe color, this will create a graph that shows a stacked bar graph
    #showing the number of good + bad records per year
    # New thing ------ calculate number of bad species PER YEAR.

    #Also need to count up GOOD records -- but can just do totals and subtract the Lasio, Ceratina, and genus only records
    #First just get total number of bees per year
    bees_per_year = allbees['year_numbers'].value_counts()
    print("Bees per year", bees_per_year.sort_index())
    
    
    
    # The Lasioglossum speciesthat have had their identity or identification changed significantly by Gibbs 2010,2011, to the extent where old IDs are unreliable.
    species_known_bad_pre_2010 = ["Lasioglossum pilosum", "Lasioglossum callidum", "Lasioglossum versatum", "Lasioglossum admirandum", "Lasioglossum near_admirandum", 
                                  "Lasioglossum abanci", "Lasioglossum oblongum", "Lasioglossum viridatum", "Lasioglossum viridatum_group"] # again, could also add viridatum here
    
    #first filter by bees less than 2010
    bad_Lasioglossum = allbees[allbees['year_numbers'] < 2010] 
    
    #then filter by the species known bad
    bad_Lasioglossum = bad_Lasioglossum[bad_Lasioglossum['name'].isin(species_known_bad_pre_2010)] 
    print ("Number bad lasioglossum here is:", bad_Lasioglossum.shape[0])
    
    #then we can get unique sorted by year
    bad_Lasioglossum_per_year = bad_Lasioglossum['year_numbers'].value_counts()
    
    print (bad_Lasioglossum_per_year.sort_index())
    
    
    #Now do bad Ceratina
    
    #The Ceratina species that were changed by either Rehan and Richards 2008 or Rehan and Sheffield 2011
    ceratina_changed_or_described = ["Ceratina dupla", "Ceratina floridana", "Ceratina mikmaqi"] #not including Ceratina calcarata for now
    #Ceratina morphospecies used in some of the datasets
    ceratina_morphos = ["Ceratina calcarata/dupla/mikmaqi", "Ceratina calcarata/mikmaqi", "Ceratina dupla/mikmaqi"]
    ceratina_bad_pre_2010 = ceratina_changed_or_described + ceratina_morphos #combine lists for convenience
    
    bad_Ceratina = allbees[allbees['year_numbers'] < 2010] 
    bad_Ceratina = bad_Ceratina[bad_Ceratina['name'].isin(ceratina_bad_pre_2010)]
    
    #then we can get unique sorted by year
    bad_Ceratina_per_year = bad_Ceratina['year_numbers'].value_counts()
    
    #testing out the fill zero years function
    bad_Ceratina_per_year = fill_zero_years(bad_Ceratina_per_year, year1, year2)
    
    print (bad_Ceratina_per_year.sort_index())
    
    
    #try to add togher bad lasio and bad ceratina
    bad_lasio_and_ceratina_per_year = bad_Ceratina_per_year.add(bad_Lasioglossum_per_year, fill_value=0)
    print ("added bad lasio and ceratina", bad_lasio_and_ceratina_per_year)
    
    #normalizing the name so the if statement doesnt break code
    all_bad_bees_per_year = bad_Ceratina_per_year.add(bad_Lasioglossum_per_year, fill_value=0)
    
    
    # Also count up things just identified to genus, which is an imperfect proxy, but every non-traditional name gets rejected by GBIF filters, so only way to get at question
    if 'ID_level' in allbees.columns:
        records_not_to_species = allbees[allbees['ID_level'] == "GENUS"]
        not_to_species_per_year = records_not_to_species['year_numbers'].value_counts()
        
        print("records not identified to species", not_to_species_per_year.sort_index())
        
        
        #now add in the bad records that aren' tto genus as well
        all_bad_bees_per_year = bad_lasio_and_ceratina_per_year.add(not_to_species_per_year, fill_value=0)
        print ("added bad lasio and ceratina and genera", all_bad_bees_per_year)
        
        
    #to find the good bees per year, subtract all the bad bees from all bees
    #all_good_bees_per_year = bees_per_year.subtract(all_bad_bees_per_year)
    #print("all good bees per year", all_good_bees_per_year)
    
    
    #quick hacky code to graph proportion of Lasioglossum
    ###all_bad_bees_per_year = allbees[allbees['name'].str.contains("Lasioglossum") ] 
    ###sall_bad_bees_per_year = all_bad_bees_per_year['year_numbers'].value_counts()
    
    
    #now make graph!
    plt.bar(bees_per_year.index, bees_per_year.tolist(),  color=graph_color)
    
    plt.xlabel('Year', fontsize=14)
    plt.xticks(bees_per_year.index)
    plt.xticks(rotation = 45, ha='right', rotation_mode='anchor')
    plt.ylabel('# Records', fontsize=14)
    
    #this is supposed to keep the axes as integers
    plt.locator_params(axis="y", integer=True)    

    
    # set the title
    plt.title(dataset_name, fontsize=16)
    ###plt.ylim(ymin=-1)#only use -1 for scatter plot
    plt.ylim(ymin=0)
    
    #adjusting margin so tick marks don't start so far from begininging of x axis
    plt.margins(x=0.02)
    
    # prevents x axis label from being cut off
    plt.tight_layout()
    
    #all_data = True
    if all_data == False:
        plt.bar( all_bad_bees_per_year.index,all_bad_bees_per_year.tolist(), color='darkgray', zorder = 4 )
        #plt.bar( all_bad_bees_per_year.index,all_bad_bees_per_year.tolist(), color='tomato', zorder = 4 )
    
    
    #save the plot
    
    plt.savefig("figures/" + dataset_name + '.png')    
    # show the plot
    #
    plt.show()    
    
    #close the plot so they  don't stack
    plt.close()
      
    

#all of the bee genera from the US and Canada to filter the datos data, as it has a lot of non-bees
bee_genera = ['Agapanthinus', 'Agapostemon', 'Ancylandrena', 'Ancyloscelis', 'Andrena', 'Anthemurgus', 'Anthidiellum', 'Anthidium', 'Anthophora', 'Anthophorula', 'Apis', 'Ashmeadiella', 'Atoposmia', 'Augochlora', 'Augochlorella', 'Augochloropsis', 'Bombus', 'Brachymelecta', 'Brachynomada', 'Calliopsis', 'Caupolicana', 'Cemolobus', 'Centris', 'Ceratina', 'Chelostoma', 'Chilicola', 'Coelioxys', 'Colletes', 'Conanthalictus', 'Diadasia', 'Dianthidium', 'Dieunomia', 'Dioxys', 'Dufourea', 'Epeoloides', 'Epeolus', 'Ericrocis', 'Eucera', 'Euglossa', 'Eulaema', 'Eulonchopria', 'Exomalopsis', 'Florilegus', 'Gaesischia', 'Habropoda', 'Halictus', 'Heriades', 'Hesperapis', 'Hexepeolus', 'Holcopasites', 'Hoplitis', 'Hylaeus', 'Lasioglossum', 'Leiopodus', 'Lithurgopsis', 'Lithurgus', 'Macropis', 'Macrotera', 'Martinapis', 'Megachile', 'Megandrena', 'Melecta', 'Melissodes', 'Melissoptila', 'Melitoma', 'Melitta', 'Mesoplia', 'Mesoxaea', 'Mexalictus', 'Micralictoides', 'Neolarra', 'Neopasites', 'Nomada', 'Nomia', 'Odyneropsis', 'Oreopasites', 'Osmia', 'Panurginus', 'Paranomada', 'Paranthidium', 'Peponapis', 'Perdita', 'Protandrena', 'Protodufourea', 'Protosmia', 'Protoxaea', 'Pseudaugochlora', 'Pseudoanthidium', 'Pseudopanurgus', 'Ptiloglossa', 'Ptilothrix', 'Rhopalolemma', 'Simanthedon', 'Sphecodes', 'Sphecodosoma', 'Stelis', 'Svastra', 'Syntrichalonia', 'Temnosoma', 'Tetraloniella', 'Townsendiella', 'Trachusa', 'Triepeolus', 'Triopasites', 'Xenoglossa', 'Xeralictus', 'Xeroheriades', 'Xeromelecta', 'Xylocopa', 'Zacosmia', 'Zikanapis']



#Read in midatlantic bees dataset

print ("code is running! beep boop")

#Read in data ===== this is the Kammerer et al. (2020) dataset
"""
allbees = pd.read_csv("1OccurrenceLevel_AllBees.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
print ("file successfully read in!")


#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year'], errors = 'coerce')
"""

#gonna try it on the 2011 dataset 
"""
allbees = pd.read_csv("2011-version.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode', encoding='latin-1')
print ("file successfully read in!")


#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year1'], errors = 'coerce')

"""

# Read in the GBIF dataset

print ("code is running!")
allbees = pd.read_csv("usgs-data.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode', header = None, 
                      names = ['num', 'code', 'web_address', 'animal', 'arthropod', 'insecta', 'order', 'family', 'genus', 'name', 'mystery', 'ID_level', 'scientific name', 'name_again',
                               'blank','country','blank2','state', 'blank3', 'blank4', 'code2', 'lat', 'lon', 'elev_maybe', 'y', 'z', 'aa', 'ab', 'ac', 'full_date', 'day', 'month', 'year',
                               'another_number', 'same_number_again', 'preserved_specimen', 'bison', 'inst_code',  'event_and_DRO_num', 'an', 'collector', 'ID_date',
                               'cc', 'ar', 'identifier', 'au', 'time','geode' ])
print ("file successfully read in!")
#allbees = pd.read_csv("0086423-210914110416597.csv", sep='\t', error_bad_lines=False, index_col=False, dtype='unicode')
allbees = pd.read_csv("2023-data/0273179-220831081235567.csv", sep='\t', error_bad_lines=False, index_col=False, dtype='unicode') #this is the 2023 new data

#print (allbees.head())


#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year'], errors = 'coerce')
#allbees['identifier'] = allbees['web_address'].str.replace("http://www.discoverlife.org/mp/20l?id=", "")

#filtering out anything that isn't in a bee family:
allbees = allbees[allbees['family'].isin(['Apidae', 'Andrenidae', 'Colletidae', 'Halictidae', 'Megachilidae', 'Melittidae'])] 

#Use only records from the US
allbees = allbees[allbees['countryCode'] == "US"] 

#filtering out all years lower than 2000 because they are messing up my graphs
allbees = allbees[allbees['year_numbers'] > 1999] 

#updating species name column name
allbees['name']= allbees['species']

#updating taxon rank name
allbees['ID_level'] = allbees['taxonRank']


#ok now we move onto the datos dataset
"""
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


# now test out the county by year function
species_name = "Lasioglossum versatum"
results = count_by_year(allbees, 2000, 2015, species_name)
print ("count_by_year results", results)
#series_to_graph(results, species_name)

print (allbees.head())
"""


#renaming columns so that the Kammerer dataset runs on "grouped_name" rather than "name"
##allbees.rename(columns={'name': 'old_name'}, inplace=True)
##allbees.rename(columns={'grouped_name': 'name'}, inplace=True)

print(allbees.head())

all_species = allbees['name'].unique()






#This block should be un-commented out to make graphs for each individual species in the dataset. 

#And here we do a subset of species
###all_species = ["Lasioglossum ephialtum", "Lasioglossum floridanum", "Lasioglossum leucocomum", "Lasioglossum gotham", "Lasioglossum trigeminum", "Lasioglossum near_admirandum", "Lasioglossum admirandum"]


#now loop through and get results and make a graph for each species. This is the current code. Uncomment to run.
for bee in all_species:
    print('bee', bee)
    #results = count_by_year(allbees, 2002, 2016, bee) #This is for mid atlantic dataset
    #results = count_by_year(allbees, 2001, 2018, bee) #This is range for GBIF OLD
    results = count_by_year(allbees, 2001, 2022, bee) #This is range for GBIF NEW
    
    #results = count_by_year(allbees, 2001, 2015, bee) #This is range for Datos -- though it does have some 1999 records that we will have already filtered out
    
    if type(bee) == str:
        
        #trying to filter out non bee genera here...
        if (bee.split(' ', 1)[0]) in bee_genera:
            series_to_graph(results, bee)



#This block is to create the proportion good / bad graphs for the entire dataset
#graph_proportion_bad(allbees, 2001, 2015, 'rebeccapurple', 'Datos') #datos dataset
#graph_proportion_bad(allbees, 2002, 2016, '#1f77b4', 'Kammerer et al. (2020)')#Kammerer dataset
#graph_proportion_bad(allbees, 2001, 2018, 'brown', 'BIML GBIF')#BIML GBIF dataset OLD
graph_proportion_bad(allbees, 2001, 2022, 'brown', 'BIML GBIF')#BIML GBIF dataset NEW

#graph_proportion_bad(allbees, 2001, 2015, 'green', '2011 version') #datos dataset

#allbees = allbees[allbees['year_numbers'] < 2010] 
#graph_proportion_bad(allbees, 2001, 2009, 'brown', 'BIML GBIF 2001-2009')#BIML GBIF dataset but only the years 2001-2009

#GBIF dataset



#let us try the graphing function here, yay!
#series_to_graph(results, species_name)


