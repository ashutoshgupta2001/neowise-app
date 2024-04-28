from flask import jsonify, request, session
import os
from datetime import date
from app import app, db
import uuid
from .models import Users, Transactions

def generate_id():
    return str(uuid.uuid4())

@app.route('/transactions/', methods=['GET','POST'])
def get_transactions():
    if request.method == 'GET': 
        transactions = Transactions.query.all()
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
    if request.method == 'POST':
        request_data = request.json
        details = request_data.get('details')
        amount = request_data.get('amount')
        sender_id = request_data.get('senderId')
        receiver_id = request_data.get('receiverId')

        receiver = Users.query.filter_by(id=receiver_id).first()
        sender = Users.query.filter_by(id=sender_id).first()

        if not receiver:
            return {
                "success": False,
                "message": "Receiver not found for provided receiverId"
            }

        try:
            if int(sender.balance) >= int(amount):
                sender.balance -= int(amount)
                receiver.balance += int(amount)
                transaction_id = generate_id()
                transaction = Transactions(transaction_id=transaction_id, amount=amount, details=details, sender_id=sender_id, receiver_id=receiver_id)
                db.session.add(transaction)
                db.session.commit()

                print(f"{sender.name} Rs {amount} has been debited from your account")
                print(f"{receiver.name} Rs {amount} has been credited to your account")

                return {
                    "success": True,
                    "message": "Transaction completed successfully",
                    "payment_id": transaction_id
                }
            else:
                return {
                    "success": False,
                    "message": "Transaction failed! Not enough balance available to make this transaction"
                }, 400
        except Exception as e:
            print("An error occurred while making transaction:", e)
            return {
                "success": False,
                "message": "An error occurred while making transaction"
            }, 500   


#Route to get a specific transaction by ID
@app.route('/transactions/<transaction_id>', methods=['GET','DELETE'])
def get_transaction(transaction_id):
    if request.method == 'GET':
        transactions = Transactions.query.filter_by(transaction_id=transaction_id).all()
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
    
    if request.method == 'DELETE':
        transaction = Transactions.query.filter_by(transaction_id=transaction_id).first()
        if transaction:
            print(">>>>>>>>>>>>>>>>",transaction)
            print(transaction.receiver_id)
            try:
                receiver = Users.query.filter_by(id=transaction.receiver_id).first()
                sender = Users.query.filter_by(id=transaction.sender_id).first()
                amount = transaction.amount
                sender.balance += int(amount)
                receiver.balance -= int(amount)

                db.session.delete(transaction)
                db.session.commit()
                return {
                    "success" : True,
                    "message" : "Transaction deleted succesfully"
                }
            except Exception as e:
                print("An error occurred while making transaction:", e)
            return {
                "success": False,
                "message": "An error occurred while making transaction"
            }, 500 

        else:
            return {
                "success" : False,
                "message" : "No transaction found for this transaction id"
            }


