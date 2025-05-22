from flask import Flask, render_template, request, redirect, url_for, jsonify
from pony.orm import Database, PrimaryKey, Required, Optional, Set, db_session, select, desc
from datetime import datetime
import os

app = Flask(__name__)
db = Database()
db.bind(provider='sqlite', filename='expense_tracker.sqlite', create_db=True)

# Osiguraj da direktoriji postoje
os.makedirs(os.path.join('static', 'css'), exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Model podataka
class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    expenses = Set('Expense')

class Expense(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Required(float)
    description = Required(str)
    date = Required(datetime)
    category = Required(Category)

db.generate_mapping(create_tables=True)

# Rute
@app.route('/')
@db_session
def index():
    categories = Category.select()
    expenses = Expense.select().order_by(desc(Expense.date))
    return render_template('index.html', categories=categories, expenses=expenses)

# CRUD operacije za kategorije
@app.route('/categories', methods=['GET'])
@db_session
def get_categories():
    categories = Category.select()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['POST'])
@db_session
def add_category():
    name = request.form['name']
    Category(name=name)
    return redirect(url_for('get_categories'))

@app.route('/categories/edit/<int:category_id>', methods=['POST'])
@db_session
def edit_category(category_id):
    category = Category[category_id]
    category.name = request.form['name']
    return redirect(url_for('get_categories'))

@app.route('/categories/delete/<int:category_id>', methods=['POST'])
@db_session
def delete_category(category_id):
    Category[category_id].delete()
    return redirect(url_for('get_categories'))

# CRUD operacije za troškove
@app.route('/expenses', methods=['GET'])
@db_session
def get_expenses():
    expenses = Expense.select().order_by(desc(Expense.date))
    categories = Category.select()
    return render_template('expenses.html', expenses=expenses, categories=categories)

@app.route('/expenses/add', methods=['POST'])
@db_session
def add_expense():
    amount = float(request.form['amount'])
    description = request.form['description']
    date_str = request.form['date']
    date = datetime.strptime(date_str, '%Y-%m-%d')
    category_id = int(request.form['category_id'])
    
    Expense(
        amount=amount,
        description=description,
        date=date,
        category=Category[category_id]
    )
    
    return redirect(url_for('get_expenses'))

@app.route('/expenses/edit/<int:expense_id>', methods=['POST'])
@db_session
def edit_expense(expense_id):
    expense = Expense[expense_id]
    expense.amount = float(request.form['amount'])
    expense.description = request.form['description']
    date_str = request.form['date']
    expense.date = datetime.strptime(date_str, '%Y-%m-%d')
    expense.category = Category[int(request.form['category_id'])]
    
    return redirect(url_for('get_expenses'))

@app.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@db_session
def delete_expense(expense_id):
    Expense[expense_id].delete()
    return redirect(url_for('get_expenses'))

# Specifične funkcije za use-case
@app.route('/reports', methods=['GET'])
@db_session
def reports():
    categories = Category.select()
    
    # Ukupni troškovi po kategorijama
    category_totals = []
    for category in categories:
        total = sum(expense.amount for expense in category.expenses)
        category_totals.append({
            'category': category.name,
            'total': total
        })
    
    # Ukupni troškovi (svi)
    total_expenses = sum(expense.amount for expense in Expense.select())
    
    return render_template('reports.html', 
                          category_totals=category_totals, 
                          total_expenses=total_expenses)

@app.route('/api/chart-data', methods=['GET'])
@db_session
def chart_data():
    categories = Category.select()
    
    # Podaci za pie chart - troškovi po kategorijama
    category_data = []
    for category in categories:
        total = sum(expense.amount for expense in category.expenses)
        category_data.append({
            'name': category.name,
            'value': total
        })
    
    return jsonify(category_data)

if __name__ == '__main__':
    # Inicijalni podaci ako je potrebno
    with db_session:
        if not Category.select().count():
            Category(name="Hrana")
            Category(name="Prijevoz")
            Category(name="Stanovanje")
            Category(name="Zabava")
            Category(name="Ostalo")
    
    app.run(debug=True, host='0.0.0.0', port=5001)