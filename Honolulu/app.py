# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
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
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
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
def stations():

    # Run query
    query = session.query(Measurement.station).distinct().all()

    session.close()

    # Convert to normal list
    station_list = list(np.ravel(query))

    return jsonify(station_list)


# TOBS ROUTE
@app.route('/api/v1.0/tobs')
def tobs():

    # Run query
    query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281', Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23').all()
    
    session.close()

    # Convert to normal list
    tobs_list = list(np.ravel(query))

    return jsonify(tobs_list)


# START DATE ROUTE
@app.route('/api/v1.0/<start>')
def temps_start(start):

    # Query
    query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
    .filter(Measurement.date>=start) \
    .all()

    session.close()

    # Convert to list
    temps_start_list = list(np.ravel(query))

    return jsonify(temps_start_list)

# START-END DATE ROUTE
@app.route('/api/v1.0/<start>/<end>')
def temps_start_end(start, end):

    # Query
    query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
    .filter(Measurement.date>=start, Measurement.date<=end) \
    .all()

    session.close()

    # Convert to list
    temps_start_end_list = list(np.ravel(query))

    return jsonify(temps_start_end_list)


#################################################
# RUN APP
#################################################
if __name__ == "__main__":
    app.run(debug=True)