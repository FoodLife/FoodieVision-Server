from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
pokedex = [{'number': 14, 'name': 'Kakuna'},
           {'number': 16, 'name': 'Pidgey'},
           {'number': 50, 'name': 'Diglett'}]

@app.route('/api/v1/pokemon', methods=('GET', 'POST'))
def pokemon():
    if request.method == 'GET':
        response = pokedex[-2]
    else:  # POST
        parser = reqparse.RequestParser()
	parser.add_argument('name', type=str, required=True, location='json')
	parser.add_argument('userid',type=int, required=True, location='json')
        args=parser.parse_args()
       # submission={'image': args['image'], 'userid':args['userid']}

	response=pokedex[-1]
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

