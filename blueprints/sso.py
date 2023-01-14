import jwt
from flask import Blueprint
import sys
from handler.ssoHandler import *
from generic.requestAndResponse import TransFormRequest
sys.path.append('..')
from db.sso import *
sso = Blueprint('sso', __name__,template_folder='templates')
#it is remaining part needs to be develop
@sso.route('/login',methods=['POST'])
def login():
    return render("LOGIN")   

