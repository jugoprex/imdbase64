from imdbparser import get_child_imdb_id, get_parents_imdb_id
import tqdm

def get_url_list(csv_file):
    '''parse csv file, and return a list after simple-processing.'''
    with open(csv_file, 'r', encoding='latin1') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line.split(',') for line in lines]
    return lines[1:] # remove head line

def get_all_unique_imdb_ids(csv_file):
    '''get all unique imdb ids from csv file.'''
    lines = get_url_list(csv_file)
    imdb_ids = [line[1] for line in lines]
    print('removing duplicates...')
    #remove duplicates and return an array
    imdb_ids = list(set(imdb_ids))
    print('total number of people: ', len(imdb_ids))
    return imdb_ids


CSV_FILE = 'imdb-aging.dat'
image_lines = get_all_unique_imdb_ids(CSV_FILE)
with open('parents.csv', 'a') as f:
    f.write('child_imdb_id, parent1_imdb_id, parent2_imdb_id, parent3_imdb_id\n')
    print('getting parent imdb ids...')
    for child in tqdm.tqdm(image_lines):
        parents = get_parents_imdb_id(child)
        if len(parents) > 0:
            parents_string = ','.join(parents)
            print(child, parents_string)
            f.write(str(child) +', '+ str(parents_string) + '\n')
f.close()

