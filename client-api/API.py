rom flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
api.add_resource(foodievision, '/api/v1/foodievision')

class foodievision(Reasource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=str, required=True,location='json')
        parser.add_argument('userid',type=str, required=True, location='json')
        args=parser.parse_arge(strict=True)
        submission={'image': args['image'], 'userid':args['userid']}
        #check if it is database already, maybe not if we don't care
        #
