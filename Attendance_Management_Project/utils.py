import numpy as np
import cv2
import face_recognition

def faceRecog(Known_Face_Encoding ,image_np):
    

    small_frame = cv2.resize(image_np, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, :3]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)

    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    name = "False"

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([Known_Face_Encoding], face_encoding)
        print(matches)
        face_distances = face_recognition.face_distance([Known_Face_Encoding], face_encoding)
        print(face_distances)
        if (matches[0] and  face_distances[0] < 0.50):
            name = "True"
    return name