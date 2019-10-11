from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
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

auth = fire.auth()

def login(request):
    
    return render(request, 'Login.html', {})

def home(request):
    if(request.method == 'POST'):
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = auth.sign_in_with_email_and_password(email, password)
        
        return render(request, 'Home.html', {'i':email})
    return redirect('login')
