from flask import Flask
from blueprints import userBluePrint,adminBluePrint,sso,filemanager
from flask_cors import CORS,cross_origin
# --------------------
# Author : Sandesh Rathod
# sandeshrathod09@gmail.com
# -------------------
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"methods": ["OPTIONS", "GET", "POST"]}})
app.register_blueprint(filemanager,url_prefix="/file")
app.register_blueprint(userBluePrint,url_prefix="/api/v1/")
app.register_blueprint(adminBluePrint,url_prefix="/admin")
app.register_blueprint(sso,url_prefix="/sso")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=7000,debug=True,threaded=True)