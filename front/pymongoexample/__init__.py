import re
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
        if request.form['numberTVA'] != '' and request.form['compName'] == '' and request.form['creatDate'] == '':
            check = request.form['numberTVA']
            print('id is: ', check)
            return findById(check)
        elif request.form['compName'] != '' and request.form['numberTVA'] == '' and request.form['creatDate'] == '':
            name = request.form['compName']
            print('name is: ', name)
            return findByName(name)
        elif request.form['creatDate'] != '' and request.form['numberTVA'] == '' and request.form['compName'] == '':
            date = request.form['creatDate']
            print('creation date: ', date)
            return findByDate(date)
        elif request.form['creatDate'] == '' and request.form['numberTVA'] == '' and request.form['compName'] == '':
            print('find everything')
            return findEverything()
        else:
            print('nothing to look for')
            return 'nothing to look for'

        


    return render_template("test.html")


@app.route('/findById')
def findById(y):
    
    company = mongo.db.statutes.find({"_id": y})
    return render_template('test.html', company = company)

@app.route('/findByName')
def findByName(y):
    cleanString = re.sub('\W+',' ', y)  # r in front of '\W+'
    stringList = cleanString.split()
    print(stringList)
    pattern_string = ''
    for word in stringList:
        pattern_string += f'(?:{word})|'
    pattern_string = pattern_string[:-1]
    # company = mongo.db.statutes.find({"Denomination": {"$regex" : pattern_string}})
    company = mongo.db.statutes.find({"Denomination": re.compile(pattern_string, re.IGNORECASE)})
    #company = mongo.db.statutes.find({"Denomination": y})
    return render_template('test.html', company = company)



@app.route('/findByDate')
def findByDate(y):
    company = []
    for doc in mongo.db.statutes.find():
        if y in doc['documents'].keys():
            print('deep check')
            #company = doc['documents'][y]['text']
            #print(company)
            company.append(doc)
    # textDir = mongo.db.statutes.find({f"documents.{y}"})
    # company = textDir.text

    return render_template('test.html', company = company, date = y)


@app.route('/findEverything')
def findEverything():
    company = mongo.db.statutes.find()
    return render_template('test.html', company = company)

# def create_app(config_object='pymongoexample.settings'):
#     app = Flask(__name__)

#     app.config.from_object(config_object)

#     mongo.init_app(app)

#     app.register_blueprint(main)

#     return app