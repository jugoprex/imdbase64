from imdbparser import get_child_imdb_id
import tqdm

def getURLList(csv_file):
    '''parse csv file, and return a list after simple-processing.'''
    with open(csv_file, 'r', encoding='latin1') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line.split(',') for line in lines]
    return lines[1:] # remove head line

def get_all_unique_imdb_ids(csv_file):
    '''get all unique imdb ids from csv file.'''
    lines = getURLList(csv_file)
    imdb_ids = [line[1] for line in lines]
    print('removing duplicates...')
    #remove duplicates and return an array
    imdb_ids = list(set(imdb_ids))
    print('total number of people: ', len(imdb_ids))
    return imdb_ids

csv_file = 'IMDb-Face.csv'
image_lines = get_all_unique_imdb_ids(csv_file)
#use tqdm
print('getting children imdb ids...')
for parent in tqdm.tqdm(image_lines):
    children = get_child_imdb_id(parent)
    if len(children) > 0:
        #save children to file
        child = children[0]
        for child in children:
            # get sting of comma separated values
            child = ', '.join(child)
        print(child)
        with open('children.csv', 'a') as f:
            f.write(str(parent) +', '+ str(child) + '\n')
        f.close()

