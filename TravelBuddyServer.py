from flask import Flask
from flaskext.mysql import MySQL
from flask import jsonify, json
from flask import request
from alg4 import TSP
import query
import firebase_admin
import requests
from firebase_admin import credentials, auth
from operator import itemgetter
import datetime
import public_config
app = Flask(__name__)

credential = credentials.Certificate("./travelbuddy-firebase.json")

firebase_app = firebase_admin.initialize_app(credential=credential)
_verify_password_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword'


mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = public_config.db_user
app.config['MYSQL_DATABASE_PASSWORD'] = public_config.db_password
app.config['MYSQL_DATABASE_DB'] = public_config.db_name
app.config['MYSQL_DATABASE_HOST'] = public_config.db_host

mysql.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register/', methods=["POST"])
def register_page():

    error = ''
    try:
        if request.method == "POST":
            jsonReq = request.get_json()
            name = jsonReq['name']
            email = jsonReq['email']
            phone = jsonReq['phone']
            password = jsonReq['password']

            user = auth.create_user(display_name=name, email=email, phone_number=phone, password=password)
            token = auth.create_custom_token(user.uid)

            return json.jsonify({'success':1, 'token': token.decode('utf-8'), 'email': email, 'name': name, 'phone': phone})
        return json.jsonify({'success':0})


    except Exception as e:
        #flash(e)
        print ("error: " + str(e))
        return json.jsonify({'success':0})

@app.route('/login/', methods=["POST"])
def login_page():
    error = ''
    try:
        if request.method == "POST":
            jsonReq = request.get_json()
            print(jsonReq)
            email = jsonReq['email']
            password = jsonReq['password']
            body = {'email': email, 'password': password}
            params = {'key': public_config.firebase_api_key}

            resp = requests.request('post', _verify_password_url, params=params, json=body)
            if bool(resp.json().get('registered')):
                user = auth.get_user_by_email(email)
                return json.jsonify({'success': 1, 'email': user.email, 'name': user.display_name, 'uid': user.uid})
            else:
                return json.jsonify({'success': 0})

        return json.jsonify({'success': 0})


    except Exception as e:
        # flash(e)
        print("error: " + str(e))
        return json.jsonify({'success': 0})

@app.route('/flights')
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
    response = dict()
    response["success"] = 1
    response["price"] = cheapestTrip[0]
    response["flights"] = cheapestTrip[1]
    print(cheapestTrip)
    return jsonify(response)

@app.route('/addTrip/', methods=['POST'])
def add_trips_handler():
    cmd = ''
    try:
        if request.method == "POST":
            reqJson = request.get_json()
            user_email = 'sample@gmail.com'
            user_trip = 'MY TRIP'
            date = datetime.date.today()
            dateObj = datetime.datetime.strptime(str(date), '%Y-%m-%d')
            date = dateObj.strftime('%Y-%m-%d')

            if "email" in reqJson:
                user_email = str(reqJson['email'])
            if "trip" in reqJson:
                user_trip = json.dumps(reqJson['trip'])[1:-1].replace("'", "\\'")

            if "startDate" in reqJson:
                date = str(reqJson['startDate'])
                print(date)
            # user_email = request.values.get('email', default="tobincolby@gmail.com", type=str)
            # user_trip = request.values.get('trip', default="MY TRIP", type=str)
            conn = mysql.connect()
            cursor = conn.cursor()
            cmd = "INSERT INTO flights (email, flight_info, start_date) VALUES ('{}','{}', '{}')".format(user_email, user_trip, date)
            cursor.execute(cmd)
            response = {}
            # response['trip'] = str(user_trip)
            response['email'] = user_email
            response['success'] = 1
            conn.commit()
            return json.jsonify(response)
        return json.jsonify({'success':0})
    except Exception as e:
        #flash(e)
        print ("error: " + str(e))
        return json.jsonify({'success':0, 'error': str(e), 'cmd': cmd})


@app.route('/trips/', methods=["GET"])
def trips_handler():
    user_email = request.args.get('email', default="tobincolby@gmail.com", type=str)

    conn = mysql.connect()
    cursor = conn.cursor()
    date = datetime.date.today()
    dateObj = datetime.datetime.strptime(str(date), '%Y-%m-%d')
    date = dateObj.strftime('%Y-%m-%d')
    cursor.execute('SELECT * from flights WHERE email="{}" AND start_date >= "{}"'.format(user_email, date))
    row = cursor.fetchone()
    trips = []
    while row is not None:
        trips.append(row[2])
        row = cursor.fetchone()

    response = {}
    response['flights'] = trips
    response['success'] = 1
    response['email'] = user_email

    return json.jsonify(response)


@app.route('/restaurants/getByCity', methods=["GET"])
def restaurants_handler():
    destinations = []
    num_destinations = int(request.args.get('destNum'))
    for i in range(num_destinations):
        destinations.append(request.args.get('dest' + str(i)))
    businesses = []
    for destination in destinations:
        businesses.extend(query.run_yelp_query(query.searchQuery(location=destination))["data"]["search"]["business"])

    return json.jsonify({"business": businesses})

    # destination = request.args.get('dest', default="JFK", type=str)
    # cityInfo = Query.runLocationQuery(destination, ["cityname"])
    # return json.jsonify(Query.run_yelp_query(Query.searchQuery(location=cityInfo[0]))["data"]["search"])


if __name__ == '__main__':
    app.run()
