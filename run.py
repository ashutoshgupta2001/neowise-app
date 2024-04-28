from app import app, load_data_from_json, insert_transaction_data_to_database, db
if __name__ == "__main__":
#     with app.app_context():
#  # Create database tables if they don't exist
#        db.create_all()
#        json_transaction_data = load_data_from_json('/Users/ashutoshgupta/Downloads/neowise-se-assignment-flask/neowise-se-assignment/spec/transaction.json')
#        insert_transaction_data_to_database(json_transaction_data)
    app.run(debug=True)

