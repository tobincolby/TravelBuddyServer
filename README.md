# TravelBuddy Server Guide
This is how to setup and configure the server for TravelBuddy locally

## Installation

1. Create a new Python3 Virtual Environment
2. Install pip requirements from requirements.txt

```bash
pip install -r requirements.txt
```

3. Drop the "public_config.py" file from Canvas and "travelbuddy-firebase.json" into the main project root.

##Database Setup

1. Run the following command with the file "TravelBuddyDB.sql"

```bash
mysql -u user_name -p TravelBuddyLocal < TravelBuddyDB.sql
```

2. Update the public_config.py file to include the correct credentials for the system to access the DB.


## How to run Server

1. Activate the virtual environment
2. SetUp Flask

```bash
export FLASK_APP="TravelBuddyServer.py"
```

3. Run Flask Server
```bash
flask run
```