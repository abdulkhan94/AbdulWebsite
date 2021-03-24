from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

'''video_put_args = reqparse.RequestParser()
video_put_args.add_argument("year", type=int, help="add year of video", required=True)
video_put_args.add_argument("country", type = str, help="add country of video", required=True)
'''

class Movies(db.Model):
    video_id = db.Column(db.String(100), primary_key = True)
    year = db.Column(db.Integer)
    country = db.Column(db.String(100))
    
    def __init__(self, _video_id, _year, _country):
        self.video_id = _video_id
        self.year = _year
        self.country = _country
        
        
class Video(Resource):
    def get(self, video_id):
        record = Movies.query.filter_by(video_id = video_id).first()
        if record == None:
            abort(404, message = "video_id not found")
        else:
            return {"video_id": record.video_id, "year":record.year, "country": record.country},200
        
     
    def put(self, video_id):
        args = request.form
        print(args)
        mvs = Movies(video_id, args["year"], args["country"])
        db.session.add(mvs)
        db.session.commit()
        return 202        

    
    def delete(self, video_id):
        record = Movies.query.filter_by(video_id=video_id).first()
        if record == None:
            abort(404, message = "video_id not found")
        else:
            Movies.query.filter_by(video_id=video_id).delete()
            db.session.commit()
            return 200
        
        
    
api.add_resource(Video, "/video/<string:video_id>")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)