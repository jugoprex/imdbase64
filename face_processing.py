# File: data_processing.py
import pandas as pd
import os

# Load and preprocess the data
def load_data(data_path = 'data/unzipped/'):
    data = pd.DataFrame()
    return preprocess(data, data_path)

def preprocess(data, data_path = 'data/unzipped/'):
    for file in os.listdir(data_path):
        df = pd.read_csv(os.path.join(data_path, file))
        id = file.split('.')[0].split('_')[1]
        df['id'] = id
        data = pd.concat([data, df])
    data.columns = data.columns.str.replace(' ', '')  # Remove spaces from column names
    
    # for every "imdb_id" row that appears with multiple "id" values, reeplace the "id" value with the first
    id_replacements = {}
    for imdb_id in data['imdb_id'].unique():
        unique_ids = data[data['imdb_id'] == imdb_id]['id'].unique()
        
        if len(unique_ids) > 1:
            for old_id in unique_ids:
                id_replacements[old_id] = unique_ids[0]  # Replace with the first unique ID
                print(f"Replacing {old_id} with {unique_ids[0]}")
            data.loc[data['imdb_id'] == imdb_id, 'id'] = unique_ids[0]
    data['id'] = data['id'].replace(id_replacements)
    return data

