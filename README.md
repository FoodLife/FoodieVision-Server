# foodievision-server
~~this is just a basic hello world, so don't get too excited~~
This API/Database is designed to run on an ec2 instance with the user ec2-user
using python-flask and mysql

## server currently is running on an ec2 instance at 34.232.146.205

## to get the server running do the following:
dependencies `sudo yum install mysql
start the flask serever using `sudo FLASK_APP=API.py python -m flask run --host=0.0.0.0 --port=5000`

The application will need to know the exact ip address of the server, currently it is configured to run on our ec2 instance.

The sever uses json data passed through post requests, here is an example post request to login 
```
POST /foodies/login HTTP/1.1

Host: 34.232.146.205:5000
User-Agent: curl/7.43.0
Accept: */*
Content-Type: application/json
Content-Length: 32
{"user_name":"test","password":"pass"}
```
