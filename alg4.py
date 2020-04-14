#in travelbuddy

import query

import time
from datetime import datetime
from datetime import timedelta
import sys
from operator import itemgetter

class TSP:

    def __init__(self, trip):
        """
        Args:
            trip: a list of arguments:
                0: origin city
                1: dictionary of destinations mapped to number of days to spend at that destination
                2: list of length 2 containing start and end dates for time region

        Objective:
            initialize class variables

        Returns:
            None
        """

        #paths is the array of all possible trips to the destination
        self.paths = []

        self.origin = trip[0]
        self.cities = trip[1]
        self.startdate = datetime.strptime(trip[2][0], "%Y-%m-%d")
        self.enddate = datetime.strptime(trip[2][1], "%Y-%m-%d")

        self.daterange_size = (self.enddate - self.startdate).days
        self.already_queried = dict() #stores queries so we don't have to
            # make redundant API calls

        tl = 0
        for city in trip[1]:
            tl += trip[1][city]
        self.triplength = tl #total number of days of trip


    def fromOrigin(self):
        """
        Args:
            None

        Objective:
            loop through every possible start date in range of travel dates
            for each start date, starting from the departure city, run the
                recursive traveling algorithm on each possible 1st city in
                trip

        Returns:
            None
        """

        for i in range(self.daterange_size - self.triplength + 1):
            flightdate_str = datetime.strftime(self.startdate + timedelta(i), '%Y-%m-%d')
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
        """
        Args:
            prev: the previous city you visited / city you are "coming from"
            visited: list of cities (airport codes) you have already visited so far on your trip
            path: your current itinerary thus far into the trip, including all the flight info
                you would need to book
            price: the cumulative price of the path thus far

        Objective:
            recursively bounce through every possible combination of flights from the original "prev"
                that was passed in from fromOrigin

        Returns:
            None
        """

        # when you got to this city
        arrived_on = datetime.strptime(prev['departure_date'], "%Y-%m-%d")

        # when you need to leave the city, in str form (for the flights alg)
        leave_on = datetime.strftime(arrived_on + timedelta(self.cities[prev['destination_code']]), "%Y-%m-%d")

        # case when trip is over and you need to go home (not to a location in 'cities')
        #   (this case places the completed path into the class paths object and
        #   returns back up the recursive stack)
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

        # go to a new city/destination (where the recursion happens)
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
        """
        Args:
            origin: the airport code of the flight origin
            dest: the airport codde of the flight destination
            date: the date of flight departure

        Objective:
            call the API to get information about the cheapest flight between
            the 2 destinations on the specified date, or inform that no such
            flight exists

        Returns:
            next_flight: flight object of the "next" flight in the current
                possible itinerary
        """

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

                # query.py is set to return "sleep" if the api call fails due
                # to us pinging it to frequently. The code sleeps for a little
                # and tries the API again after some time
                while next_flight == "sleep":
                    time.sleep(10)
                    next_flight = query.query_flights(origin, dest, date)
                    if next_flight == "":
                        return ""

            # hits the exception and sleeps if the query fails entirely
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

