#OR -- just left join both datasets by ID#, filter for ones that have different species names

# This can tell us if ANY IDs were updated between the 2 datasets. 

import pandas as pd
pd.set_option('display.max_columns', None)  

print ("code is running!")


biml_2022 = pd.read_csv("0086423-210914110416597.csv", sep='\t', error_bad_lines=False, index_col=False, dtype='unicode')
biml_2023 = pd.read_csv("2023-data/0273179-220831081235567.csv", sep='\t', error_bad_lines=False, index_col=False, dtype='unicode')

#replace all NaN with zero so it doesn't mess up the comparisons
biml_2022 = biml_2022.fillna("sp")
biml_2023 = biml_2023.fillna("sp")

print (biml_2022.head())

df = pd.merge(biml_2022, biml_2023, on="occurrenceID", how="inner")

#df.fillna(0)

#lasio_not_to_species_pre_2010 = lasio_not_to_species[lasio_not_to_species['year_numbers'] < 2010]


Lasio1 = df[df["occurrenceID"] == "http://www.discoverlife.org/mp/20l?id=USGS_DRO006969"] 
print ("Lasio1", Lasio1)

print (df.head())
print(len(df))


test = df.loc[df['species_x'] != df['species_y']]
print (len(test))

#ONE THING COULD DO -- CREATE NEW column combining name and gen_sp -- "gen_sp changed to name". Then do an index count of those!
test["name change"] = test['species_x'] + " changed to " + test['species_y']
print (test.head())

print(test['name change'].value_counts())

changed_counts = test['name change'].value_counts()

changed_counts.to_csv('changed_counts_biml.csv')

#test.to_csv('out-datos-11.csv')


#now let's check i any records were removed from the 2022 data in the 2023 data. 
#df = pd.merge(biml_2022, biml_2023, on="occurrenceID", how="left")

only_2022 = biml_2022[~biml_2022["occurrenceID"].isin(biml_2023["occurrenceID"])]

print (only_2022.head())

print (len(only_2022))
only_2022.to_csv('only_2022.csv')

species_counts = only_2022['species'].value_counts()
print (species_counts)
species_counts.to_csv('only_2022_species.csv')



#dig into the Osmia collinsiae changed
#osmia_collinsiae = test[test["species_x"] == "Lasioglossum admirandum"]
#osmia_collinsiae.head()
#osmia_collinsiae.to_csv('changed-Lasioglossum_admirandum.csv')