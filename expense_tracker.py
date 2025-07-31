from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'

db :SQLAlchemy = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(50), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(200), nullable = False)

    def __init__(self, amount:int, category:str, description:str):
        self.amount = amount
        self.category = category
        self.description = description

    def __repr__(self):
        return f"\n(Expense: {self.id} - {self.amount} - {self.category} - {self.description})"

    
@app.route('/api/expenses', methods = ['POST'])
def add_expense():
    expense_data = request.get_json()
    try:
        expense = Expense(amount=expense_data['amount'], category=expense_data['category'], description=expense_data['description'])
        db.session.add(expense)
        db.session.commit()
        return jsonify({'message':'Successfully inserted!', 'expense':str(expense)}), 201
    except Exception as e:
        return jsonify({'error': str(e) }), 400

@app.route('/api/expenses', methods=['GET'])
def show_expenses():
    expenses = Expense.query.all()
    print(expenses)
    return jsonify({'Expenses':str(expenses)}), 201

@app.route('/api/expenses/<int:id>', methods=['PUT'])
def update_expense(id:int):
    try:
        expense = Expense.query.get(id)
        if not expense:
            return jsonify({'error':'Expense Not Found'}), 404

        data = request.get_json()
        expense.amount = data.get('amount', expense.amount)
        expense.category = data.get('category', expense.category)
        expense.description = data.get('description', expense.description)
        db.session.commit()
        
        return jsonify({'message': 'Successfully Updated', 'expense':str(expense)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:id>', methods=["DELETE"])
def delete_expense(id:int):
    try:
        expense = Expense.query.get(id)
        if not expense:
            return jsonify({'error':'Expense not found'}), 404

        db.session.delete(expense)
        db.session.commit()

        return jsonify({'message': 'Successfully Deleted', 'expense':str(expense)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
        


