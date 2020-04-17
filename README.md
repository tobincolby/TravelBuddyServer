# TravelBuddy Server Guide
This is how to setup and configure the server for TravelBuddy locally

## Important Files
1. alg4.py contains the code that actually runs the TSP algorithm
2. query.py houses all code that is used to query various 3rd party APIs
3. TravelBuddyServer.py houses all of the endpoints for the react native application

## Requirements
1. Python3
2. MySQL 8.0
3. public_config.py and travelbuddy-firebase.json files provided in submission

## Installation

1. Create a new Python3 Virtual Environment
2. Install pip requirements from requirements.txt

```bash
pip install -r requirements.txt
```

3. Drop the "public_config.py" file from Canvas and "travelbuddy-firebase.json" into the same directory as TravelBuddyServer.py.

## Database Setup

1. Run the following command with the file "TravelBuddyDB.sql"

```bash
mysql -u user_name -p TravelBuddyLocal < TravelBuddyDB.sql
```

2. Update the public_config.py file to include your MySQL username and password to allow the application access to MySQL.


## How to run Server

1. Activate the virtual environment
2. Setup Flask

```bash
export FLASK_APP="TravelBuddyServer.py"
```

3. Run Flask Server
```bash
flask run
```

4. Now you may run the React Native TravelBuddy Application