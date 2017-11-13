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
        #store picture locally and store filepath in sql database
        #return id number assigned to picture sql entry
        #then have AI process picture and store analysis in sql database.  
        #the second post request will then send the analysis results.
