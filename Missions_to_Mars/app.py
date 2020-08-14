from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)
#mongo.mars_db.mars_data_collection.drop()

@app.route("/")
def index():
    mars_data = mongo.db.mars_data_collection.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data_collection = mongo.db.mars_data_collection
    mars_data = scrape_mars.scrape()
    mars_data_collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=False)