from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
import json
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yourpassword@yourhostname:5432/yourdb'

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Declare models 

class Station(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    code = db.Column(db.String, unique=True)
    longitude = db.Column(db.Text)
    latitude = db.Column(db.Text)
    url = db.Column(db.Text)
    active = db.Column(db.Integer)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    measurements = db.relationship('Measurement', backref='station')

    def __repr__(self):
        return '<Station %r>' % self.name

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    #stations = db.relationship('Station', backref='region')

    def __repr__(self):
        return '<Region %r>' % self.name

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Text)
    cs = db.Column(db.Text)
    fof2 = db.Column(db.Text)
    fof1 = db.Column(db.Text)
    mufd = db.Column(db.Text)
    foes = db.Column(db.Text)
    foe = db.Column(db.Text)
    hf2 = db.Column(db.Text)
    he = db.Column(db.Text)
    hme = db.Column(db.Text)
    hmf2 = db.Column(db.Text)
    hmf1 = db.Column(db.Text)
    yf2 = db.Column(db.Text)
    yf1 = db.Column(db.Text)
    tec = db.Column(db.Text)
    scalef2 = db.Column(db.Text)
    fbes = db.Column(db.Text)
    altitude = db.Column(db.Text)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))
    station_name = db.relationship('Station', foreign_keys=[station_id])
    def __repr__(self):
        return '<Measurement %r>' % self.id

#Generate marshmallow Schemas from your models using ModelSchema

class RegionSchema(ma.ModelSchema):
    class Meta:
        model = Region

region_schema = RegionSchema()
regions_schema = RegionSchema(many=True)

class StationSchema(ma.ModelSchema):
    class Meta:
        model = Station # Fields to expose
    region = ma.Nested(RegionSchema)

station_schema = StationSchema()
stations_schema = StationSchema(many=True)

class MeasurementSchema(ma.ModelSchema):
    class Meta:
        model = Measurement
    station = fields.Nested('StationSchema', only=['region', 'name', 'id', 'code', 'longitude', 'latitude',  'region_id'])

measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many=True)

#You can now use your schema to dump and load your ORM objects.


class RegionSchema(ma.ModelSchema):
    class Meta:
        model = Region

region_schema = RegionSchema()
regions_schema = RegionSchema(many=True)

class StationSchema(ma.ModelSchema):
    class Meta:
        model = Station # Fields to expose
    region = ma.Nested(RegionSchema)

station_schema = StationSchema()
stations_schema = StationSchema(many=True)

class MeasurementSchema(ma.ModelSchema):
    class Meta:
        model = Measurement
    station = fields.Nested('StationSchema', only=['region', 'name', 'id', 'code', 'longitude', 'latitude',  'region_id'])

measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many=True)

#You can now use your schema to dump and load your ORM objects.

#Returns latest measurements for all stations in JSON
@app.route("/stations.json" , methods=['GET'])
def stationsjson():

    subq = (db.session.query(db.func.max(Measurement.id).label("max_id")).group_by(Measurement.station_id)).subquery()

    qry = (db.session.query(Measurement).join(subq, and_(Measurement.id == subq.c.max_id)))

    db.session.close()
    
    result = measurements_schema.dump(qry)

    return jsonify(result.data)

@app.route("/", methods=['GET'])
def static_stations():
      index_path = os.path.join(app.static_folder, 'index.html')
      return send_file(index_path)
      #return render_template('stations.html')
                            #tables=[table.to_html(classes='stationTable', escape=False)],
                            #latestmes = latestmes

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=80)
