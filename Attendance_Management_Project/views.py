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
from . import utils
import datetime

import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyCt_ES04VDH6IyBOx810tj0eG6a17-uzTA",
    'authDomain': "face-recog-2aeb4.firebaseapp.com",
    'databaseURL': "https://face-recog-2aeb4.firebaseio.com",
    'projectId': "face-recog-2aeb4",
    'storageBucket': "face-recog-2aeb4.appspot.com",
    'messagingSenderId': "218928360961",
    'appId': "1:218928360961:web:b2d67d596e1082e97b5a00",
    'measurementId': "G-LM4YT1REVF"
  }
 
fire = pyrebase.initialize_app(firebaseConfig)

authe = fire.auth()
database = fire.database()

def login(request):
    
    return render(request, 'login.html',{'error':'0'})

def dupHome(request):
    email = ""
    try:
        idToken = request.session['uid']
        a = authe.get_account_info(idToken)
        a = a["users"]
        user = a[0]
        email = user["email"]
    except KeyError:
        return redirect('logOut')
    if(len(email.split("@")[0]) != 6):
        return render(request, 'StudentHome.html', {'i':email})
    else:
        database.child("publicData").update({"AttendanceStatus":False})
        return render(request, 'FacultyHome.html', {'i':email})
    
def attendanceClosed(request):
    email = ""
    try:
        idToken = request.session['uid']
        a = authe.get_account_info(idToken)
        a = a["users"]
        user = a[0]
        email = user["email"]
    except KeyError:
        return redirect('logOut')
    return render(request, 'StudentHome.html', {'i':email, 'Closed':"0"})
    
def attendanceRecorded(request):
    email = ""
    try:
        idToken = request.session['uid']
        a = authe.get_account_info(idToken)
        a = a["users"]
        user = a[0]
        email = user["email"]
    except KeyError:
        return redirect('logOut')
    return render(request, 'StudentHome.html', {'i':email, 'Recorded':"0"})
    
def home(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        user = authe.sign_in_with_email_and_password(email, password)
        print(user['idToken'])
    except:
        return redirect('wrongCredentials')
    sessionId = user['idToken']
    request.session['uid'] = str(sessionId)
    if(len(email.split("@")[0]) != 6):
        return render(request, 'StudentHome.html', {'i':email})
    else:
        database.child("publicData").update({"AttendanceStatus":False})
        return render(request, 'FacultyHome.html', {'i':email})

def wrongCredentials(request):
    return render(request, 'login.html',{'error':'1'})

def logOut(request):
    email = ""
    try:
        idToken = request.session['uid']
        a = authe.get_account_info(idToken)
        a = a["users"]
        user = a[0]
        email = user["email"]
        del request.session['uid']
    except KeyError:
        pass
    if(len(email.split("@")[0]) == 6):
        database.child("publicData").update({"AttendanceStatus":False})
    return render(request, 'login.html',{'error':'2'})

def showAttendance(request):
    localId = ""
    try:
        idToken = request.session['uid']
        user = authe.get_account_info(idToken)["users"][0]
        localId = user["localId"]
    except KeyError:
        return redirect('logOut')
    data = []
    for i in range(database.child("Users").child(localId).child("AttendanceLastCount").get().val()):
        Attendance = []
        Attendance.append(database.child("Users").child(localId).child("").child("").get().val())
    return render(request, 'showAttendance.html',{})
    
def ajaxCanvas(request):
    try:
        if(database.child("publicData").child("AttendanceStatus").get().val()):
            image_b64 = request.POST.get('imageBase64')
            image_data = re.sub('^data:image/.+;base64,', '', image_b64)
            image_PIL = Image.open(BytesIO(base64.b64decode(image_data)))
            image_np = np.array(image_PIL) 
            #Shape Difference
            idToken = request.session['uid']
            a = authe.get_account_info(idToken)
            a = a["users"]
            user = a[0]
            Known_Face_Encoding = database.child("Users").child(user["localId"]).child("details").child("faceDetails").get().val().split()
            Known_Face_Encoding = [float(x) for x in Known_Face_Encoding]
            #print(Known_Face_Encoding)
            Status = utils.faceRecog(Known_Face_Encoding ,image_np)
            if(Status == "True"):
                database.child("Users").child(user["localId"]).update({"PresentAttendance": "Present"})
            return HttpResponse(json.dumps({'Status': Status}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'Status': "Closed"}), content_type="application/json")
    except KeyError:
        return redirect('logOut')
    except Exception as e:
        print("error: "+str(e))
    return HttpResponse("Success!")
               
def ajaxStatusCheck(request):
    if(database.child("publicData").child("AttendanceStatus").get().val()):
        return HttpResponse(json.dumps({'Status': "Open"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Status': "Closed"}), content_type="application/json")

def ajaxAttendanceUpdate(request):
    data = {}
    try:
        idToken = request.session['uid']
        length = database.child("publicData").child("LastCount").get().val()
        data["length"] = length
        for i in range(length):
            localId = database.child("publicData").child("studentLocalId").child(i).get().val()
            val = database.child("Users").child(localId).child("PresentAttendance").get().val()
            data[i] = val
    except KeyError:
        return redirect('logOut')
    return HttpResponse(json.dumps(data), content_type="application/json")
    
def studentRegister(request):
    try:
        idToken = request.session['uid']
        database.child("publicData").update({"AttendanceStatus":False})
    except KeyError:
        return redirect('logOut')
    
    return render(request, 'studentRegister.html', {})

def postRegistration(request):
    database.child("publicData").update({"AttendanceStatus":False})
    try:
        idToken = request.session['uid']
    except KeyError:
        return redirect('logOut')
    firstName = email = request.POST.get("firstName")
    lastName = email = request.POST.get("lastName")
    email = request.POST.get("email")
    password = request.POST.get("password")
    faceDetails = request.POST.get("faceDetails")
    
    user = authe.create_user_with_email_and_password(email, password);
    uid = user['localId']
    
    attendanceData = {"AttendanceLastCount" : 0, "PresentAttendance" : "Absent"}
    database.child("Users").child(uid).set(attendanceData)
    
    data = {"firstName":firstName, "lastName":lastName, "faceDetails":faceDetails, "regNumber":email.split("@")[0]}
    database.child("Users").child(uid).child("details").set(data)
    
    
    val =database.child("publicData").child("LastCount").get().val()
    database.child("publicData").child("studentLocalId").child(val).set(user['localId'])
    val+=1;
    
    database.child("publicData").update({"LastCount":val})
    return render(request, 'postRegistration.html', {})

def markAttendance(request):
    try:
        idToken = request.session['uid']
    except KeyError:
        return redirect('logOut')
    return render(request, 'markAttendance.html', {})

def facultyAttendance(request):
    data = []
    try:
        idToken = request.session['uid']
        database.child("publicData").update({"AttendanceStatus":True})
        for i in range(database.child("publicData").child("LastCount").get().val()):
            student = []
            localId = database.child("publicData").child("studentLocalId").child(i).get().val()
            student.append(database.child("Users").child(localId).child("details").child("firstName").get().val())
            student.append(database.child("Users").child(localId).child("details").child("lastName").get().val())
            student.append(database.child("Users").child(localId).child("details").child("regNumber").get().val())
            database.child("Users").child(localId).update({"PresentAttendance": "Absent"})
            data.append(student)
        #data = [[FirstName, SecondName, Email],[],[]]
    except KeyError:
        return redirect('logOut')
    return render(request, 'facultyAttendance.html', {"data":data})

def attendanceMarked(request):
    try:
        idToken = request.session['uid']
        user = authe.get_account_info(idToken)["users"][0]
        email = user["email"]
    except KeyError:
        return redirect('logOut')
    datetime_object = datetime.datetime.now()
    Date = datetime.date.today()
    Hour = datetime_object.hour
    for i in range(database.child("publicData").child("LastCount").get().val()):
        localId = database.child("publicData").child("studentLocalId").child(i).get().val()
        val = database.child("Users").child(localId).child("AttendanceLastCount").get().val()
        database.child("Users").child(localId).child("AttendanceMarked").child(val).set(request.POST.get("sel"+str(i)))
        database.child("Users").child(localId).child("DateTime").child(val).set(Date.strftime('%m/%d/%Y')+" "+str(Hour)+"-"+str((Hour+1)%24))
        database.child("Users").child(localId).update({"AttendanceLastCount": val+1})
        database.child("Users").child(localId).update({"PresentAttendance": "Absent"})
    database.child("publicData").update({"AttendanceStatus":False})
    return render(request, 'FacultyHome.html', {'i':email, 'Status':"Marked"})