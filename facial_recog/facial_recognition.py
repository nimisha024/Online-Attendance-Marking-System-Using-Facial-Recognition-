import os
import pickle
import numpy
import face_recognition

from facial_recog.config import KNOWN_IMG_DIR, TO_BE_PROCESSED_IMG_DIR, ENCODINGS_FILE


def train():
    (_, _, img_filenames) = next(os.walk(KNOWN_IMG_DIR))

    all_face_encodings = {}
    for filename in img_filenames:
        face = face_recognition.load_image_file(os.path.join(KNOWN_IMG_DIR, filename))
        all_face_encodings[filename] = face_recognition.face_encodings(face)[0]

    with open(ENCODINGS_FILE, 'wb') as enc_file:
        pickle.dump(all_face_encodings, enc_file)


class FacialRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.preprocess()

    def preprocess(self):
        if not os.path.exists(ENCODINGS_FILE):
            train()

        with open(ENCODINGS_FILE, 'rb') as enc_file:
            all_face_encodings = pickle.load(enc_file)

        self.known_face_names = list(all_face_encodings.keys())
        self.known_face_encodings = numpy.array(list(all_face_encodings.values()))

    def recognize_face(self, image_name):
        unknown_image = face_recognition.load_image_file(os.path.join(TO_BE_PROCESSED_IMG_DIR, image_name))
        unknown_face = face_recognition.face_encodings(unknown_image)
        result = face_recognition.compare_faces(self.known_face_encodings, unknown_face)

        if True in result:
            first_match_index = result.index(True)
            return self.known_face_names[first_match_index]


fr = FacialRecognition()
