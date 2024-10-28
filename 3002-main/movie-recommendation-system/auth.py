from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User  # Assuming User model includes get, create_user, and check_password methods

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Attempt to retrieve user from database
        user = User.get(username)  # Replace with actual query, e.g., User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # Ensure check_password method is defined in User model
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))  # Redirect to homepage or dashboard
        flash("Invalid credentials", "danger")
    
    return render_template('login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Create a new user
        user = User.create_user(username, password)  # Replace with actual user creation logic
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('auth.login'))  # Redirect to login page
    
    return render_template('register.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth.login'))
