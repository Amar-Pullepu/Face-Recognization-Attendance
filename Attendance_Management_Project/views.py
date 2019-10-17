from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
import json

import numpy as np
from PIL import Image
import base64
import re
from io import StringIO, BytesIO
import cv2
import face_recognition

import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyDpDl1RtmJLRgmNyrtX8TmQ_S20CsWJPTw",
    'authDomain': "facial-attendance-51766.firebaseapp.com",
    'databaseURL': "https://facial-attendance-51766.firebaseio.com",
    'projectId': "facial-attendance-51766",
    'storageBucket': "facial-attendance-51766.appspot.com",
    'messagingSenderId': "159422306378",
    'appId': "1:159422306378:web:afafa94ca12b970431eeb3",
    'measurementId': "G-MMS71VDRW4"
  }
 
fire = pyrebase.initialize_app(firebaseConfig)

authe = fire.auth()

def login(request):
    
    return render(request, 'login.html',{'error':'0'})

def home(request):
    if(request.method == 'POST'):
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            print(user['idToken'])
        except:
            return redirect('wrongCredentials')
        sessionId = user['idToken']
        request.session['uid'] = str(sessionId)
        return render(request, 'Home.html', {'i':email})
    return redirect('login', permanent=True)

def wrongCredentials(request):
    return render(request, 'login.html',{'error':'1'})

def logOut(request):
    auth.logout(request)
    return render(request, 'login.html',{'error':'2'})

def ajaxCanvas(request):
    try:
        image_b64 = request.POST.get('imageBase64')
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)        
        #print("Debug 1")
        image_PIL = Image.open(BytesIO(base64.b64decode(image_data)))
        #print("Debug 2")
        image_np = np.array(image_PIL)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        nam = ""
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([Known_Face_Encoding], face_encoding)
            
            face_distances = face_recognition.face_distance([Known_Face_Encoding], face_encoding)
            
            if (matches[0] and  face_distances[0] < 0.3):
                nam = "True"
        #print(type(image_np))
        #print('Image received: {}' + str(image_np.shape))
        return HttpResponse(json.dumps({'name': nam}), content_type="application/json")
    except:
        print("Error")
    return HttpResponse("Success!")
               
