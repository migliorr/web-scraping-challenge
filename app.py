from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

#Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Route to index.html page to render Mongo data to template
@app.route("/")
def index():

    # Find data
    mars_coll = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_coll=mars_coll)

# Route to trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_coll = scrape_mars.mars_news()
    mars_coll = scrape_mars.mars_image()
    mars_coll = scrape_mars.mars_weather()
    mars_coll = scrape_mars.mars_facts()
    mars_coll = scrape_mars.mars_hemispheres()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_coll, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
