from .transaction import getTransactions
from flask import jsonify,render_template,request,make_response
import sys
sys.path.append('..')
from generic import *


def dashboard(mysql):
    if request.method=='GET':
        data = rawQuery(mysql,"select  SUM(CASE WHEN fd.status = 'PENDING' THEN 1 ELSE 0 END) AS `PENDING`,SUM(CASE WHEN fd.status = 'REJECTED' THEN 1 ELSE 0 END) AS `REJECTED`,SUM(CASE WHEN fd.status = 'ONGOING' THEN 1 ELSE 0 END) AS `ONGOING`,SUM(CASE WHEN fd.status = 'COMPLETED' THEN 1 ELSE 0 END) AS `COMPLETED` FROM form_data fd WHERE is_deleted=0","SELECT","one")
        context = {"data":data}
        return render_template('user/dash.html',context=context)
    else:
        return response(404,"","page Not Found")
# select f_data.PENDING,f_data.REJECTED,f_data.ONGOING,f_data.COMPLETED FROM user 
# left join (select  SUM(CASE WHEN fd.status = 'PENDING' THEN 1 ELSE 0 END) AS `PENDING`,
# SUM(CASE WHEN fd.status = 'REJECTED' THEN 1 ELSE 0 END) AS `REJECTED`,
# SUM(CASE WHEN fd.status = 'ONGOING' THEN 1 ELSE 0 END) AS `ONGOING`,
# SUM(CASE WHEN fd.status = 'COMPLETED' THEN 1 ELSE 0 END) AS `COMPLETED`,fd.user_id FROM form_data fd WHERE is_deleted=0) AS f_data ON f_data.user_id=user.id
# group by 1,2,3,4; 



