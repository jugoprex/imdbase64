import os
from PIL import Image
from collections import defaultdict
import face_recognition
import pickle
import numpy as np

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
    face_encodings = defaultdict(list)
    for _, row in data.iterrows():
        id = row['id']
        person_id = row['imdb_id']
        image = row['image']
        filename = os.path.splitext(image)[0]
        out_file = f'data/images/family_{id}/{image}'

        try:
            img = face_recognition.load_image_file(out_file)
        except Exception as e:
            print(f'Error loading image {out_file}: {e}')
            continue

        # Get face locations and encodings
        face_locations = face_recognition.face_locations(img)
        embeds = face_recognition.face_encodings(img, face_locations)
        if not embeds:
            continue

        # make a list of tuples of the form (filename, embedding)
        out = [{
            "filename": filename, 
            "embedding": embed,
            "bounding": location
            } for location, embed in zip(face_locations, embeds)]
        
        face_encodings[person_id].append(out)
        print(f'Added {len(embeds)} faces to key {person_id} on image {filename}')
    return face_encodings

def check_crop(img, rect):
    top, right, bottom, left = rect
    rect = (left, top, right, bottom)
    img_pil = Image.fromarray(img)
    cropped = img_pil.crop(rect)
    resized = cropped.resize((112, 112))
    return resized
