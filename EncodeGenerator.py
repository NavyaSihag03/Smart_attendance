import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://database-af492-default-rtdb.firebaseio.com/",
    'storageBucket': "database-af492.appspot.com"
})


folderPath = 'Images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentIDs = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    # print(path)
    # print(os.path.splitext(path)[0])
    studentIDs.append(os.path.splitext(path)[0])
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studentIDs)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)


    return encodeList

print("Encoding started......")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIDs = [encodeListKnown, studentIDs]
print("Encoding complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIDs, file)
file.close()
print("File Saved")