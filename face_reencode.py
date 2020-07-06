import os
import face_recognition
import pickle
all_face_encodings = {}
            #i=0
for filename in os.listdir("input_images"):
    print(filename)
    img1 = face_recognition.load_image_file(os.path.join("input_images",filename))
            #print(os.path.join(folder,filename))
                #if img1 is not None:
    all_face_encodings[filename[:-4]]=face_recognition.face_encodings(img1)[0]
                #i=i+1
    with open('dataset_faces.dat', 'wb') as fa:
        pickle.dump(all_face_encodings, fa)
