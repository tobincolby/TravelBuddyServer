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
        self.already_queried = dict()


        tl = 0
        for city in trip[1]:
            tl += trip[1][city]
        self.triplength = tl


    def fromOrigin(self):
        # for i in range(self.daterange_size - self.triplength + 1):
        flightdate_str = datetime.strftime(self.startdate + timedelta(0), '%Y-%m-%d')
        for city in self.cities:
            if (self.origin, city, flightdate_str) in self.already_queried:
                flight = self.already_queried[(self.origin, city, flightdate_str)]
            else:
                flight = self.getFlight(self.origin, city, flightdate_str)
                if flight == "":
                    continue
                self.already_queried[(self.origin, city, flightdate_str)] = flight
            self.getNext(flight, [self.origin, city], [flight], flight['price'])


    def getNext(self, prev, visited, path, price):
        # when you got to this city
        arrived_on = datetime.strptime(prev['departure_date'], "%Y-%m-%d")

        # when you need to leave the city, in str form (for the flights alg)
        leave_on = datetime.strftime(arrived_on + timedelta(self.cities[prev['destination_code']]), "%Y-%m-%d")

        # trip is over / need to go home
        if len(visited) == len(self.cities)+1:
            if (prev['destination_code'], self.origin, leave_on) in self.already_queried:
                next_flight = self.already_queried[(prev['destination_code'], self.origin, leave_on)]
            else:
                next_flight = self.getFlight(prev['destination_code'], self.origin, leave_on)
                if next_flight == "":
                    return
                self.already_queried[(prev['destination_code'], self.origin, leave_on)] = next_flight
            path.append(next_flight)
            price += next_flight['price']
            self.paths.append((price, path))
            return

        # go to new city
        for city in self.cities:
            if (city not in visited) or (len(visited) == len(self.cities)+1 and city == self.origin):
                if (prev['destination_code'], city, leave_on) in self.already_queried:
                    next_flight = self.already_queried[(prev['destination_code'], city, leave_on)]
                else:
                    next_flight = self.getFlight(prev['destination_code'], city, leave_on)
                    if next_flight == "":
                        continue
                    self.already_queried[(prev['destination_code'], city, leave_on)] = next_flight
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
                if next_flight == "":
                    return ""
                passed = True
                while next_flight == "sleep":
                    time.sleep(10)
                    next_flight = query.query_flights(origin, dest, date)
                    if next_flight == "":
                        return ""
            except:
                time.sleep(0.1)

        if tries == 5:
            return ""
        return next_flight


# trip = "ATL", {"ORD": 3, "LAX":2, "SEA":2, "TPA": 2, "PHL": 2}, ["2020-04-10", "2020-05-01"]
# tsp = TSP(trip)
# start = datetime.now()
# tsp.fromOrigin()
# print(sorted(tsp.paths, key=itemgetter(0))[0])
# end = datetime.now()
# print((end - start).total_seconds())
#print(query.query_flights('ATL', 'SFO', '2020-04-03'))
#
# # prints all possible paths (comment out to avoid terminal clog)
# print(tsp.paths)
# print()
#
# print("cheapest trip: ")
# print(sorted(tsp.paths, key=itemgetter(0))[0])
