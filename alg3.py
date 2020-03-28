from datetime import datetime
from datetime import timedelta
import sys

class TSP:

    # path = []
    # paths = []
    # global_mincost = sys.maxsize
    # visited = []
    # adj = []
    def __init__(self, trip):
        self.paths = []

        self.origin = trip[0]
        self.cities = trip[1]
        self.daterange = trip[2]

        self.adj = [[[] for x in range(len(self.cities)+1)] for x in range(len(self.cities)+1)]

        # TRACKS ORDER OF CITIES IN THE ADJ MATRIX
        #   for use if we remove the origin/dest from the tuple we put in the matrix
        self.cityInd = {}
        i = 0
        self.cityInd[self.origin] = i
        for city in self.cities:
            i += 1
            self.cityInd[city] = i
        # print(getCityInd)
        # print()



    def setup(self):
        a = (100, "ATL", "SFO", "2019-04-25")
        #a = {"price":100, "origin": "ATL", "destination":"SFO", "departure_date": "2019-04-25"} #considering # of NIGHTS
        b = (200, "SFO", "LAX", "2019-04-28")
        c = (400, "LAX", "SEA", "2019-05-02")
        d = (7, "SEA", "ATL", "2019-05-04")

        e = (50, "ATL", "SFO", "2019-04-28")
        f = (78, "SFO", "LAX", "2019-05-01")
        g = (92, "LAX", "SEA", "2019-05-04")
        h = (300, "SEA", "ATL", "2019-05-06")

        i = (50, "ATL", "SFO", "2019-04-28")
        j = (78, "SFO", "LAX", "2019-05-08")
        k = (92, "LAX", "SEA", "2019-05-12")
        l = (8, "SEA", "ATL", "2019-05-13")

        m = (50, "ATL", "LAX", "2019-04-28")
        n = (78, "LAX", "SEA", "2019-05-02")
        o = (92, "SEA", "SFO", "2019-05-04")
        p = (300, "SFO", "ATL", "2019-05-07")

        flights_tup = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]
        flights = []
        for flight in flights_tup:
            cur = {}
            cur["price"] = flight[0]
            cur["origin"] = flight[1]
            cur['destination'] = flight[2]
            cur['departure_date'] = datetime.strptime(flight[3], "%Y-%m-%d")
            flights.append(cur)

        # LOAD ADJ
        for flight in flights:
            #adj[getCityInd[flight['origin']]][getCityInd[flight['destination']]].append((flight['price'], flight['departure_date']))
            self.adj[self.cityInd[flight['origin']]][self.cityInd[flight['destination']]].append((flight['origin'], flight['destination'], flight['price'], flight['departure_date']))

    def fromOrigin(self):
        for i in self.adj[0]:
            if i != []:
                for flight in i:
                    self.getNext(flight, [self.origin, flight[1]], [flight], flight[2])


    def getNext(self, prev, visited, path, price):
        if len(visited) == len(self.cities)+2: # path complete
            self.paths.append((price, path))
            return

        for i in self.adj[self.cityInd[prev[1]]]:
            if i != []:
                for flight in i:
                    isNewCity = flight[1] not in visited
                    notDoneYet = len(visited) <= len(self.cities)
                    readyToGoHome = (len(visited) == len(self.cities)+1)
                    flightGoesHome = flight[1] == self.origin
                    if (isNewCity and notDoneYet) or (readyToGoHome and flightGoesHome):
                        rightNumDays = flight[3] == prev[3] + timedelta(self.cities[flight[0]])
                        if rightNumDays:
                            visited.append(flight[1])
                            path.append(flight)
                            price += flight[2]
                            self.getNext(flight, visited, path, price)


trip = "ATL", {"SFO": 3, "LAX":4, "SEA":2}, ["2019/04/25", "2019/05/20"]
tsp = TSP(trip)
tsp.setup()
tsp.fromOrigin()
print(min(tsp.paths))

