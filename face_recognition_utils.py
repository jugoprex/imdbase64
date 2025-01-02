import os
from PIL import Image
import face_recognition
import pickle
import numpy as np

def crop_faces(df, kinship, encoding, processed_faces, distance_threshold=0.59):
    for index, row in df.iterrows():
        id = row['id']
        image = row['image']
        out_file = f'data/images/family_{id}/{image}'

        try:
            img = face_recognition.load_image_file(out_file)
        except Exception as e:
            print(f'Error loading image {out_file}: {e}')
            continue

        # Get face locations and encodings
        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img, face_locations)

        # Initialize variables to track the best match
        best_distance = float('inf')  # Start with a very high distance
        best_face_location = None

        # Find the best match
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Skip this face if its encoding has already been processed
            if any(np.allclose(face_encoding, processed_encoding) for processed_encoding, _ in processed_faces):
                continue

            # Calculate distance to the provided encoding
            distance = face_recognition.face_distance([encoding], face_encoding)[0]

            # Update best match if this face is a better match
            if distance < best_distance:
                best_distance = distance
                best_face_location = face_location

        # Only crop if the best match is within the threshold
        if best_distance <= distance_threshold:
            print(f'Match found with distance: {best_distance}')
            top, right, bottom, left = best_face_location
            rect = (left, top, right, bottom)
            img_crop = check_crop(img, rect)

            if img_crop:
                # Add the processed face encoding and location to the set
                face_key = (tuple(face_encodings[face_locations.index(best_face_location)]), best_face_location)
                if face_key not in processed_faces:
                    filename = os.path.splitext(out_file)[0]
                    output_path = f'{filename}_{kinship}_crop.jpg'
                    print(f'Saving image {output_path}')
                    img_crop.save(output_path)

                    # Mark this face as processed
                    processed_faces.add(face_key)

def crop_all_faces(id, data, encodings_path):
    with open(encodings_path, 'rb') as handle:
        encodings_dictionary = pickle.load(handle)
    df = data[data['id'] == id]
    print(f'Found {len(df)} images for id {id}')

    processed_faces = set()  # Track processed faces to avoid duplicates

    for encoding_key, encoding_value in encodings_dictionary.items():
        if id in encoding_key:
            kinship = encoding_key.split(id)[1]
            print(f'Found {len(encoding_value)} faces for kinship {kinship} in id {id}')
            for encoding in encoding_value:
                crop_faces(df, kinship, encoding, processed_faces)

def draw_all_faces(df):
    from IPython.display import display
    image_landmarks = {}
    for index, row in df.iterrows():
        id = row['id']
        image = row['image']
        out_file = f'data/images/family_{id}/{image}'
        print(f'Processing image {out_file}')
        try:
            img = face_recognition.load_image_file(out_file)
        except Exception as e:
            print(f'Error loading image {out_file}: {e}')
            continue

        landmarks = face_recognition.face_landmarks(img)
        image_landmarks[row['url']] = landmarks

        for face_landmarks in landmarks:
            for points in face_landmarks.values():
                for x, y in points:
                    img[y - 1:y + 2, x - 1:x + 2] = [255, 255, 255]
                    img[y, x] = [255, 255, 255]

        img_pil = Image.fromarray(img)
        display(img_pil)

def draw_faces(id, data):
    df = data[data['id'] == id]
    print(f'Found {len(df)} images for id {id}')
    draw_all_faces(df)

def create_dict(data):
    face_encodings = {}
    for _, row in data.iterrows():
        id = row['id']
        image = row['image']
        kinship = row['kinship']
        out_file = f'data/images/family_{id}/{image}'

        try:
            img = face_recognition.load_image_file(out_file)
        except Exception as e:
            print(f'Error loading image {out_file}: {e}')
            continue

        embeds = face_recognition.face_encodings(img)
        if not embeds:
            continue

        key = f'{id}{kinship}'
        if key in face_encodings:
            face_encodings[key].extend(embeds)
            print(f'Added {len(embeds)} faces to key {key}')
        else:
            face_encodings[key] = embeds
            print(f'Created key {key} with {len(embeds)} faces')
    return face_encodings

def check_crop(img, rect):
    img_pil = Image.fromarray(img)
    return img_pil.crop(rect)
