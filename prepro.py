import face_recognition
from face_recognition import face_distance
from face_recognition_utils import check_crop
from pathlib import Path
import pickle

class person:
    id: str
    emb: list
    embs: list

    def __init__(self, id, db, threshold):
        self.id = id
        self.emb = self.find_representative(db)
        self.embs = self.find_themselves(db, threshold)

    @classmethod    
    def from_embeddings(cls, id, db, threshold):
        emb = self.find_representative(db)
        embs = self.find_themselves(db, threshold)
        return cls(id, emb, embs)

    def find_themselves(self, db, th):
        embs = []
        for l in db[self.id]:
            for face in l:
                distance = face_distance([face["embedding"]], self.emb["embedding"])[0]
                if distance <= th:
                   embs.append(face)
        return embs

    def find_representative(self, db):
        for l in db[self.id]:
            if len(l) == 1:
                return l[0]
        raise ValueError("No unique embedding found")

    def __str__(self):
        return f"{id} : {{ for file_name }}"

# Por cada carpeta
#    * Buscar alguna foto con un unico embedding
#    * Ese emb pasa a ser el emb "identificatorio"

def process_person(person_id, encodings):
    per = person(person_id, encodings, 0.6)
    for e in per.embs:
        path = f"data/images/{person_id}/{e['filename']}.jpg"
        img = face_recognition.load_image_file(path)
        img = check_crop(img, e['bounding'])
        # remove jpg extension
        path = path.split('.')[0]
        img.save(f"{path}_crop.jpg")
        print(f"Processed {path}")


