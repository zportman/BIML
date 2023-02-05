"""
This is a program to quickly and efficiently analyze bee datasets, particularly the various 
datasets from the USGS Bee Inventory and Monitoring Lab
also I'm learning pandas

"""
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)  
import csv

#First setting up all the lists of species for convenience.

#The Ceratina species that were changed by either Rehan and Richards 2008 or Rehan and Sheffield 2011
ceratina_changed_or_described = ["Ceratina dupla", "Ceratina floridana", "Ceratina mikmaqi", "Ceratina calcarata"] #including Ceratina calcarata for now

#Ceratina morphospecies used in some of the datasets
ceratina_morphos = ["Ceratina calcarata/dupla/mikmaqi", "Ceratina calcarata/mikmaqi", "Ceratina dupla/mikmaqi"]

#Lasioglossum species that were described or newly reinstated by Gibbs 2010 or 2011. Only includes the abundant species (in the datasets I'm looking at)
species_desc_or_rein_Gibbs = ["Lasioglossum ephialtum", "Lasioglossum gotham", "Lasioglossum trigeminum", "Lasioglossum floridanum", "Lasioglossum leucocomum"]

#The rest of the species that were described or newly reinstated by Gibbs 2010 or 2011, included in a separate list because they occur in low numbers
other_species_desc_Gibbs = ["Lasioglossum taylorae", "Lasioglossum timothyi", "Lasioglossum georgeickworti", "Lasioglossum katherineae", 
                            "Lasioglossum rozeni"]

#Species characterized as frequently or "often misidentified" by Gibbs 2011
species_freq_misidentified = ["Lasioglossum abanci", "Lasioglossum admirandum", "Lasioglossum near_admirandum", 
                              "Lasioglossum oblongum", "Lasioglossum versatum", "Lasioglossum admirandum/rohweri",
                              "Lasioglossum rohweri/versatum", "Lasioglossum viridatum", "Lasioglossum viridatum_group"] # could potentially add "Lasioglossum viridatum_group" and L. viridatum....

# The Lasioglossum species that have had their identity or identification changed significantly by Gibbs 2010,2011, to the extent where old IDs are unreliable.
species_known_bad_pre_2010 = ["Lasioglossum pilosum", "Lasioglossum callidum", "Lasioglossum versatum", "Lasioglossum admirandum", "Lasioglossum near_admirandum", 
                              "Lasioglossum abanci", "Lasioglossum oblongum", "Lasioglossum viridatum", "Lasioglossum viridatum_group",
                              "Lasioglossum admirandum/rohweri", "Lasioglossum rohweri/versatum"                              ] # adding viridatum in here because it's listed as "viridatum group" in the original data

#All of the species descirbed in Gibbs 2010. 
ALL_species_described_Gibbs_2010 = ['abundipunctum', 'atwoodi', 'dashwoodi', 'ebmerellum', 'ephialtum', 'imbrex', 'knereri', 'lilliputense', 'macroprosopum', 
                                    'packeri', 'prasinogaster', 'reasbeckae', 'sablense', 'sandhousiellum', 'sheffieldi', 'sitocleptum', 'taylorae', 'timothyi', 'yukonae']

# only NEWLY reinstated, not just a name change
species_reinstated_by_Gibbs_2010 = ['floridanum', 'leucocomum'] 

#All of the species described in Gibbs 2011
ALL_species_described_Gibbs_2011 = ['arantium', 'ascheri', 'batya', 'curculum', 'furunculum', 'georgeickworti', 'gotham', 'izawsum', 'katherineae', 'rozeni', 'trigeminum']

#all of the bee genera from the US and Canada to filter the datos data, as it has a lot of non-bees
bee_genera = ['Agapanthinus', 'Agapostemon', 'Ancylandrena', 'Ancyloscelis', 'Andrena', 'Anthemurgus', 'Anthidiellum', 'Anthidium', 'Anthophora', 'Anthophorula', 'Apis', 'Ashmeadiella', 'Atoposmia', 'Augochlora', 'Augochlorella', 'Augochloropsis', 'Bombus', 'Brachymelecta', 'Brachynomada', 'Calliopsis', 'Caupolicana', 'Cemolobus', 'Centris', 'Ceratina', 'Chelostoma', 'Chilicola', 'Coelioxys', 'Colletes', 'Conanthalictus', 'Diadasia', 'Dianthidium', 'Dieunomia', 'Dioxys', 'Dufourea', 'Epeoloides', 'Epeolus', 'Ericrocis', 'Eucera', 'Euglossa', 'Eulaema', 'Eulonchopria', 'Exomalopsis', 'Florilegus', 'Gaesischia', 'Habropoda', 'Halictus', 'Heriades', 'Hesperapis', 'Hexepeolus', 'Holcopasites', 'Hoplitis', 'Hylaeus', 'Lasioglossum', 'Leiopodus', 'Lithurgopsis', 'Lithurgus', 'Macropis', 'Macrotera', 'Martinapis', 'Megachile', 'Megandrena', 'Melecta', 'Melissodes', 'Melissoptila', 'Melitoma', 'Melitta', 'Mesoplia', 'Mesoxaea', 'Mexalictus', 'Micralictoides', 'Neolarra', 'Neopasites', 'Nomada', 'Nomia', 'Odyneropsis', 'Oreopasites', 'Osmia', 'Panurginus', 'Paranomada', 'Paranthidium', 'Peponapis', 'Perdita', 'Protandrena', 'Protodufourea', 'Protosmia', 'Protoxaea', 'Pseudaugochlora', 'Pseudoanthidium', 'Pseudopanurgus', 'Ptiloglossa', 'Ptilothrix', 'Rhopalolemma', 'Simanthedon', 'Sphecodes', 'Sphecodosoma', 'Stelis', 'Svastra', 'Syntrichalonia', 'Temnosoma', 'Tetraloniella', 'Townsendiella', 'Trachusa', 'Triepeolus', 'Triopasites', 'Xenoglossa', 'Xeralictus', 'Xeroheriades', 'Xeromelecta', 'Xylocopa', 'Zacosmia', 'Zikanapis']


def write_csv(filename, data):
    ## Given filename and A SINGLE ROW of data, it write to a csv file (APPENDING it)
    # example of how to call
    #for x in range(5):
    #     write_csv(filename, [x, x+1])
    
    with open(filename +'.csv', 'a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)    


def pre_post_2010(dataframe, species_name):
    """Given a species name, it returns the pre and post 2010 numbers of it, Aka up to 2009, and then 2010 and onwards"""
    allbees = dataframe
    
    #step 1: get all the records of a given bee 
    species = allbees[allbees['name'] == species_name]
    
    #step 1.5: find the mimimum year, aka the earlier this species waas found in the dataset
    minyear = species['year_numbers'].min()
    
    #step 2: count all the pre 2010 records
    pre2010 = species[species['year_numbers'] < 2010]
    
    #step 2.5: adding in the pre 2008 records, so that we can look at the breakdown of pre-2008 vs 2008-2009
    #pre2008 = species[species['year_numbers'] < 2008]
    
    
    #step 3: count all the records 2010 and after
    post2010 = species[species['year_numbers'] > 2009]
    
    #return the counts of pre and post 2010
    #return pre2010.shape[0], post2010.shape[0], minyear, pre2008.shape[0] # old thing for step 2.5, put in wrong place
    return pre2010.shape[0], post2010.shape[0], minyear

def pre_post_2008(dataframe, species_name):
    """Given a species name, it returns the pre and post 2008 numbers of it, Aka up to 2007, and then 2008 and onwards"""
    #just doing this to explore how the newly described species from before 2010 tend to be clumped in 2008 and 2009 rather than earlier
    allbees = dataframe
    
    #step 1: get all the records of a given bee 
    species = allbees[allbees['name'] == species_name]
    
    #step 1.5: find the mimimum year, aka the earlier this species waas found in the dataset
    minyear = species['year_numbers'].min()
    
    #step 2: count all the pre 2008 records
    pre2008 = species[species['year_numbers'] < 2008]
    
    #step 3: count all the records 2008 and after
    post2008 = species[species['year_numbers'] > 2007]
    
    #return the counts of pre and post 2010
    #return pre2010.shape[0], post2010.shape[0], minyear, pre2008.shape[0] # old thing for step 2.5, put in wrong place
    return pre2008.shape[0], post2008.shape[0], minyear


def pre_post_encapsulator(allbees):
    ### Putting a bunch of code in here because I repeat it a bunch of times. It's messy an inefficient, oh well
    ### This holds all the pre-post stuff and also writes it to file
    
    ### TODO -- maybe skip writing to file if there is 0 0 in the numbers.

    print ("pre- and post-2010 records for the Ceratina species that were newly described or had their identification clarified in 2010/2011")
    write_csv("pre_post", ["pre- and post-2010 records for the Ceratina species that were newly described or had their identification clarified in 2010/2011"])
    for bee in ceratina_changed_or_described:
        results = pre_post_2010(allbees, bee)
        print (bee, results)
        write_csv("pre_post", [bee, results[0], results[1]])
    
    print ("pre- and post-2010 records for the Ceratina morphospecies")
    write_csv("pre_post", ["pre- and post-2010 records for the Ceratina morphospecies"])
    for bee in ceratina_morphos:
        results = pre_post_2010(allbees, bee)
        print (bee, results) 
        write_csv("pre_post", [bee, results[0], results[1]])
        
    print ("pre- and post-2010 records for species newly described or reinstated by Gibbs")
    write_csv("pre_post", ["pre- and post-2010 records for species newly described or reinstated by Gibbs"])
    for bee in species_desc_or_rein_Gibbs:
        results = pre_post_2010(allbees, bee)
        print (bee, results)
        write_csv("pre_post", [bee, results[0], results[1]])
        
    print ("pre- and post-2010 records for species newly described or reinstated by Gibbs BUT presentin very low numbers")
    write_csv("pre_post", ["pre- and post-2010 records for species newly described or reinstated by Gibbs BUT presentin very low numbers"])
    for bee in other_species_desc_Gibbs:
        results = pre_post_2010(allbees, bee)
        print (bee, results)
        write_csv("pre_post", [bee, results[0], results[1]])
        
    write_csv("pre_post", ["pre- and post-2010 records for species described as 'frequently misidentified' by Gibbs"])
    print ("pre- and post-2010 records for species described as 'frequently misidentified' by Gibbs")  
    for bee in species_freq_misidentified:
        results = pre_post_2010(allbees, bee)
        print (bee, results)  
        write_csv("pre_post", [bee, results[0], results[1]])
        
        
def overall_stats_encapsulator(allbees):
    """This is a wrapper function that just combines a lot of code that is repeated for each of the datasets"""
    
    print("Total number of records in the dataset:", len(allbees))
    
    pre2010 = allbees[allbees['year_numbers'] < 2010]
    print ("Total number of records pre-2010:",len(pre2010)    )
    
    post2010 = allbees[allbees['year_numbers'] > 2009]
    print ("Total number of records 2010 and onwards:",len(post2010)    )
    
    
    Lasioglossum = allbees[allbees['name'].str.contains('Lasioglossum', na=False)]
    print ("Total number of Lasioglossum in the dataset:", len(Lasioglossum))
    
    pre2010_Lasioglossum = Lasioglossum[Lasioglossum['year_numbers'] < 2010]
    print ("Pre 2010 Lasioglossum total:", len(pre2010_Lasioglossum))
    
    pre_2010_described = 0
    post_2010_described = 0
    #Let's do all species newly described or reinstated by Gibbs 2010 or 2011
    all_Lasio_desc_Gibbs = ALL_species_described_Gibbs_2010 + ALL_species_described_Gibbs_2011
    for bee in all_Lasio_desc_Gibbs:
        bee = "Lasioglossum " + bee
        results = pre_post_2010(allbees, bee)
        pre_2010_described += int(results[0])
        post_2010_described += int(results[1])        
        
    print ("pre 2010 species newly describe total:", pre_2010_described)
    print ("post 2010 species newly described total:", post_2010_described)
        #write_csv("pre_post", [bee, results[0], results[1]])        
    
    
    pre_2008_described = 0
    post_2008_described = 0
    #Let's do all species newly described or reinstated by Gibbs 2010 or 2011
    all_Lasio_desc_Gibbs = ALL_species_described_Gibbs_2010 + ALL_species_described_Gibbs_2011
    for bee in all_Lasio_desc_Gibbs:
        bee = "Lasioglossum " + bee
        results = pre_post_2008(allbees, bee)
        pre_2008_described += int(results[0])
        post_2008_described += int(results[1])        
        
    print ("pre 2008 species newly describe total:", pre_2008_described)
    print ("post 2008 species newly described total:", post_2008_described)    
    
    
    
    #So then need to calcualt proprtion that are invalid....
    #here we add up total number of records with KNOWN taxonomic issues:
    
    total_known_invalid_Lasioglossum = 0
    
    for bee in species_known_bad_pre_2010:
        results = pre_post_2010(allbees, bee)
        total_known_invalid_Lasioglossum += results[0]
        
    print ("Total Lasioglossum bees with KNOWN taxonomic issues: ", total_known_invalid_Lasioglossum)
    
    
    ##pre2010 = species[species['year_numbers'] < 2010]
    
    #Let's try to add in Lasioglossum only determined to genus
    #a = allbees['name'].unique()
    #print (a)
    #Lasio_not_to_species = allbees[allbees['name'] == "Lasioglossum pilosum"]
    records_only_to_genus = 0
    records_only_to_genus_pre_2010 = 0
    if 'taxonRank' in allbees.columns:
        records_not_to_species = allbees[allbees['taxonRank'] == "GENUS"]
        print("Number of records not identified to species:", len(records_not_to_species))
        records_only_to_genus = len(records_not_to_species)
        
        records_not_to_species_pre_2010 = records_not_to_species[records_not_to_species['year_numbers'] < 2010]
        print("Number of pre-2010 not identified to species:", len(records_not_to_species_pre_2010))
        records_only_to_genus_pre_2010 = len(records_not_to_species_pre_2010)
        
        ceratina_not_to_species = records_not_to_species[records_not_to_species['genus'] == "Ceratina"]
        print ("Total Ceratina not to species", len(ceratina_not_to_species))
        ceratina_not_to_species_pre_2010 = ceratina_not_to_species[ceratina_not_to_species['year_numbers'] < 2010]
        print ("Ceratina not to species pre 2010", len(ceratina_not_to_species_pre_2010))

        lasio_not_to_species = records_not_to_species[records_not_to_species['genus'] == "Lasioglossum"]
        print ("Total Lasioglosssum not to species", len(lasio_not_to_species))
        lasio_not_to_species_pre_2010 = lasio_not_to_species[lasio_not_to_species['year_numbers'] < 2010]
        print ("Lasioglossum not to species pre 2010", len(lasio_not_to_species_pre_2010))
        
    
    #data = allbees[allbees['name'].str.match(r'\A[\w-]+\Z')]

    
    
    total_known_invalid_Ceratina= 0
    #Let's try adding the Ceratina to that list
    for bee in ceratina_morphos:
        results = pre_post_2010(allbees, bee)
        total_known_invalid_Ceratina += results[0]
    
    print ("Total Ceratina bees with KNOWN taxonomic issues: ", total_known_invalid_Ceratina)
    
    
    prop_pre2010_Lasio_invalid = total_known_invalid_Lasioglossum/len(pre2010_Lasioglossum)
    print ("Percentage of pre 2010 Lasioglossum records that are invalid:", round(100 * prop_pre2010_Lasio_invalid, 1))
    
    prop_pre2010_ALL_invalid = (total_known_invalid_Lasioglossum + total_known_invalid_Ceratina) /len(pre2010)
    print ("Proportion of ALL pre 2010 records with known taxonomic issues / invalid (Lasio + Cera):", prop_pre2010_ALL_invalid)
    
    prop_pre2010_ALL_invalid = (total_known_invalid_Lasioglossum + total_known_invalid_Ceratina + records_only_to_genus_pre_2010) /len(pre2010)
    print ("Proportion of ALL pre 2010 records with known taxonomic issues / invalid (Lasio + Cera) + records only to genus:", prop_pre2010_ALL_invalid)    
    
    print ("Proprtion of all records (2002-2016) with known taxonomic issues / invalid", (total_known_invalid_Lasioglossum + total_known_invalid_Ceratina)/len(allbees))
    all_bees_invalid = (total_known_invalid_Lasioglossum + total_known_invalid_Ceratina + records_only_to_genus)/len(allbees)
    print ("Proprtion of all records (2002-2016) with known taxonomic issues / invalid, inc specimens not ID'd to species (in all years)", all_bees_invalid)
    
                                                         
    
    
    
    #then do total number pre and post 2010
    #then do total number of Lasioglossum, and total Lasioglossum pre and post 2010
    #then get into proportion of pre-2010 lasioglossum that are invalid
    #then total proportion of records invalid


print ("code is running! beep boop")

#Read in data ===== this is the Kammerer et al. (2020) dataset
allbees = pd.read_csv("1OccurrenceLevel_AllBees.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
print ("file successfully read in!")
print ("Mid-Atlantic bees dataset")


#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year'], errors = 'coerce')


#open output file, and for the first one you wr,ite, instead of append
with open("pre_post.csv", "w", newline='') as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(["Kammerer et al. 2020"])  # write header
    writer.writerow(["Species", "records 2002-2009", "records 2010-2016"])  # write header


# Running the pre-post stuffo on the Kammerer dataset
pre_post_encapsulator(allbees)

# then run all the general stats
overall_stats_encapsulator(allbees)
    
    

#ok now we move onto the datos dataset
    
allbees = pd.read_csv("Datos1.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
print ("file successfully read in!")
print ("anthropogenic bees dataset")

print ("Total number of records in the dataset:", len(allbees))

#filter out everything that isn't in a bee genus  ------ question -- does the original paper filter out the non bees? It may not
allbees = allbees[allbees['Genus'].isin(bee_genera)] 

#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year1'], errors = 'coerce')
allbees.rename(columns={"gen_sp":"name"}, inplace=True)

#filtering out all years lower than 2001 because they are messing up my graphs and there are like 10 records
allbees = allbees[allbees['year_numbers'] > 2000] 



#open output file, this time append so to not wipe previous stu
with open("pre_post.csv", "a", newline='') as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(["Collado et al. 2019"])  # write header
    writer.writerow(["Species", "records 2002-2009", "records 2010-20XX"])  # write header


# Running the pre-post stuffo on the Kammerer dataset
pre_post_encapsulator(allbees)

# then run all the general stats
overall_stats_encapsulator(allbees)



    
    
# Read in the GBIF dataset
print ("code is running!")
#allbees = pd.read_csv("usgs-data.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode', header = None, 
#                      names = ['num', 'code', 'web_address', 'animal', 'arthropod', 'insecta', 'order', 'family', 'genus', 'name', 'mystery', 'ID_level', 'scientific name', 'name_again',
#                               'blank','country','blank2','state', 'blank3', 'blank4', 'code2', 'lat', 'lon', 'elev_maybe', 'y', 'z', 'aa', 'ab', 'ac', 'full_date', 'day', 'month', 'year',
#                               'another_number', 'same_number_again', 'preserved_specimen', 'bison', 'inst_code',  'event_and_DRO_num', 'an', 'collector', 'ID_date',
#                               'cc', 'ar', 'identifier', 'au', 'time','geode' ])
#USGS BIML dataset from https://doi.org/10.15468/dl.2e5ugx
allbees = pd.read_csv("0086423-210914110416597.csv", sep='\t', error_bad_lines=False, index_col=False, dtype='unicode')
print ("file successfully read in!")
print ("GBIF dataset")

print (allbees.head())


#convert years to numeric and assign to a new column
allbees['year_numbers'] = pd.to_numeric(allbees['year'], errors = 'coerce')
#allbees['identifier'] = allbees['web_address'].str.replace("http://www.discoverlife.org/mp/20l?id=", "")

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


#TODO maybe: also create a new column for identifier by truncating the web address

#open output file, this time append so to not wipe previous stu
with open("pre_post.csv", "a", newline='') as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(["GBIF Dataset"])  # write header
    writer.writerow(["Species", "records 20XX-2009", "records 2010-20XX"])  # write header

# Running the pre-post stuffo on the GBIF dataset
pre_post_encapsulator(allbees)

# then run all the general stats
overall_stats_encapsulator(allbees)

#print (allbees.head())



    
"""

print(allbees.head(8))


year = allbees['year']
print (year.head())
print (year.shape)




after_2010 = allbees[allbees['year_numbers'] > 2010]
print (after_2010.shape)
#print(after_2010.head)


#let's try remove any where year is blank?
hasyear = allbees[allbees['year_numbers'].notna()]
print (hasyear.shape) # ok so they all have a year!


#ok let's count all the Lasioglossum gotham in the dataset
Lgotham = allbees[allbees['name'] == "Lasioglossum gotham"]
print ("Total number of Lasioglossum gotham in the dataset:", Lgotham.shape[0])

#then let's get all the Lasioglossum gotham from 2015
Lgotham_2015 = Lgotham[Lgotham['year_numbers'] == 2015]
print (Lgotham_2015.shape) #woot, got the right number of 46

#ok lets try doing a summary of L gotham by year
print(Lgotham['year_numbers'].value_counts())






#lets go back and get all the L gotham pre 2010
Lgotham_pre2010 = Lgotham[Lgotham['year_numbers'] < 2010]
print ("Number of L gotham pre 2010:", Lgotham_pre2010.shape[0]) 

Lgotham_2010plus = Lgotham[Lgotham['year_numbers'] > 2009]
print ("Number of L gotham 2010 and after:", Lgotham_2010plus.shape[0]) 



#ok -- todo -- write a function that takes a species name and returns the pre and post 2010 numbers of it. 
#also maybe todo -- write a function that returns a count of each year and also fills in the zero years so you can graph nice




print ("function test")
test = pre_post_2010(allbees, "Lasioglossum gotham")
print (test)
print("Lasioglossum admirnadum", pre_post_2010(allbees, "Lasioglossum admirandum"))


def count_by_year(year1, year2, species_name):
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

    
    
Lgotham_summary = Lgotham['year_numbers'].value_counts()
print(Lgotham_summary.sort_index())

#let's see if we can add zero yeras to the Lasioglossum gotham dataset
Lgotham_summary.loc[2002] =0
print("added 2002")
print(Lgotham_summary.sort_index())

print(2003 in Lgotham_summary)
print(2002 in Lgotham_summary)

year1 = 2002
year2 = 2016

year_list = list(range(year1, year2+1))
print (year_list)

for year in year_list:
    if year not in Lgotham_summary:
        Lgotham_summary.loc[year] = 0
        
print(Lgotham_summary.sort_index())


Lgotham_summary = Lgotham_summary.sort_index()
print (type(Lgotham_summary))
print (Lgotham_summary.keys())
#Lgotham_summary.plot(y='index')
#plt.plot(Lgotham_summary)
#plt.show()

Lgotham_summary = Lgotham_summary.to_frame()
#Lgotham_summary.plot()
print(Lgotham_summary.columns)
print(Lgotham_summary.head())

print()
print(Lgotham_summary['year_numbers'].index.tolist())
print("years:", Lgotham_summary.index.values)


print("counts:", Lgotham_summary['year_numbers'].values.tolist())


# scatter plot
plt.plot(Lgotham_summary.index.values.tolist(), Lgotham_summary['year_numbers'].values.tolist(), 'ro')
  
# set the title
plt.title("Lasgiolossum gotham")
  
# show the plot
plt.show()

print("we are at the end")

"""