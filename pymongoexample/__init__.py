from flask import Flask, render_template, request
from flask_pymongo import PyMongo

# from .extentions import mongo
# from .main import main

app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb://localhost:27017/kpmg'

mongo = PyMongo(app)

@app.route('/', methods=['GET','POST'])
def home():
    print('we re here')
    if request.method == 'POST':
        check = request.form['numberTVA']
        print('working? ::', check)
        return findOne(check)

    return render_template("test.html")


@app.route('/findOne')
def findOne(y):
    try:
        company = mongo.db.statutes.find({"_id": y})
        return render_template('test.html', company = company)
    except Exception as e:
        return e 

# def create_app(config_object='pymongoexample.settings'):
#     app = Flask(__name__)

#     app.config.from_object(config_object)

#     mongo.init_app(app)

#     app.register_blueprint(main)

#     return app
