import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, SentimentOptions
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if "api_key" in kwargs:
            api_key = kwargs["api_key"]
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        # Call get method of requests library with URL and parameters
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except Exception as e:
        print(e)
        # If any error occurs
        print("Network exception occurred")
        status_code = 404
        print("With status {} ".format(status_code))
        json_data = {}
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, st=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["body"]
        # For each dealer object
        for review_entry in reviews:
            # Create a CarDealer object with values in `doc` object
            if review_entry["purchase"]:
                purchase_date = review_entry["purchase_date"]
                car_make = review_entry["car_make"]
                car_model = review_entry["car_model"]
                car_year = review_entry["car_year"]
            else:
                purchase_date = ""
                car_make = ""
                car_model = ""
                car_year = ""
            sentiment = analyze_review_sentiments(review_entry["review"])
            review_obj = DealerReview(dealership=review_entry["dealership"], name=review_entry["name"], purchase=review_entry["purchase"],
            review=review_entry["review"], purchase_date=purchase_date, car_make=car_make,
            car_model=car_model, car_year=car_year, id=review_entry["id"], sentiment=sentiment)
            results.append(review_obj)

    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


def analyze_review_sentiments(text):
    api_key = "YUOSFreFPRdESYzzbKLmeMXpZ8BT2Uu7tD5PVriFqOv5"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/79a474cb-505b-491a-a158-85e0026800e7"
    params = dict()
    params["text"] = text
    params["version"] = "2021-08-01"
    params["features"] = "sentiment"

    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

    natural_language_understanding.set_service_url(url) 

    response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 

    label=json.dumps(response, indent=2) 

    label = response['sentiment']['document']['label'] 

    return(label) 