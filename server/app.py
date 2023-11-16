#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API"
        }
        return make_response(response_dict, 200)

api.add_resource(Home, "/")

class Newsletters(Resource):
    def get(self):
        responses = [item.to_dict() for item in Newsletter.query.all()]
        return make_response(responses, 200)
    
    def post(self):
        new_record = Newsletter(
            title=request.get_json()["title"],
            body=request.get_json()["body"],
        )

        db.session.add(new_record)
        db.session.commit()

        return make_response(new_record.to_dict(), 201)
    
api.add_resource(Newsletters, '/newsletters')

class NewslettersById(Resource):
    def get(self, id):
        found = Newsletter.query.filter_by(id = id).first().to_dict()
        return make_response(found, 200)

api.add_resource(NewslettersById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
