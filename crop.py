from face_processing import load_data
from face_recognition_utils import crop_all_faces, create_dict, draw_faces
import pickle

# Load data
data = load_data('data/unzipped/')

# Save encodings dictionary
def save_encodings_dictionary(data):
    encodings_dictionary = create_dict(data)
    with open('encodings_dictionary.pickle', 'wb') as handle:
        pickle.dump(encodings_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Example usage
crop_all_faces('27', data, 'encodings_dictionary.pickle')