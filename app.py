from flask import Flask, render_template, request, redirect, url_for, jsonify
from pony.orm import Database, PrimaryKey, Required, Optional, Set, db_session, select, desc
from datetime import datetime
from populate_data import populate_it_business_expenses
import os
import sqlite3

app = Flask(__name__)
db = Database()

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'expense_tracker.sqlite')

parent_dir = os.path.dirname(db_path)
if parent_dir and not os.path.exists(parent_dir):
    os.makedirs(parent_dir, exist_ok=True)

os.makedirs(os.path.join(script_dir, 'static', 'css'), exist_ok=True)
os.makedirs(os.path.join(script_dir, 'templates'), exist_ok=True)

if not os.path.exists(db_path):
    print(f"Stvaram novu SQLite bazu: {db_path}")
    try:
        
        if os.path.isdir(db_path):
            print(f"❌ GREŠKA: {db_path} je direktorij, ne datoteka!")
            import shutil
            shutil.rmtree(db_path)
            print(f"✅ Uklonjen direktorij: {db_path}")
        
        # Stvori praznu SQLite datoteku
        conn = sqlite3.connect(db_path)
        conn.close()
        
        
        if os.path.isfile(db_path):
            print(f"✅ SQLite baza uspješno stvorena: {db_path}")
        else:
            raise Exception("Datoteka nije stvorena")
            
    except Exception as e:
        print(f"❌ Greška pri stvaranju baze: {e}")
        exit(1)
else:
    print(f"✅ SQLite baza već postoji: {db_path}")

print(f"Database path: {db_path}")

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
    recurring = Required(bool, default=False) 

db.bind(provider='sqlite', filename=db_path, create_db=True)
db.generate_mapping(create_tables=True)

@app.route('/')
@db_session
def index():
    categories = Category.select()
    expenses = Expense.select().order_by(desc(Expense.date))
    return render_template('index.html', categories=categories, expenses=expenses)

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

@app.route('/expenses', methods=['GET'])
@db_session
def get_expenses():
    category_filter = request.args.get('category', '')
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'desc')
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page', '25')
    
    if per_page == 'all':
        per_page_int = None
    else:
        per_page_int = int(per_page)

    all_expenses = list(Expense.select())
    if category_filter:
        try:
            category_id = int(category_filter)
            expenses = [e for e in all_expenses if e.category.id == category_id]
        except (ValueError, TypeError):
            expenses = all_expenses
    else:
        expenses = all_expenses
    
    if sort_by == 'amount':
        expenses.sort(key=lambda e: e.amount, reverse=(sort_order == 'desc'))
    elif sort_by == 'category':
        expenses.sort(key=lambda e: e.category.name, reverse=(sort_order == 'desc'))
    elif sort_by == 'id':
        expenses.sort(key=lambda e: e.id, reverse=(sort_order == 'desc'))  # Fixed typo: exercises -> expenses
    else:
        expenses.sort(key=lambda e: e.date, reverse=(sort_order == 'desc'))
    
    total_expenses = len(expenses)
    
    if per_page_int:
        start_idx = (page - 1) * per_page_int
        end_idx = start_idx + per_page_int
        paginated_expenses = expenses[start_idx:end_idx]
        
        total_pages = (total_expenses + per_page_int - 1) // per_page_int
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1 if has_prev else None
        next_page = page + 1 if has_next else None
        
        page_numbers = []
        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)
        for i in range(start_page, end_page + 1):
            page_numbers.append(i)
    else:
        paginated_expenses = expenses
        total_pages = 1
        has_prev = False
        has_next = False
        prev_page = None
        next_page = None
        page_numbers = [1]
    
    categories = list(Category.select())
    
    return render_template('expenses.html', 
                          expenses=paginated_expenses, 
                          categories=categories,
                          current_category=category_filter,
                          current_sort=sort_by,
                          current_order=sort_order,
                          current_page=page,
                          per_page=per_page,
                          total_expenses=total_expenses,
                          total_pages=total_pages,
                          has_prev=has_prev,
                          has_next=has_next,
                          prev_page=prev_page,
                          next_page=next_page,
                          page_numbers=page_numbers)

@app.route('/expenses/add', methods=['POST'])
@db_session
def add_expense():
    amount = float(request.form['amount'])
    description = request.form['description']
    date_str = request.form['date']
    date = datetime.strptime(date_str, '%Y-%m-%d')
    category_id = int(request.form['category_id'])
    recurring = 'recurring' in request.form
    
    Expense(
        amount=amount,
        description=description,
        date=date,
        category=Category[category_id],
        recurring=recurring
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
    expense.recurring = 'recurring' in request.form
    
    return redirect(url_for('get_expenses'))

@app.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@db_session
def delete_expense(expense_id):
    Expense[expense_id].delete()
    return redirect(url_for('get_expenses'))

@app.route('/reports', methods=['GET'])
@db_session
def reports():
    categories = Category.select()
    
    category_totals = []
    for category in categories:
        total = sum(expense.amount for expense in category.expenses)
        category_totals.append({
            'category': category.name,
            'total': total
        })
    
    total_expenses = sum(expense.amount for expense in Expense.select())
    
    return render_template('reports.html', 
                          category_totals=category_totals, 
                          total_expenses=total_expenses)

@app.route('/api/chart-data', methods=['GET'])
@db_session
def chart_data():
    try:
        categories = list(Category.select())
        category_data = []
        
        for category in categories:
            expenses = list(category.expenses)
            total = sum(expense.amount for expense in expenses)
            if total > 0:
                category_data.append({
                    'name': category.name,
                    'value': round(total, 2)
                })
        
        category_data.sort(key=lambda x: x['value'], reverse=True)
        return jsonify(category_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/time-series-data', methods=['GET'])
@db_session
def time_series_data():
    try:
        expenses = list(Expense.select())
        
        if not expenses:
            return jsonify([])
        
        monthly_data = {}
        for expense in expenses:
            month_key = expense.date.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = 0
            monthly_data[month_key] += expense.amount
        
        if monthly_data:
            sorted_months = sorted(monthly_data.keys())
            time_series = [
                {'month': month, 'amount': round(monthly_data[month], 2)}
                for month in sorted_months
            ]
        else:
            time_series = []
        
        return jsonify(time_series)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/monthly-comparison', methods=['GET'])
@db_session
def monthly_comparison():
    try:
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        
        if current_month == 1:
            prev_month = 12
            prev_year = current_year - 1
        else:
            prev_month = current_month - 1
            prev_year = current_year
        
        current_month_data = {}
        prev_month_data = {}
        
        categories = list(Category.select())
        for category in categories:
            current_month_data[category.name] = 0
            prev_month_data[category.name] = 0
        
        all_expenses = list(Expense.select())
        
        for expense in all_expenses:
            if expense.date.month == current_month and expense.date.year == current_year:
                current_month_data[expense.category.name] += expense.amount
            elif expense.date.month == prev_month and expense.date.year == prev_year:
                prev_month_data[expense.category.name] += expense.amount
        
        filtered_current = {k: round(v, 2) for k, v in current_month_data.items() if v > 0}
        filtered_prev = {k: round(v, 2) for k, v in prev_month_data.items() if v > 0}
        
        all_categories = set(filtered_current.keys()) | set(filtered_prev.keys())
        
        result = {
            'current_month': {
                'name': current_date.strftime('%B %Y'),
                'data': {cat: filtered_current.get(cat, 0) for cat in all_categories}
            },
            'prev_month': {
                'name': datetime(prev_year, prev_month, 1).strftime('%B %Y'),
                'data': {cat: filtered_prev.get(cat, 0) for cat in all_categories}
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-categories', methods=['GET'])
@db_session
def top_categories():
    try:
        categories = list(Category.select())
        category_data = []
        
        for category in categories:
            expenses = list(category.expenses)
            total = sum(expense.amount for expense in expenses)
            if total > 0:
                category_data.append({
                    'name': category.name,
                    'value': round(total, 2)
                })
        
        category_data.sort(key=lambda x: x['value'], reverse=True)
        top_5 = category_data[:5]
        
        return jsonify(top_5)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expense-summary', methods=['GET'])
@db_session
def expense_summary():
    try:
        all_expenses = list(Expense.select())
        
        if not all_expenses:
            return jsonify({
                'total': 0,
                'count': 0,
                'average': 0,
                'recurring_total': 0,
                'non_recurring_total': 0,
                'recurring_percentage': 0
            })
        
        total_expenses = sum(e.amount for e in all_expenses)
        recurring_expenses = sum(e.amount for e in all_expenses if e.recurring)
        non_recurring_expenses = total_expenses - recurring_expenses
        
        summary = {
            'total': round(total_expenses, 2),
            'count': len(all_expenses),
            'average': round(total_expenses / len(all_expenses), 2),
            'recurring_total': round(recurring_expenses, 2),
            'non_recurring_total': round(non_recurring_expenses, 2),
            'recurring_percentage': round((recurring_expenses / total_expenses * 100), 1) if total_expenses > 0 else 0
        }
        
        return jsonify(summary)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with db_session:
        existing_categories = Category.select().count()
        existing_expenses = Expense.select().count()
        
        if existing_categories == 0 and existing_expenses == 0:
            print("🚀 Pokretanje populacije baze podataka...")
            populate_it_business_expenses(db, Category, Expense, db_session)
        else:
            print(f"📊 Baza već sadrži {existing_categories} kategorija i {existing_expenses} troškova")
    
    app.run(debug=True, host='0.0.0.0', port=5001)