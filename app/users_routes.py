from flask import jsonify, request
import os
from datetime import date
from app import app, db
import json
from .models import Users, Transactions


@app.route('/api/users/', methods=['GET'])
def get_users():
    if request.method == 'GET': 
        users = Users.query.all()
        users_data = [
        {
            'id': user.id,
            'name': user.details,
            'balance': user.balance
        }
        for user in users
    ]
        return jsonify(users_data)

# Route to get a specific user by ID
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if request.method == 'GET':
        users = Users.query.filter_by(id=user_id).all()
        if users:
            users_data = [
        {
            'id': user.id,
            'name': user.details,
            'balance': user.balance
        }
        for user in users
    ]
            return jsonify(users_data)
        
        return jsonify({"error": "transaction not found"}), 404

@app.route('/api/users/<user_id>/transactions', methods=['GET'])
def get_user_transactions(user_id):
    if request.method == 'GET':
        transactions = Transactions.query.filter((Transactions.sender_id==user_id)|(Transactions.receiver_id==user_id)).all()
        if transactions:
            transactions_data = [
        {
            'transaction_id': transaction.transaction_id,
            'details': transaction.details,
            'amount': transaction.amount,
            'sender_id': transaction.sender_id,
            'receiver_id': transaction.receiver_id
        }
        for transaction in transactions
    ]
            return jsonify(transactions_data)
        
        return jsonify({"error": "transaction not found"}), 404
    return jsonify({"success":False,
                    "error": "Transactions not found for this user"})