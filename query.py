
import urllib.parse
from datetime import date
import json
import requests


def run_ticketmaster_query(postal_code=None, city=None, state_code=None, start_date_time=date.today(),
                           end_date_time=None):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = dict()
    params["apikey"] = ""
    if postal_code:
        params["postalCode"] = postal_code
    if city:
        params["city"] = city
    if state_code:
        params["stateCode"] = state_code
    if start_date_time:
        start_date_time = str(start_date_time) + "T00:00:00Z"
        params["startDateTime"] = str(start_date_time)
    if end_date_time:
        end_date_time = str(end_date_time) + "T23:59:00Z"
        params["endDateTime"] = str(end_date_time)

    param_string = urllib.parse.urlencode(params).replace("%3A", ":")
    url += "?" + param_string
    request = requests.get(url)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, url))


def searchQuery(location="NYC"):
    searchQuery = '''
        {
            search(location: "%s") {
                business {
                    id
                    name
                    rating
                    price
                    display_phone
                    url
                    photos
                    location {
                        address1
                        city
                        state
                        postal_code
                        country
                    }
                }
            }
        }
            ''' % (location)

    return searchQuery

def run_yelp_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    headers = {"Authorization": "",
    "Content-Type": "application/graphql",
    }
    request = requests.post('https://api.yelp.com/v3/graphql', data=query, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def query_flights(origin, destination, departureDate):
    origin += "-sky"
    destination += "-sky"
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/US/USD/en-US/" + origin + "/"+destination+"/"+departureDate

    headers = {}

    response = requests.request("GET", url, headers=headers)
    text = json.loads(response.text)
    places = text["Places"]
    carriers = text["Carriers"]
    quotes = text["Quotes"]

    smallest_quote = quotes[0]
    for quote in quotes:
        if quote["Direct"] and quote["OutboundLeg"]["DepartureDate"][:10] == departureDate and quote["MinPrice"] < smallest_quote["MinPrice"]:
            smallest_quote = quote

    airline = ""
    for carrier in carriers:
        if carrier["CarrierId"] in smallest_quote["OutboundLeg"]["CarrierIds"]:
            airline = carrier["Name"]
    destination = ""
    origin = ""
    for place in places:
        if place["PlaceId"] == smallest_quote["OutboundLeg"]["DestinationId"]:
            destination = place["Name"]
        if place["PlaceId"] == smallest_quote["OutboundLeg"]["OriginId"]:

            origin = place["Name"]

    return_info = dict()
    return_info["price"] = smallest_quote["MinPrice"]
    return_info["airline"] = airline
    return_info["destination"] = destination
    return_info["origin"] = origin
    return_info["departure_date"] = departureDate


    return return_info

# print(run_yelp_query(searchQuery()))
#
# print(query_flights("SFO", "ORD", "2020-05-05"))

# print(run_ticketmaster_query(city="Atlanta", state_code="GA"))