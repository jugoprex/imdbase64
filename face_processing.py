# File: data_processing.py
import pandas as pd
import os

# Load and preprocess the data
def load_data(data_path):
    data = pd.DataFrame()
    for file in os.listdir(data_path):
        df = pd.read_csv(os.path.join(data_path, file))
        id = file.split('.')[0].split('_')[1]
        df['id'] = id
        data = pd.concat([data, df])
    data.columns = data.columns.str.replace(' ', '')  # Remove spaces from column names
    return data

