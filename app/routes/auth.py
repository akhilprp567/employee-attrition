from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# 🔥 SIGNUP
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            full_name = request.form.get('full_name', '').strip()
            department = request.form.get('department', '').strip()

            # Validation
            if not all([username, email, password, full_name]):
                flash('All fields are required!', 'error')
                return redirect(url_for('auth.signup'))

            if len(username) < 3:
                flash('Username must be at least 3 characters!', 'error')
                return redirect(url_for('auth.signup'))

            if len(password) < 6:
                flash('Password must be at least 6 characters!', 'error')
                return redirect(url_for('auth.signup'))

            if password != confirm_password:
                flash('Passwords do not match!', 'error')
                return redirect(url_for('auth.signup'))

            # Check duplicates
            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'error')
                return redirect(url_for('auth.signup'))

            if User.query.filter_by(email=email).first():
                flash('Email already exists!', 'error')
                return redirect(url_for('auth.signup'))

            # Create user
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                department=department,
                role='admin'
            )

            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            print("✅ User created successfully")

            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            print("❌ ERROR:", e)   # IMPORTANT
            flash('Error creating account!', 'error')

    return render_template('signup.html')


# 🔥 LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        if not username or not password:
            flash('Username and password required!', 'error')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(username=username).first()

        if not user:
            print("❌ User not found")
            flash('Invalid username or password!', 'error')
            return redirect(url_for('auth.login'))

        if not user.check_password(password):
            print("❌ Wrong password")
            flash('Invalid username or password!', 'error')
            return redirect(url_for('auth.login'))

        if hasattr(user, 'is_active') and not user.is_active:
            flash('Account inactive!', 'error')
            return redirect(url_for('auth.login'))

        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        login_user(user, remember=remember)

        print("✅ Login successful")

        return redirect('/dashboard/')   # FORCE redirect

    return render_template('login.html')


# 🔥 LOGOUT
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))


# 🔥 ERROR HANDLER
@auth_bp.app_errorhandler(404)
def not_found(error):
    return redirect(url_for('auth.login'))