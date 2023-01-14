from flask import render_template,request,make_response
import sys
sys.path.append('..')
from generic import *

def getTransactions(mysql):
    query = "select * from Transactions where is_deleted = 0 order by created_on desc"
    data = rawQuery(mysql,query,"SELECT","all")
    return response(200,data,"")

def targetedTransactions(mysql):
    query = "select * from Transactions where is_deleted = 0 order by created_on desc"
    data = rawQuery(mysql,query,"SELECT","all")
    return response(200,data,"")

def TransactionsDetails(mysql):
    print("dsndjfn")
    return render_template("/user/Transactions/details.html")