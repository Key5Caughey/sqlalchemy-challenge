# Import the dependencies.
# Design climate app
#Import dependencies

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper# create a session


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Flask Setup
from flask import Flask, jsonify
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
@app.route ("/")
def welcome():
    output = """Server recieved request for 'Home' page...<br />
    <h1>Welcome to my home page!</h1>
     Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    <br/>
     Temp Observation from most active station:<br/>
    /api/v1.0/tobs<br/>
    <br/>
     Enter start date at end of URL:<br/>
    /api/v1.0/temps/<start><br/>
     Enter /start date/end date at end of URL:<br/>
    /api/v1.0/temps/<start>/<end<br/>
    <br/>
    <br/>
    <h2>Enjoy your Hawaiian vacation !</h2>
    <br/>
    <img src="https://pixabay.com/photos/maui-sunset-hawaii-2729958/" alt="Maui Sunset">


"""
    return output

    
        
#of dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp). \
                            filter(Measurement.date >= prev_year).all()
    session.close()
    precip = {date: prcp for date , prcp in precipitation}
    return jsonify(precip)
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():

    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= prev_year).all()
    
    session.close()
    temps = list(np.ravel(results))

    return jsonify(temps)

@app.route("/api/v1.0/temps/<start>")
@app.route("/api/v1.0/temps/<start>/<end>")
def stats(start = None, end = None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%Y-%m-%d")   #2016-8-23
        results = session.query(*sel). \
            filter(Measurement.date >= start).all()
        
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    results = session.query(*sel). \
            filter(Measurement.date >= start). \
            filter(Measurement.date <=end).all()
    
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps)



if __name__ == "__main__":
    app.run(debug=True)

