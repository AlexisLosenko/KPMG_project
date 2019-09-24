from flask import Blueprint
from .extentions import mongo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # something = 'hello there'
    print('is this working?')
    # user_collection = mongo.db.statutes
    # user_collection.insert({'name': 'bob'})
    return '<h1>hello there</h1>'

@main.route('/find')
def find():
    company_collection = mongo.db.statutes
    company = company_collection.find_one({'_id' : '0700974260'})
    print('checking: ', company)
    return "<h1>TVA number: {company['_id']}</h1>"