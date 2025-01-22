from pathlib import Path
import pickle
from prepro import process_person
from face_processing import load_data
from prepro import sort_images
from tqdm import tqdm

def prepare_for_training():
    data = load_data()
    #tqdm
    for person_id in tqdm(data['imdb_id'].unique()):
        sort_images(person_id, data)

def crop_everyone():
    pickle_file = Path("encodings_dictionary_filenames.pickle")
    encodings = pickle.load(pickle_file.open("rb"))
    for person_id in encodings.keys():
        try:
            process_person(person_id, encodings)
        except ValueError as e:
            print(f"Error processing {person_id}: " + str(e))

def main():
    prepare_for_training()


if __name__ == "__main__":
    main()
