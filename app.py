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
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    vin = db.Column(db.String(80), nullable=True)

# Routes
@app.route('/')
def lock():
    return render_template('lock.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
