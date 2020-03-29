#in travelbuddy

import query

import time
from datetime import datetime
from datetime import timedelta
import sys
from operator import itemgetter

class TSP:

    def __init__(self, trip):
        self.paths = []
        self.origin = trip[0]
        self.cities = trip[1]
        self.startdate = datetime.strptime(trip[2][0], "%Y-%m-%d")
        self.enddate = datetime.strptime(trip[2][1], "%Y-%m-%d")
        self.daterange_size = (self.enddate - self.startdate).days
        self.already_queried = {}

        tl = 0
        for city in trip[1]:
            tl += trip[1][city]
        self.triplength = tl


    def fromOrigin(self):
        for i in range(self.daterange_size - self.triplength + 1):
            flightdate_str = datetime.strftime(self.startdate + timedelta(i), '%Y-%m-%d')
            for city in self.cities:
                flight = self.getFlight(self.origin, city, flightdate_str)
                self.getNext(flight, [self.origin, city], [flight], flight['price'])


    def getNext(self, prev, visited, path, price):
        # when you got to this city
        arrived_on = datetime.strptime(prev['departure_date'], "%Y-%m-%d")

        # when you need to leave the city, in str form (for the flights alg)
        leave_on = datetime.strftime(arrived_on + timedelta(self.cities[prev['destination_code']]), "%Y-%m-%d")

        # trip is over / need to go home
        if len(visited) == len(self.cities)+1:
            next_flight = self.getFlight(prev['destination_code'], self.origin, leave_on)
            path.append(next_flight)
            price += next_flight['price']
            self.paths.append((price, path))
            return

        # go to new city
        for city in self.cities:
            if (city not in visited) or (len(visited) == len(self.cities)+1 and city == self.origin):
                next_flight = self.getFlight(prev['destination_code'], city, leave_on)
                visited.append(city)
                path.append(next_flight)
                price += next_flight['price']
                self.getNext(next_flight, visited, path, price)

    def getFlight(self, origin, dest, date):
        passed = False
        #next_flight = ''
        tries = 0
        while not passed and tries < 5:
            tries += 1
            try:
                next_flight = query.query_flights(origin, dest, date)
                passed = True
                while next_flight == "sleep":
                    time.sleep(10)
                    next_flight = query.query_flights(origin, dest, date)
            except:
                time.sleep(0.1)

        if tries == 5:
            raise Error("failed to get flight")
        return next_flight


trip = "ATL", {"SFO": 3, "LAX":4, "SEA":2}, ["2020-04-03", "2020-04-30"]
tsp = TSP(trip)
print(tsp.fromOrigin())
#print(query.query_flights('ATL', 'SFO', '2020-04-03'))

# prints all possible paths (comment out to avoid terminal clog)
print(tsp.paths)
print()

print("cheapest trip: ")
print(sorted(tsp.paths, key=itemgetter(0))[0])

