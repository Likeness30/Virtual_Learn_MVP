#!/usr/bin/env python3

from flask import render_template, url_for, flash, redirect, request, jsonify
from . import app, db
from app.forms import RegistrationForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            password=hashed_password,
            dob=form.dob.data,
            gender=form.gender.data,
            primary_address=form.primary_address.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'dob', 'gender', 'primary_address']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        email=data['email'],
        phone_number=data['phone_number'],
        password=hashed_password,
        dob=data['dob'],
        gender=data['gender'],
        primary_address=data['primary_address']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Account created successfully'}), 201
