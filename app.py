###################################################################################################
# Step 2 - MongoDB and Flask Application
#
#   Use MongoDB with Flask templating to create a new HTML page that displays all of the 
#   information that was scraped from the URLs above.
#
#       1. Start by converting your Jupyter notebook into a Python script called scrape_mars.py with 
#           a function called scrape that will execute all of your scraping code from above and  
#           return one Python dictionary containing all of the scraped data.
#
#       2. Next, create a route called `/scrape` that will import your scrape_mars.py script and 
#           call your scrape function.
#           - Store the return value in Mongo as a Python dictionary.
#       
#       3. Create a root route `/` that will query your Mongo database and pass the mars data into 
#           an HTML template to display the data.
#       
#       4. Create a template HTML file called index.html that will take the mars data dictionary 
#           and display all of the data in the appropriate HTML elements. Use the following as 
#           a guide for what the final product should look like, but feel free to create your own design.
###################################################################################################
# Import Dependencies 
from flask import Flask, render_template
import scrape_mars
import pymongo

#################################################
# Flask and Mongo Setup
#################################################
app = Flask(__name__)

# Setup mongo connection
conn = "mongodb://127.0.0.1:27017"
client = pymongo.MongoClient(conn)

# Connect to mongo db
db = client.mars_db

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    # Find all the items in the db and set it to a variable
    mars_data = list(db.mars_db.find())
    print(mars_data)

    # Render an index.html template and pass it the data retrieved from the database
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
# Import scrape function from scrape_mars.py that will execute all your scraping code 
# and return one Python dictionary containing all of the scraped data.
def scrape():

    # Initialize mars_db
    mars_db = db.mars_db

    # Re-scrape mars data
    dict_of_scraped = scrape_mars.scrape()

    # Insert into MongoDB
    mars_db.update(
        {},
        dict_of_scraped,
        upsert=True
    )

    # Print MongoDB Data
    from pprint import pprint
    mars_data = db.mars_db.find()
    for data in mars_data:
        pprint(data)

    return ("Done")


if __name__ == "__main__":
    app.run(debug=True)
