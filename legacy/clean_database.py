import pandas as pd

FILE = 'parents.csv'
NEW_FILE = 'parents_clean.csv'
CROSSCHECKED_FILE = 'parents_crosschecked.csv'
DATABASE = 'imdb-aging.dat'

# open csv and remove entrys of more than three columns
with open(FILE, 'r') as f:
    df = pd.read_csv(f, delimiter=',')
    # remove all rows with more than three columns
    df = df[df.apply(lambda x: x.count(), axis=1) <= 3]
    # remove empty columns
    df = df.dropna(axis=1, how='all')
    # put a 0 in the empty cells
    df = df.fillna(0)
    df.to_csv(NEW_FILE, index=False)

# remove ids of parents not found in imdb-aging
with open(NEW_FILE, 'r') as f:
    df = pd.read_csv(f, delimiter=',')
    keys = [' parent1_imdb_id', ' parent2_imdb_id']
    with open(DATABASE, 'r') as g:
        database = pd.read_csv(g, delimiter=',')
        for index, row in df.iterrows():
            if row[' parent1_imdb_id'] not in database['imdb_id'].values:
                df.at[index, ' parent1_imdb_id'] = 'A'
            if row[' parent2_imdb_id'] not in database['imdb_id'].values:
                 df.at[index, ' parent2_imdb_id'] = 'A'
    #get rid of all rows with an A in the second column
    df = df[(df[' parent2_imdb_id'] != 'A') | (df[' parent1_imdb_id'] != 'A')]
    df.to_csv(CROSSCHECKED_FILE, index=False)


