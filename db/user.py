import sys
sys.path.append('..')
from generic import *

def addUser(mysql):
    try:
        data = request.get_json()
        mycursor = mysql.cursor()
        sql = "INSERT INTO user (fname,mname,lname,mail,mobile,password) VALUES (%s, %s,%s, %s,%s, %s)"
        val = (data.get('first_name'),data.get('middle_name'),data.get('last_name'),data.get('mail'),data.get('mobile'),data.get('password'))
        mycursor.execute(sql, val)
        id = mycursor.lastrowid
        sql = "INSERT INTO wallete (user_id) VALUES (%s)"
        mycursor.execute(sql, [str(id)])
        mysql.commit()
        return response(200,"user created")
    except Exception as e:
        mysql.rollback()
        return response(404,"",e)