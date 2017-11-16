from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'foodies'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'test'
mysql.init_app(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_DB'] = 'test'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()
cursor.execute("select \'a\' from dual")

data = cursor.fetchall()
for result in data:
    print(result[0])


