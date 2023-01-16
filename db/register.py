import sys
sys.path.append('..')
from generic import *

def registerPatients(mysql):
    try:
        data = request.get_json()
        print("data",request)
        print(data)
        if data.get('firstname')!=None and data.get('lastname')!=None and data.get('telephone')!=None and data.get('age')!=None and data.get('gender')!=None :
            print('h1')
            #conn = connect()
            cur = mysql.cursor()
            query = "insert into patient(firstname, lastname, age, gender, bloodgroup, email,telephone) values('{firstname}','{lastname}', {age}, '{gender}', '{bloodgroup}',  '{email}', {telephone})".format(firstname=data.get('firstname'),lastname=data.get('lastname'),
            age=data.get('age'),gender=data.get('gender'),bloodgroup=data.get('bloodgroup'),email=data.get('email'), telephone=data.get('telephone'))
            cur.execute(query)
            pid = cur.lastrowid
            newid=0
            query4="select id, address, city, state, pin from geos where address='{address}' and city='{city}' and state='{state}' and pin={pin}".format(address=data.get('address'),city=data.get('city'),state=data.get('state'),pin=data.get('pin'))
            print("q4",query4) 
            cur.execute(query4)
            #newdata=cur.fetchone()
            fields=[field_md[0] for field_md in cur.description]
            row=[dict(zip(fields,row)) for row in cur.fetchall()]
            print("query 4",row)
            if len(row)==0:
    
                query2="insert into geos(address, city, state, pin) values('{address}', '{city}', '{state}', {pin})".format(address=data.get('address'),city=data.get('city'),state=data.get('state'),pin=data.get('pin'))
            
                cur.execute(query2)
                g = cur.lastrowid
                print("patient_gio_ids",pid,g)
                query3= "insert into patient_geos(patient_id,geo_id) values({patient_id},{geo_id})".format(patient_id=pid,geo_id=g)            
                cur.execute(query3)
                mysql.commit()
            else:
                newid=row[0].get('id')
                query3= "insert into patient_geos(patient_id,geo_id) values({patient_id},{geo_id})".format(patient_id=pid,geo_id=newid)            
                cur.execute(query3)
                mysql.commit()
            mysql.close()
            return jsonify(data="registration successfull")
        else:
            print("val")
    except Exception as e:
        print(e)
    mysql.rollback()
    mysql.close()
    return jsonify(data="registration fail")
def getPatients(mysql):
    try:
        #con=connect()
        cur=mysql.cursor()
        query="select patient.id, patient.created_date, patient.firstname, patient.lastname, patient.age, patient.gender, patient.bloodgroup,patient.email, patient.telephone, geos.address, geos.city, geos.state, geos.pin from patient inner join patient_geos on patient.id=patient_geos.patient_id inner join geos on geos.id=patient_geos.geo_id where patient.is_delete=0 order by patient.created_date DESC; "

        #query="select *from patient"
        cur.execute(query)
        fields=[field_md[0] for field_md in cur.description]
        data=[dict(zip(fields,row)) for row in cur.fetchall()]
        cur.close()
        mysql.close()
       
        return jsonify(data)
    except Exception as e:
        print(e)
    return jsonify(data="failed to get details")


def updatePatients(mysql):
    try:
        data=request.get_json()
    #con=connect()
        cur=mysql.cursor()
        query="update patient set firstname='{firstname}',lastname='{lastname}',age={age},gender='{gender}', bloodgroup='{bloodgroup}', email='{email}' where id={id}".format(firstname=data.get('firstname'), lastname=data.get('lastname'), age=data.get('age'), gender=data.get('gender'),bloodgroup=data.get('bloodgroup'),email=data.get('email'), id=data.get('id'))
        cur.execute(query)
        mysql.commit()
        mysql.close()
        cur.close()
        response=jsonify("Record is updated Successfully")
        response.status_code=200
        return response
    except Exception as e:
        print(e)
    return jsonify(data="failed to get details")

    