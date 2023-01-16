import sys,os
from db import*
import mysql.connector
sys.path.append('..')
#load_dotenv('')
cntx=None
def createConnection():
    return mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    database=os.environ['DB_NAME'] 
    )
def render(template):
    cntx=createConnection()
    if template=='registerp':
        return registerPatients(cntx)
    if template=='getPatient':
        return getPatients(cntx)
    if template=='updatePatient':
        return updatePatients(cntx)
    else:
        return response(501,"","Invalid API Service")
