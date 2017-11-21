from flaskext.mysql import MySQL

def login(connection: MySQL,user_name,password):
    try:
        cur = connection.cursor()
        string = "call login('{}','{}') ".format(user_name,password)
        cur.execute(string)
        return cur.fetchall()
    except:
        return -2

def create_user(connection: MySQL,user_name,password):
    try:
        cur = connection.cursor()
        string = "call create_user('{}','{}') ".format(user_name,password)
        cur.execute(string)
        return cur.fetchall()
    except:
        return -2

def create_picture(connection: MySQL, user_token,analysis,confidence):
    try:
        cur = connection.cursor()
        string = "call create_picture('{}','{}','{}')".format(user_token,analysis,confidence)
        cur.execute(string)
        return cur.fetchall()
    except:
        return -2

def create_favorite(connection: MySQL,user_token,picture_id):
    try:
        cur = connection.cursor()
        string = "call create_favorite('{}','{}')".format(user_token,picture_id)
        cur.execute(string)
        return cur.fetchall()
    except:
        return -2

def delete_favorite(connection: MySQL,user_token,picture_id):
    try:
        cur = connection.cursor()
        string = "call delete_favorite('{}','{}')".format(user_token,picture_id)
        cur.execute(string)
        return cur.fetchall()
    except:
        return -2

def change_password(connection: MySQL,user_token,new_password):
    try:
        cur = connection.cursor()
        string = "call change_password('{}','{}')".format(user_token,new_password)
        cur.execute(string)
        return cur.fetchall()
    except:
        return -2

