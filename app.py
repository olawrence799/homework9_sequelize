from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurements
Station = Base.classes.stations
session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precip():
    results = session.query(Measurement).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    all_precip = []
    for record in results:
        precip_dict = {}
        precip_dict['date'] = record.date
        precip_dict['tobs'] = record.tobs
        all_precip.append(precip_dict)
        
    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def station():
    results_station = session.query(Station.station).all()
    results_station = [record.station for record in results_station]
    return jsonify(results_station)

@app.route("/api/v1.0/tobs")
def tobs():
    results_tobs = session.query(Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    results_tobs = [record.tobs for record in results_tobs]
    return jsonify(results_tobs)



start_date = '2017-01-01'
end_date = '2017-01-14'

@app.route("/api/v1.0/start")
def start():
    results_start = session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= (start_date)).all()
    return jsonify(results_start)

@app.route("/api/v1.0/startend")
def end():
    results_start_end = session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date.between(start_date, end_date)).all()
    return jsonify(results_start_end)

if __name__ == '__main__':
    app.run(debug=True)