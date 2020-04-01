from flask import Flask
from flask import jsonify
from flask import request
from alg4 import TSP
from operator import itemgetter
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getflights')
def get_flights():
    origin = request.args.get('origin')
    destination_number = int(request.args.get('destinationNumber'))
    start_date = request.args.get('startDate')
    destinations = dict()
    for i in range(destination_number):
        destinations[request.args.get('destination' + str(i))] = int(request.args.get('duration' + str(i)))

    trip = origin, destinations, [start_date, start_date]
    print(trip)
    tsp = TSP(trip)

    tsp.fromOrigin()

    cheapestTrip = sorted(tsp.paths, key=itemgetter(0))[0]

    return jsonify(cheapestTrip)


if __name__ == '__main__':
    app.run()
