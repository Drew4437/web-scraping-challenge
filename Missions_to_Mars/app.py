from flask import Flask, render_template
# Import scrape_mars
import scrape_mars
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017/mission_to_mars'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Set route
@app.route("/")
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape 
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    return render_template('index.html', mars=mars_data)

if __name__ == "__main__":
    app.run(debug=True) 