from pathlib import Path
import pickle
from prepro import process_person

pickle_file = Path("encodings_dictionary_filenames.pickle")
encodings = pickle.load(pickle_file.open("rb"))

for person_id in encodings.keys():
    try:
        process_person(person_id, encodings)
    except ValueError as e:
        print(f"Error processing {person_id}: " + str(e))