from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, get_dealer_by_state_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)
# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, id='', st=''):
    context = {}
    if request.method == "GET":
        url = "https://10e3d698.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        if id:
            dealerships = get_dealer_by_id_from_cf(url, id)
        elif st:
            dealerships = get_dealer_by_state_from_cf(url, st)
        else:
            dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://10e3d698.us-south.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        dealer_reviews = ' '.join([review.review + " " + review.sentiment + "\n" for review in reviews])
        context["review_list"] = reviews

        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        user = request.user
        url = "https://10e3d698.us-south.apigw.appdomain.cloud/api/review"
        if user.is_authenticated:
            review = {}
            json_payload = {}
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            valid_field = ["name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"]
            for key in request.POST:
                if key in valid_field:
                    review[key] = request.POST[key]
            review["name"] = "me"
            review["review"] = "This is a great car dealer"
            json_payload = {"review": review}
            result = post_request(url, json_payload)
            return HttpResponse(result)
