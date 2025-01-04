import face_recognition
from face_recognition import face_distance
from pathlib import Path

class person:
    id: String
    emb
    embs

    def __init__(self, id, emb, embs):
        self.id = id
        self.emb = emb
        self.embs = embs

    @classmethod    
    def from_embeddings(cls, id, db, theshold):
        emb = self.find_representative(db)
        embs = self.find_themselves(db, threshold)
        return cls(id, emb, embs)

    def find_themselves(self, db, th):
        embs = []
        for l in db[self.id]:
            for face in l:
                distance = face_distance(face, emb)[0]
                if distance <= th:
                    embs.append(face)
        return embs

    def find_representative(self, db):
        for l in db[self.id]:
            if length(l) == 1:
                return l[0]
        raise ValueError

    def __str__(self):
        return f"{id} : {{ for file_name }}"

# Por cada carpeta
#    * Buscar alguna foto con un unico embedding
#    * Ese emb pasa a ser el emb "identificatorio"
