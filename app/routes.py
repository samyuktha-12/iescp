# app/routes.py
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, CampaignForm
from app.models import User, Campaign, AdRequest

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Implement login logic here
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
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
