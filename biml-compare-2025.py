#Just some code to compare different versions of the datasets to see what has changed or if records are mismatched between datasets

import pandas as pd
pd.set_option('display.max_columns', None)  

print ("code is running!")


biml_2023 = pd.read_csv("0011366-231120084113126-2023-simple/0011366-231120084113126.csv", sep='\t', on_bad_lines='warn', index_col=False, dtype='unicode')
biml_2025 = pd.read_csv("0002129-250218110819086-simple/0002129-250218110819086.csv", sep='\t', on_bad_lines='warn', index_col=False, dtype='unicode')

#replace all NaN with zero so it doesn't mess up the comparisons
biml_2023 = biml_2023.fillna("sp")
biml_2023["trimmed_ID"] = biml_2023["occurrenceID"].str.replace("http://www.discoverlife.org/mp/20l?id=", "")


biml_2025 = biml_2025.fillna("sp")
biml_2025["trimmed_ID"] = biml_2025["occurrenceID"].str.replace("https://www.discoverlife.org/mp/20l?id=", "")


print ("BIML 2023:",biml_2023.head())
print ("BIML 2025:",biml_2025.head())

#df = pd.merge(biml_2023, biml_2025, on="occurrenceID", how="inner")
df = pd.merge(biml_2023, biml_2025, on="trimmed_ID", how='outer', indicator=True)

#df.fillna(0)

#lasio_not_to_species_pre_2010 = lasio_not_to_species[lasio_not_to_species['year_numbers'] < 2010]


#Lasio1 = df[df["occurrenceID"] == "http://www.discoverlife.org/mp/20l?id=USGS_DRO006969"] 
#print ("Lasio1", Lasio1)

print ("MERGED TABLE")
print (df.head())
print(len(df))


test = df.loc[df['species_x'] != df['species_y']]
#test = df.loc[df['species_y'] != "NaN"]
print ("TEST: ", len(test))





#ONE THING COULD DO -- CREATE NEW column combining name and gen_sp -- "gen_sp changed to name". Then do an index count of those!
test["name change"] = test['species_x'] + " changed to " + test['species_y']
print ("CHANGED NAMES:", test.head())

test.to_csv('full-changed.csv')


print(test['name change'].value_counts())

changed_counts = test['name change'].value_counts()

changed_counts.to_csv('changed_counts_biml.csv')

#test.to_csv('out-datos-11.csv')


#now let's check i any records were removed from the 2023 data in the 2025 data. 
#df = pd.merge(biml_2023, biml_2025, on="occurrenceID", how="left")

only_2023 = biml_2023[~biml_2023["trimmed_ID"].isin(biml_2025["trimmed_ID"])]

print (only_2023.head())

print ("number only 2023: ", len(only_2023))
only_2023.to_csv('only_2023.csv')

species_counts = only_2023['species'].value_counts()
print (species_counts)
species_counts.to_csv('only_2023_species.csv')

only_2025 = biml_2025[~biml_2025["trimmed_ID"].isin(biml_2023["trimmed_ID"])]

print ("number only 2025: " ,len(only_2025))
only_2025.to_csv('only_2025.csv')

#dig into the Osmia collinsiae changed
#osmia_collinsiae = test[test["species_x"] == "Lasioglossum admirandum"]
#osmia_collinsiae.head()
#osmia_collinsiae.to_csv('changed-Lasioglossum_admirandum.csv')

