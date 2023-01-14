import sys,os
from dbAdmin import *
from dotenv import load_dotenv
import mysql.connector
sys.path.append('..')
load_dotenv()
def connect():
  return mysql.connector.connect(
  host=os.environ['DB_HOST'],
  user=os.environ['DB_USER'],
  password=os.environ['DB_PASS'],
  database=os.environ['DB_NAME']
)
def render(template):
  cntx = connect()
  if template=="GET_USER":
    return getAllUsers(cntx)
  if template=="GET_TRANSACTION":
    return getAllTransactions(cntx)
  if template=="GET_APPLICATIONS":
    return getAllApplications(cntx)
  return response(501,error="not implemented")
  # if template == "dashboard":
  #     return dashboard(mysql)
  # if template == "getAllApplications":
  #   return getAllApplications(mysql)
  # if template == "getAllApplicationsDetails":
  #   return getAllApplicationsDetails(mysql)
  # if template == "addAdminStrator":
  #   return addAdminStrator(mysql)
  # if template == "setService":
  #   return setServices(mysql)
  # if template == "setServiceType":
  #   return setServiceType(mysql)