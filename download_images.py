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
    id = row['id']
    url = row['url']
    image = row['image']
    response = requests.get(url, stream=True)
    
    if not os.path.exists('data/images/'+'/family_'+id):
        os.makedirs('data/images/'+'/family_'+id)
    
    with open('data/images/'+'/family_'+id+'/'+image, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response