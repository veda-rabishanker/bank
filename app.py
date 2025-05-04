from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for sessions

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String(80), nullable=False, unique=True)
    pin = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable = False, default=0.0) 

@app.route('/')
def lock():
    return render_template('lock.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        account_num = request.form.get('account_num')
        pin = request.form.get('pin')

        # Validate user credentials
        user = User.query.filter_by(account_num=account_num).first()
        if user and user.pin == pin:
            session['user_id'] = user.id  # Set user_id in session
            return render_template('dashboard.html', user=user)
        else:
            return render_template('lock.html', error="Invalid account number or PIN")
    
    # If user is already logged in
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', user=user)
    
    return redirect('/')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if request.method == 'POST':
        account_num = request.form.get('account_num')
        pin = request.form.get('pin')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Check if account number or email already exists
        existing_user = User.query.filter((User.account_num == account_num) | (User.email == email)).first()
        if existing_user:
            return render_template('signup.html', error="Account number or email already exists.")

        # Create a new user
        new_user = User(
            account_num=account_num,
            pin=pin,
            name=name,
            age=int(age),
            gender=gender,
            email=email,
            phone=phone
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')  # Redirect to login page after successful signup

    return render_template('signup.html')

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        try:
            amount = float(request.form.get('amount'))
            if amount <= 0:
                raise ValueError("Amount must be positive")
            user.balance += amount
            db.session.commit()
        except ValueError:
            return render_template('dashboard.html', user=user, error="Invalid deposit amount")
        return redirect('/dashboard')
    return redirect('/')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        amount = float(request.form.get('amount'))
        if user.balance >= amount:
            user.balance -= amount
            db.session.commit()
        else:
            return render_template('dashboard.html', user=user, error="Insufficient balance")
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user_id from session
    return redirect('/')
@app.route('/update_account', methods=['GET', 'POST'])
def update_account():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if request.method == 'POST':
            user.name = request.form.get('name')
            user.email = request.form.get('email')
            user.phone = request.form.get('phone')
            db.session.commit()
            return redirect('/dashboard')
        return render_template('update_account.html', user=user)
    return redirect('/')

@app.route('/close_account', methods=['POST'])
def close_account():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id', None)  # Log the user out
        return redirect('/')
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
