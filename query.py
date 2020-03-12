
import urllib.parse
from datetime import date
import json
import requests



def query_flights(origin, destination, departureDate):
    origin += "-sky"
    destination += "-sky"
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/US/USD/en-US/" + origin + "/"+destination+"/"+departureDate

    headers = None

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

print(query_flights("SFO", "ORD", "2020-05-05"))