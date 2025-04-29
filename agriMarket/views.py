from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "index.html")

def login_view(request):
    msg = None
    form = LoginForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                
                lat = request.POST.get('lat')
                lng = request.POST.get('lng')
                if lat and lng:
                    user.lat = lat
                    user.lng = lng
                    user.save(update_fields=['lat', 'lng'])

                if user.is_admin():
                    return redirect("admin")
                elif user.is_buyer():
                    return redirect("buyer")
                elif user.is_farmer():
                    return redirect("farmer")
                else:
                    msg = "Role not assigned. Contact admin."
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating form"

    return render(request, "login.html", {"form": form, "msg": msg})


def register(request):
    msg = None
    if(request.method == "POST"):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            msg = "User created"
            user.lat = request.POST.get('lat')
            user.lng = request.POST.get('lng')
            user.save()
            return redirect("login")
        else :
            msg = "form is not valid"
    else : 
        form = RegisterForm()
    return render(request, 'register.html', {"form":form, "msg":msg})

def home(request):
    return render(request, 'index.html')


def logout(request):
    auth_logout(request)
    return redirect('login') 


import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pickle

model = joblib.load('ml_model/price_predictor.pkl')

# @csrf_exempt
def predict_price(request):
    if request.method == 'POST':
        try:
            state = request.POST.get('state')
            district = request.POST.get('district')
            commodity = request.POST.get('commodity')
            month = int(request.POST.get('month'))

            # Your existing prediction logic
            season_map = {
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Summer',
                6: 'Summer', 7: 'Monsoon', 8: 'Monsoon',
                9: 'Monsoon', 10: 'Autumn', 11: 'Autumn'
            }
            season = season_map.get(month)

            input_df = pd.DataFrame([{
                'State': state,
                'District': district,
                'Commodity': commodity,
                'Season': season,
                'Month': month
            }])

            prediction = model.predict(input_df)[0]
            predicted_price = round(prediction, 2) / 100

            # Store the prediction in session
            request.session['predicted_price'] = "{:.2f}".format(predicted_price)
            request.session['prediction_details'] = {
                'state': state,
                'district': district,
                'commodity': commodity,
                'month': month
            }

            return redirect('buyer')

        except Exception as e:
            # Store error in session
            request.session['prediction_error'] = str(e)
            return redirect('buyer')

    return redirect('buyer')