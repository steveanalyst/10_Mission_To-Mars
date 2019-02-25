# Dependencies 
from flask import Flask, render_template, redirect 
import pymongo
import scrape_mars
import os




# Create an instance 
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars.drop()




# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_data = db.mars_data.find_one()    

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrape functions
    mars_data = db.mars_data
    mars_d = scrape_mars.mars_news_scrape()
    mars_d = scrape_mars.mars_feature_image_scrape()
    mars_d = scrape_mars.mars_facts_scrape()
    mars_d = scrape_mars.mars_weather_scrape()
    mars_d = scrape_mars.mars_hemispheres_scrape()
    mars_data.update({}, mars_d, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)