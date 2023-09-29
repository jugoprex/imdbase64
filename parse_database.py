# get lines in db of families with :
# parents aged 20-30
# children aged 30+

import pandas as pd

DATABASE = 'imdb-aging.dat'
FILE = 'parents_crosschecked.csv'
i = 1
with open(FILE, 'r') as f:
    df = pd.read_csv(f, delimiter=',')
    with open(DATABASE, 'r') as g:
        database = pd.read_csv(g, delimiter=',')
        for index, row in df.iterrows():
            #find all ocurrences of the imdb_id in the database
            parent1 = database.loc[database['imdb_id'] == row[' parent1_imdb_id']].copy()
            parent2 = database.loc[database['imdb_id'] == row[' parent2_imdb_id']].copy()
            child = database.loc[database['imdb_id'] == row['child_imdb_id']].copy()
            # for every entry in each slice of the df, add a column 'age' with the age of the actor - the year of birth
            for df in [parent1, parent2, child]:
                #add age column
                df[' age'] = 0
                for index, row in df.iterrows():
                    df.loc[index, ' age'] = int(df.at[index, 'picyear']) - int(df.at[index, 'byear'])
            # return all rows where the parent was between 15 and 40 years old and the child was 20+
            parent1 = parent1[(parent1[' age'] >= 15) & (parent1[' age'] <= 40)]
            parent2 = parent2[(parent2[' age'] >= 15) & (parent2[' age'] <= 40)]
            child = child[child[' age'] >= 20]
            # concatenate the three dataframes
            parents = pd.concat([parent1, parent2])
            # add column with kinship
            parents[' kinship'] = 'parent'
            child[' kinship'] = 'child'
            if parents.empty or child.empty:
                i += 1
                continue
            merged = pd.concat([parents, child])
            merged.to_csv(f'families_{i}.csv', index=False)
            i += 1
            