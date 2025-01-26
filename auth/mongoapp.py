from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)

bcrypt = Bcrypt(app)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")
client = MongoClient(os.getenv("MONGO_URI"))
db = client['user_auth_db']
users_collection = db['users']

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if users_collection.find_one({"username": username}):
            flash("Username already exists", "error")
        else:
            users_collection.insert_one({"username": username, "password": hashed_password})
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({"username": username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "error")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    flash("Please log in to access the dashboard.", "error")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)