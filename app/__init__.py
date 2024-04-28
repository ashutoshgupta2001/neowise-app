from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis


app = Flask(__name__)

password = 'Ashutosh@987'

app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:ashutosh@localhost/neowise'

db = SQLAlchemy(app)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

from app import users_routes
from app import transactions_routes


import json
from app.models import Users, Transactions


def load_data_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def insert_data_to_database(data):
    for item in data:
        user = Users(username=item['username'], email=item['email'])
        db.session.add(user)
    db.session.commit()

def insert_transaction_data_to_database(data):
    for item in data:
        transaction = Transactions(transaction_id=item['transactionId'], amount=item['amount'], details=item['details'], sender_id=item['senderId'], receiver_id=item['receiverId'])
        db.session.add(transaction)
    db.session.commit()

        # Load data from JSON file
        # json_user_data = load_data_from_json('/Users/ashutoshgupta/Downloads/neowise-se-assignment-flask/neowise-se-assignment/spec/users.json')

        # Insert data into the database
        # insert_data_to_database(json_user_data)
        # json_transaction_data = load_data_from_json('/Users/ashutoshgupta/Downloads/neowise-se-assignment-flask/neowise-se-assignment/spec/transaction.json')
        # insert_data_to_database(json_transaction_data)