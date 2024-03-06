# Import the dependencies.

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/ezrellemyhre-hager/Documents/GitHub/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to my app module Hawaii data page!<br>"
        f"<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Returns the JSON representation of precipitation analysis over the past 12 months. (2016-2017)<br>"
        f"/api/v1.0/stations - Returns a JSON list of stations from the dataset.<br/>"
        f"/api/v1.0/tobs - Returns a JSON list of temperature observations for the previous year on the most active station (USC00519281).<br>"
        f"/api/v1.0/<start> - Returns a JSON list of temperature observations for the previous year.<br>"
        f"/api/v1.0/<start>/<end> - Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    # get most recent date 
    most_recent_date_string = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent_date = dt.datetime.strptime(most_recent_date_string, "%Y-%m-%d")
    
    # Calculate the date one year from the last date in data set.
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precipitation_data_tuples = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()

    session.close()

    precipitation_data = []

    for date, prcp in precipitation_data_tuples:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        precipitation_data.append(prcp_dict)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    
    station_list_tuples = session.query(station.station, station.name).all()
    
    session.close()

    station_list = []

    for station_number, name in station_list_tuples:
        station_dict = {}
        station_dict["station"] = station_number
        station_dict["name"] = name
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    # get most recent date 
    most_recent_date_string = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent_date = dt.datetime.strptime(most_recent_date_string, "%Y-%m-%d")
    
    # Calculate the date one year from the last date in data set.
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data for more active station in the past 12 months
    temperature_data = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= one_year_ago).all()
    
    session.close()

    # Extract temperature data 
    temperatures = [temp[0] for temp in temperature_data]

    return temperatures

@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    
    session = Session(engine)
    
    temp_tuples = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    
    session.close()
    
    temp_stats = []
    
    for min, avg, max in temp_tuples:
        temp_dict = {}
        temp_dict["min_temp"] = min
        temp_dict["avg_temp"] = avg
        temp_dict["max_temp"] = max
        temp_stats.append(temp_dict)

    # Return the JSON representation of the temperature statistics
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):
    session = Session(engine)
    
    # Perform the query to get TMIN, TAVG, TMAX between start and end dates
    temp_tuples = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()
    
    # Convert the query results to a list of dictionaries
    temp_stats = []
    
    for min, avg, max in temp_tuples:
        temp_dict = {}
        temp_dict["min_temp"] = min
        temp_dict["avg_temp"] = avg
        temp_dict["max_temp"] = max
        temp_stats.append(temp_dict)
    
        
    # Return the JSON representation of the temperature statistics
    return jsonify(temp_stats)


if __name__ == "__main__":
    app.run(debug=True)
