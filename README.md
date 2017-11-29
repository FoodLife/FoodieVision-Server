# foodievision-server
~~this is just a basic hello world, so don't get too excited~~
This API/Database is designed to run on an ec2 instance with the user ec2-user
using python-flask and mysql

## to get the server running do the following:
0. dependencies need to be installed first `sudo yum install mysql
1. `git clone https://github.com/FoodLife/FoodieVision-Server.git`
2. `cd FoodieVision-Server/client-api/`
3. sql stuff
4. start the flask serever using `sudo FLASK_APP=API.py python -m flask run --host=0.0.0.0 --port=5000`

The application will need to know the exact ip address of the server, currently it is configured to run on our ec2 instance.

The sever uses json data passed through post requests, here is an example post request to login 
```
POST /foodies/login HTTP/1.1

Host: localhost:5000
User-Agent: curl/7.43.0
Accept: */*
Content-Type: application/json
Content-Length: 32
{"user_name":"test","password":"pass"}
```
