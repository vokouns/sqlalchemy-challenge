# Import the dependencies.
import datetime as dt
import numpy as np 

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate Analysis API!<br>"
        f"Available Routes<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/temp/start<br>"
        f"/api/v1.0/temps/end<br>"
        f"<p>'start' and 'end' date should be in format MMDDYYYY.</p>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).all()

    session.close()

    precip = {date: prcp for date, prcp in precip}
    return jsonify(precip)



@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year).all()
    
    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/start")

# @app.route("/api/v1.0/temps/end")

# @app.route("")
# 


if __name__ == "__main__":
    app.run(debug=True)