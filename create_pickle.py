import pickle
from face_processing import load_data
from face_recognition_utils import create_dict

# Load data
data = load_data('data/unzipped/')

# Save encodings dictionary
def save_encodings_dictionary(data):
    encodings_dictionary = create_dict(data)
    with open('encodings_dictionary_filenames.pickle', 'wb') as handle:
        pickle.dump(encodings_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

save_encodings_dictionary(data)