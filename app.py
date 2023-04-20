from flask import Flask, render_template
from pymongo import MongoClient
import requests
import os
from datetime import datetime, time
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# connect to MongoDB database
client = MongoClient("mongodb+srv://sahilpatel:world@cluster.rvmuxrr.mongodb.net/?retryWrites=true&w=majority")
db = client["Countries"]
collection = db["countries"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/area/chart")
def area():
    countries = list(collection.find().sort("area", -1).limit(10))
    for country in countries:
        country["area"] = float(country["area"])
    return render_template("area-chart.html", countries=countries)

@app.route("/population/chart")
def population():
    # retrieve data from MongoDB collection and sort by population
    countries = list(collection.find())
    return render_template("population-chart.html", countries=countries)

# define the timezone you want to use
tz = timezone('America/Toronto')

# create a scheduler object
scheduler = BackgroundScheduler(timezone=tz)

# define the task to be scheduled
def collection_update():
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents.")  # Add a print statement to check how many documents were deleted

    # fetch data from REST Countries API
    print("Fetching data from REST Countries API...")  # Add a print statement to check if data is being fetched
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    data = response.json()

    # insert data into MongoDB collection
    print("Inserting new data...")  # Add a print statement to check if new data is being inserted
    for entry in data:
        collection.insert_one(entry)
    print(f"Inserted {len(data)} documents.")  # Add a print statement to check how many documents were inserted

# add the task to the scheduler
scheduler.add_job(collection_update, 'interval', hours=24, start_date=datetime.combine(datetime.now(tz).date(), time(hour=0, minute=0, second=0, microsecond=0)))

if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # Add this condition
    scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)