# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# HOMEPAGE
@app.route('/')
def welcome():
    """List api routes"""
    return (
        f'available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs'
        )

# PRECIPITATION ROUTE
@app.route('/api/v1.0/precipitation')
def prcp():

    # Query database for precipitation info
    query = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23').all()
    
    session.close()

    # Create dictionary from this query and append to a list of dictionaries
    all_prcp = []
    for date, prcp in query:
        dict = {}
        dict['date'] = date
        dict['prcp'] = prcp
        all_prcp.append(dict)

    return jsonify(all_prcp)   

# STATION ROUTE
@app.route('/api/v1.0/stations')
def station():

    stations = session.query(Measurement.station).distinct()
    return jsonify(stations)


# TOBS ROUTE
# @app.route('/api/v1.0/tobs')



#################################################
# RUN APP
#################################################
if __name__ == "__main__":
    app.run(debug=True)