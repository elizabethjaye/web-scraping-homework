#Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


#Set up flask
app = Flask(__name__)

#Set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
	dictionary = mongo.db.dictionary.find_one()
	return render_template("index.html", dictionary=dictionary)

@app.route("/scrape")
def scraper():
	dictionary = mongo.db.dictionary
	dictionary_data = scrape_mars.scrape()
	dictionary.update({}, dictionary_data, upsert=True)
	return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)