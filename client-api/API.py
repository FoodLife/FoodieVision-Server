from flask import Flask, request, jsonify, json, send_from_directory
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from foodiedb import foodie_db
from seefood import see_food
from PIL import Image
from io import BytesIO
from foodiedb_config import init_db
import numpy
import os
import base64
import subprocess
import random
import sys

sys.path.insert(0, '/home/ec2-user/Foodie')
app = Flask(__name__)
init_db(app)

ai = see_food()
ai.__init__()
mysql = MySQL()
mysql.__init__(app)


@app.route('/foodies/create_user', methods=['POST'])
def make_user():
	if request.method == 'POST':
		data = request.get_json()
		if "user_name" in data and "password" in data:
			conn = mysql.connect()
			result = foodie_db.create_user(conn, data["user_name"], data["password"])
			conn.close()
			if result > 0:
				return jsonify(success=1, result=result)
			return jsonify(success=0, result="username already in use")
		return jsonify(success=-1, result="invalid parameters")


@app.route('/foodies/login', methods=['POST'])
def login():
	if request.method == 'POST':
		data = request.get_json()
		if "user_name" in data and "password" in data:
			conn = mysql.connect()
			result = foodie_db.login(conn, data["user_name"], data["password"])
			conn.close()
			if result > 0:
				return jsonify(success=1,result=result)
			return jsonify(success=0,result="invalid login credentials")
		return jsonify(success=-1,result ="invalid parameters")


@app.route('/foodies/logout', methods=['POST'])
def logout():
	if request.method == 'POST':
		data = request.get_json()
		if "user_token" in data:
			conn = mysql.connect()
			result = foodie_db.logout(conn, data["user_token"])
			conn.close()
			if result > 0:
				return jsonify(success=1, result=result)
			return jsonify(success=0,result="no user to log out")
		return jsonify(success=-1, result="invalid parameters")

@app.route('/foodies/is_food',methods=['POST'])
def is_food():
	if request.method == 'POST':
		data = request.get_json()
		if "user_token" in data and "image" in data:
			ai_result = ai.is_food(data["image"])
			conn = mysql.connect()
			analysis = numpy.array(ai_result[0])
			is_food = 'Y' if ai_result[1] else 'N'
			result = foodie_db.create_picture(conn,data["user_token"], analysis[0,0], analysis[0,1], is_food)
			if not result  == 'exception':
				folder = 'images/'
				thumb_folder = folder + 'thumb/'
				file_path = folder + str(result[1]) + ".jpg"
				thumb_path = thumb_folder + str(result[1]) + "_thumb.jpg"
				if not os.path.isdir(folder):
					os.makedirs(folder)
				if not os.path.isdir(thumb_folder):
					os.makedirs(thumb_folder)
				image = Image.open(BytesIO(base64.b64decode(data["image"]))).convert('RGB')
				image.save(file_path)
				confidence=analysis.tolist()
 			        foodieScore = max(max(confidence))
				foodieScore=(foodieScore+5)/10
				image.resize((128, 128), Image.BILINEAR).save(thumb_path)

				confidence = analysis.tolist()
				foodieScore = max(max(confidence))
				foodieScore = (foodieScore + 5) / 10
				if result > 0:
					return jsonify(success=1, result=is_food, score=foodieScore)

				return jsonify(success=0, result= "invalid user")
			return jsonify(success=-1,result='db error')
		return jsonify(success=-1, result= "invalid parameters")

@app.route('/foodies/search',methods=(['POST']))
def search():
	if request.method == 'POST':
		data = request.get_json()
		conn = mysql.connect()
		search_params = {"user_token":False, "user_name":False,"creation_date_low":False,"creation_date_high":False,"is_food":False}
		if "user_token" in data:
			search_params["user_token"]=data["user_token"]
		if "user_name" in data:
			search_params["user_name"]=data["user_name"]
		if "creation_date_low" in data:
                        search_params["creation_date_low"]=data["creation_date_low"]
		if "creation_date_high" in data:
                        search_params["creation_date_high"]=data["creation_date_high"]
		if "is_food" in data:
                        search_params["is_food"]=data["is_food"]
		result = foodie_db.search(conn,search_params["user_token"],search_params["user_name"],search_params["creation_date_low"],search_params["creation_date_high"],search_params["is_food"])

		url = ["/" + str(x[0]) + ".jpg" for x in result]

		##search(connection,user_token,user_name,creation_date_low,creation_date_high,is_food)
		conn.close()
		return jsonify(result=url)

@app.route('/foodies/is_favorite', methods=['POST'])
def is_favorite():
	if request.method == 'POST':
                data = request.get_json()
                if "user_token" in data and "picture_id" in data:
                        conn = mysql.connect()
                        result = foodie_db.is_favorite(conn, data["user_token"], data["picture_id"])
			return jsonify(result)

@app.route('/hello', methods=('GET', 'POST'))
def hello():
	if request.method == 'POST' or request.method == 'GET':
		data = request.get_json()

		return jsonify(('HELLO WURLD ' + data["json"]), "test")

@app.route('/image/<path:image_name>')
def get_image(image_name):
    return send_from_directory('images', image_name)


if __name__ == "__main__":
	app.run(host='0.0.0.0')
