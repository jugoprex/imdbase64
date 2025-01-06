import os
import pandas as pd
import zipfile

# open zip file
path = 'data/families.zip'
# extract all files

with zipfile.ZipFile(path, 'r') as zip_ref:
    zip_ref.extractall('data/unzipped/')

# for each file in the unzipped folder
# read the file, add a column with the file name, and append to a global dataframe
data = pd.DataFrame()
for file in os.listdir('data/unzipped/'):
    df = pd.read_csv('data/unzipped/'+file)
    id = file.split('.')[0].split('_')[1]
    df['id'] = id
    data = pd.concat([data, df])

# for each family (id), download all images in url column and save them in a folder with the family id.
import requests
import shutil

for index, row in data.iterrows():
    url = row['url']
    image = row['image']
    person_id = row['imdb_id']
    response = requests.get(url, stream=True)
    
    folder_path = f'data/images/{person_id}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    with open(f'{folder_path}/{image}', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        print(f'Image {image} downloaded for person {person_id}')
    del response