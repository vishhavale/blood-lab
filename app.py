from flask import Flask
from blueprints import userBluePrint
from flask_cors import CORS,cross_origin
# --------------------
# Author : Vishvajit Havale
# vishvajithavale76@gmail.com
# -------------------
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"methods": ["OPTIONS", "GET", "POST"]}})
app.register_blueprint(userBluePrint,url_prefix="/api/v1")
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=7000,debug=True,threaded=True)