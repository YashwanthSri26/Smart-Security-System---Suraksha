import face_recognition
import pickle

all_face_encodings = {}

img1 = face_recognition.load_image_file("tarun.jpg")
all_face_encodings["tarun"] = face_recognition.face_encodings(img1)[0]

img1 = face_recognition.load_image_file("rupa.jpg")
all_face_encodings["rupa"] = face_recognition.face_encodings(img1)[0]

img1 = face_recognition.load_image_file("nymish.png")
all_face_encodings["nymish"] = face_recognition.face_encodings(img1)[0]

print(all_face_encodings)
with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)
