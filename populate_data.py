from datetime import datetime, timedelta
import random

def populate_it_business_expenses(db, Category, Expense, db_session):
    
    
    with db_session:
        
        category_names = [
            'Zdravstveno osiguranje',
            'Mirovinsko osiguranje', 
            'Paušalni porez',
            'Licence',
            'Najam',
            'Marketing',
            'Hardver',
            'Softver'
        ]
        
        categories = {}
        
        
        for cat_name in category_names:
            categories[cat_name] = Category(name=cat_name)
        
        
        expenses_data = [
            
            {'desc': 'Doprinosi za zdravstveno osiguranje', 'amount': 118.67, 'category': 'Zdravstveno osiguranje', 'recurring': True},
            
            
            {'desc': 'Doprinosi za MIO 1. stup', 'amount': 107.88, 'category': 'Mirovinsko osiguranje', 'recurring': True},
            {'desc': 'Doprinosi za MIO 2. stup', 'amount': 35.96, 'category': 'Mirovinsko osiguranje', 'recurring': True},
            
            
            {'desc': 'Paušalni porez na dohodak', 'amount': 59.99, 'category': 'Paušalni porez', 'recurring': True},
            
            
            {'desc': 'Microsoft Visual Studio Professional', 'amount': 45.00, 'category': 'Licence', 'recurring': True},
            {'desc': 'Adobe Creative Cloud', 'amount': 22.99, 'category': 'Licence', 'recurring': True},
            {'desc': 'JetBrains IntelliJ IDEA', 'amount': 13.90, 'category': 'Licence', 'recurring': True},
            {'desc': 'Figma Professional', 'amount': 12.00, 'category': 'Licence', 'recurring': True},
            {'desc': 'Sketch licenca', 'amount': 99.00, 'category': 'Licence', 'recurring': False},
            {'desc': 'Affinity Designer', 'amount': 54.99, 'category': 'Licence', 'recurring': False},
            
            
            {'desc': 'Najam ureda - coworking space', 'amount': 150.00, 'category': 'Najam', 'recurring': True},
            {'desc': 'AWS hosting i serveri', 'amount': 25.00, 'category': 'Najam', 'recurring': True},
            {'desc': 'Google Workspace', 'amount': 5.40, 'category': 'Najam', 'recurring': True},
            {'desc': 'GitHub Pro račun', 'amount': 4.00, 'category': 'Najam', 'recurring': True},
            {'desc': 'Dropbox Business', 'amount': 15.00, 'category': 'Najam', 'recurring': True},
            
            
            {'desc': 'Google Ads kampanja', 'amount': 200.00, 'category': 'Marketing', 'recurring': False},
            {'desc': 'Facebook/Instagram reklame', 'amount': 100.00, 'category': 'Marketing', 'recurring': False},
            {'desc': 'LinkedIn Premium', 'amount': 59.99, 'category': 'Marketing', 'recurring': True},
            {'desc': 'Izrada web stranice', 'amount': 800.00, 'category': 'Marketing', 'recurring': False},
            {'desc': 'Logo i branding dizajn', 'amount': 300.00, 'category': 'Marketing', 'recurring': False},
            {'desc': 'Tisak vizitki', 'amount': 25.00, 'category': 'Marketing', 'recurring': False},
            {'desc': 'SEO analiza i optimizacija', 'amount': 250.00, 'category': 'Marketing', 'recurring': False},
            
            
            {'desc': 'MacBook Air M2 13"', 'amount': 1199.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Dell monitor 4K 27"', 'amount': 299.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Logitech MX Keys tipkovnica', 'amount': 99.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Logitech MX Master 3S miš', 'amount': 89.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Samsung SSD 980 1TB', 'amount': 69.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Anker USB-C hub', 'amount': 45.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Logitech C920 webcam', 'amount': 79.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Sony WH-1000XM5 slušalice', 'amount': 349.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Rain Design mStand stalak', 'amount': 49.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'WD My Passport 2TB', 'amount': 79.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'iPhone 15', 'amount': 899.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'iPad Air 5th gen', 'amount': 649.00, 'category': 'Hardver', 'recurring': False},
            {'desc': 'Apple Magic Keyboard', 'amount': 109.00, 'category': 'Hardver', 'recurring': False},
            
            
            {'desc': 'Slack Pro', 'amount': 7.25, 'category': 'Softver', 'recurring': True},
            {'desc': 'Notion Pro', 'amount': 8.00, 'category': 'Softver', 'recurring': True},
            {'desc': 'Trello Business Class', 'amount': 5.00, 'category': 'Softver', 'recurring': True},
            {'desc': 'Zoom Pro licenca', 'amount': 14.99, 'category': 'Softver', 'recurring': True},
            {'desc': '1Password Business', 'amount': 8.00, 'category': 'Softver', 'recurring': True},
            {'desc': 'Mailchimp Standard', 'amount': 20.00, 'category': 'Softver', 'recurring': True},
            {'desc': 'Canva Pro', 'amount': 12.99, 'category': 'Softver', 'recurring': True},
            {'desc': 'Grammarly Premium', 'amount': 12.00, 'category': 'Softver', 'recurring': True},
            {'desc': 'CleanMyMac X', 'amount': 89.95, 'category': 'Softver', 'recurring': False},
            {'desc': 'Parallels Desktop', 'amount': 99.99, 'category': 'Softver', 'recurring': False}
        ]
        
        
        start_date = datetime.now() - timedelta(days=180)
        
        for expense_data in expenses_data:
            category = categories[expense_data['category']]
            
            if expense_data['recurring']:
                
                current_date = start_date
                for i in range(6):  # 6 mjeseci
                    
                    if expense_data['category'] in ['Zdravstveno osiguranje', 'Mirovinsko osiguranje', 'Paušalni porez']:
                        day = 5
                        varied_amount = expense_data['amount']
                    else:
                        day = random.randint(1, 28)
                        amount_variation = random.uniform(0.98, 1.02)
                        varied_amount = round(expense_data['amount'] * amount_variation, 2)
                    
                    expense_date = current_date.replace(day=day)
                    
                    Expense(
                        amount=varied_amount,
                        description=expense_data['desc'],
                        date=expense_date,
                        category=category,
                        recurring=expense_data['recurring']
                    )
                    
                    
                    if current_date.month == 12:
                        current_date = current_date.replace(year=current_date.year + 1, month=1)
                    else:
                        current_date = current_date.replace(month=current_date.month + 1)
            else:
                
                days_offset = random.randint(0, 180)
                expense_date = start_date + timedelta(days=days_offset)
                
                Expense(
                    amount=expense_data['amount'],
                    description=expense_data['desc'],
                    date=expense_date,
                    category=category,
                    recurring=expense_data['recurring']
                )
        
