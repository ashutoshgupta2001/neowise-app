from app import app, db

class Users(db.Model):
    '''
    id, name, balance
    '''
    id = db.Column(db.String(50), nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float,nullable=False )


class Transactions(db.Model):
    '''
    transaction_id, amount, details, sender_id,receiver_id
    '''
    transaction_id = db.Column(db.String(50), nullable=False, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    details = db.Column(db.String(100),nullable=False )
    sender_id = db.Column(db.String(50),nullable=False )
    receiver_id = db.Column(db.String(50),nullable=False )



   