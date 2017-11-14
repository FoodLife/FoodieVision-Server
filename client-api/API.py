from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
import base64
import subprocess

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
        filename="id"#pic id ret from database
        filepath="userid"#user id ret from database
        
        os.makedirs(filepath+"/")
        os.chdir(filepath+"/")
        f= open(filename,"w+")
        f.write(base64.b64decode(submission['image']))
        filepath=filepath+"/"+filename
        #store filepath in database
            

        #then have AI process picture and store analysis in sql database.  
        
        #the second post request will then send the analysis results.