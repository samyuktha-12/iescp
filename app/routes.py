# app/routes.py
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db, api
from app.forms import LoginForm, RegistrationForm, CampaignForm
from app.models import User, Campaign, AdRequest
from app.resources import IndexResource, LoginResource, RegisterResource, CreateCampaignResource
import requests

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {
            'username': form.username.data,
            'password': form.password.data,
            'remember_me': form.remember_me.data
        }
        api_url = url_for('loginresource', _external=True)
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            json_response = response.json()
            if 'redirect_url' in json_response:
                redirect_url = json_response['redirect_url']
                return redirect(redirect_url)
            else:
                flash(json_response.get('message', 'Login failed'))
                return redirect(url_for('login'))
        else:
            flash(response.json().get('message', 'Login failed'))
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    data = {
            'username': form.username.data,
            'email':form.email.data,
            'password': form.password.data,
            'role': form.role.data
        }
    if form.validate_on_submit():
        api_url = url_for('registerresource', _external=True)
        response = requests.post(api_url,data)
        if response.status_code == 200:
            json_response = response.json()
            if json_response['status_code']==200:
                flash('Congratulations, you are now a registered user!<br>Please login to start enjoying our services!')
                redirect_url = json_response['redirect_url']
                return redirect(redirect_url)
            else:
                flash(json_response['message'])
                return redirect('register')
        else:
            flash('Sign Up failed. Try Again')
            return redirect(url_for('register'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}")
    return render_template('register.html', title='Register', form=form)

@app.route('/admin/dashboard')
def admin_dashboard():
    # Implement admin dashboard view logic here
    return render_template('admin_dashboard.html', title='Admin Dashboard')

@app.route('/sponsor/dashboard')
def sponsor_dashboard():
    # Implement sponsor dashboard view logic here
    return render_template('sponsor_dashboard.html', title='Sponsor Dashboard')

@app.route('/influencer/dashboard')
def influencer_dashboard():
    # Implement influencer dashboard view logic here
    return render_template('influencer_dashboard.html', title='Influencer Dashboard')

@app.route('/campaign/create', methods=['GET', 'POST'])
def create_campaign():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data,
            goals=form.goals.data,
            sponsor=current_user
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created successfully!')
        return redirect(url_for('sponsor_dashboard'))
    return render_template('create_campaign.html', title='Create Campaign', form=form)

# Add API resource routes
api.add_resource(IndexResource, '/api/')
api.add_resource(LoginResource, '/api/login')
api.add_resource(RegisterResource, '/api/register')
api.add_resource(CreateCampaignResource, '/api/campaign/create')
