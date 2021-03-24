from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import requests
import json


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    userid = db.Column(db.String(100), primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    def __init__(self, _userid, _username, _email):
        self.userid = _userid
        self.username = _username
        self.email = _email

                
class Weather(Resource):
    def get(self, city_id, year, month, day):
        r = requests.get(f'https://www.metaweather.com/api/location/{city_id}/{year}/{month}/{day}')
        data = r.json()
        current_weather = data[0]['weather_state_name']
        resp = {'Current Weather':current_weather}
        return resp, 200
    
api.add_resource(Weather, "/weather/<string:city_id>/<string:year>/<string:month>/<string:day>")
    
    
class Persons(Resource):            
    def put(self, userid):
        args = request.form
        p = Users(userid, args['username'], args['email'])
        db.session.add(p)
        db.session.commit()
        return 200
    
    
    def get(self, userid):
        side = Users.query.all()
        em_list = [x.email for x in side]
        print(em_list)
        record = Users.query.filter_by(userid = userid).first()
        return {"userid":record.userid, "username":record.username, "email":record.email}, 200
    
    
    def delete(self, userid):
        record = Users.query.filter_by(userid = userid).delete()
        db.session.commit()
        return 200
        
            
    
api.add_resource(Persons, "/person/<string:userid>")

    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)