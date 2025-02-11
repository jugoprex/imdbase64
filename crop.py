from pathlib import Path
import pickle
from prepro import process_person
from face_processing import load_data
from prepro import sort_images
from tqdm import tqdm
import numpy as np

def separate_images(data):
    # create 70-30 split for training and testing by id
    # get all ids, shuffle them, split them
    split_value = 0.7
    ids = data['id'].unique()
    np.random.shuffle(ids)
    train_ids = ids[:int(len(ids)*split_value)]
    test_ids = ids[int(len(ids)*split_value):]
    # get imdb_ids for each id
    train_imdb_ids = data[data['id'].isin(train_ids)]['imdb_id'].unique()
    test_imdb_ids = data[data['id'].isin(test_ids)]['imdb_id'].unique()
    return train_imdb_ids, test_imdb_ids


def prepare_for_training():
    data = load_data()
    #tqdm
    train, test = separate_images(data)
    print(f"Train: {len(train)} Test: {len(test)}")
    print("Preparing training data")
    for person_id in tqdm(train):
        sort_images(person_id, data, "train")
    print("Preparing testing data")
    for person_id in tqdm(test):
        sort_images(person_id, data, "test")



def crop_everyone():
    pickle_file = Path("encodings_dictionary_filenames.pickle")
    encodings = pickle.load(pickle_file.open("rb"))
    for person_id in tqdm(encodings.keys()):
        try:
            process_person(person_id, encodings)
        except ValueError as e:
            print(f"Error processing {person_id}: " + str(e))

def main():
    crop_everyone()
    prepare_for_training()


if __name__ == "__main__":
    main()
