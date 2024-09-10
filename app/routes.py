# app/routes.py
from flask import render_template, flash, redirect, url_for, session
from app import app, db, api
from app.forms import LoginForm, RegistrationForm, CampaignForm
from app.models import User, Campaign, AdRequest, Negotiations
from app.resources import IndexResource, LoginResource, RegisterResource, CreateCampaignResource, AcceptAdRequestResource,RejectAdRequestResource, GetUserProfileResource, GetInfluencerProfileResource, ViewInfluencerProfileResource, EditInfluencerProfileResource, NegotiateAdRequestResource, AddNegotiationResource, AdRequestDetailsResource, GetInfluencersResource, UpdateAdRequestResource
import requests
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import aliased

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
                session['user_id']=json_response['user_id']
                return redirect(redirect_url)
            else:
                flash(json_response.get('message', 'Login failed'))
                return redirect(url_for('login'))
        else:
            flash(response.json().get('message', 'Login failed'))
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

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

@app.route('/influencer/dashboard')
def influencer_dashboard():
    user_id = session.get('user_id')  # Assuming user_id is stored in session after login
    user = User.query.get(user_id)
    
    if not user or user.role != 'influencer':
        return redirect(url_for('login'))

    # Fetch ad requests for the logged-in influencer and include sponsor name
    ad_requests = db.session.query(
    AdRequest,
    Campaign,
    User.username.label('sponsor_name'),
    func.coalesce(Negotiations.new_amount, 0.0).label('new_amount')
    ).join(Campaign, AdRequest.campaign_id == Campaign.id
    ).join(User, Campaign.sponsor_id == User.id
    ).outerjoin(Negotiations, AdRequest.id == Negotiations.ad_id
    ).filter(
    AdRequest.influencer_id == user_id
    ).all()

    active_campaigns = []
    campaign_requests = []
    completed = []
    negotiated = []
    others = []
    current_date = datetime.utcnow()
    
    for ad_request, campaign, sponsor_name, new_amount in ad_requests:
        #if campaign.start_date <= current_date <= campaign.end_date and ad_request.status in ['Accepted']:
        if ad_request.status in ['Accepted']:
            active_campaigns.append((ad_request, campaign, sponsor_name, new_amount))
        #elif campaign.start_date <= current_date <= campaign.end_date and ad_request.status in ['Pending']:
        elif ad_request.status in ['Pending']:
            campaign_requests.append((ad_request, campaign, sponsor_name, new_amount))
        elif ad_request.status in ['Completed']:
            completed.append((ad_request, campaign, sponsor_name, new_amount))
        elif ad_request.status in ['Negotiated']:
            negotiated.append((ad_request, campaign, sponsor_name, new_amount))
        else:
            others.append((ad_request, campaign, sponsor_name, new_amount))
            
    # Calculate total earnings from completed campaigns
    total_earnings = db.session.query(db.func.sum(AdRequest.payment_amount)).filter_by(
        influencer_id=user_id,
        status='Completed'
    ).scalar() or 0.00

    return render_template('influencer_dashboard.html',
                           username=user.username,
                           active_campaigns=active_campaigns,
                           campaign_requests=campaign_requests,
                           total_earnings=total_earnings,
                           completed_campaigns=completed,
                           negotiated_requests=negotiated, 
                           title='Influencer Dashboard', 
                           active_page='profile')

@app.route('/sponsor/dashboard')
def sponsor_dashboard():
    user_id = session.get('user_id') 
    user = User.query.get(user_id)
    if not user or user.role != 'sponsor':
        return redirect(url_for('login'))
    negotiations = aliased(Negotiations)
    ad_requests = db.session.query(
        AdRequest,
        Campaign,
        User.username.label('influencer_name'),
        func.coalesce(negotiations.new_amount, 0.0).label('new_amount')
        ).join(
            Campaign,
            AdRequest.campaign_id == Campaign.id
        ).join(
            User,
            User.id == AdRequest.influencer_id
        ).outerjoin(
            negotiations,
            AdRequest.id == negotiations.ad_id
        ).filter(
            Campaign.sponsor_id == user_id 
        ).all()


    pending_requests = []
    accepted_requests = []
    rejected_requests = []
    negotiated_requests = []
    others=[]
    
    for ad_request, campaign, influencer_name, new_amount in ad_requests:
        #if campaign.start_date <= current_date <= campaign.end_date and ad_request.status in ['Accepted']:
        if ad_request.status in ['Accepted']:
            accepted_requests.append((ad_request, campaign, influencer_name, new_amount))
        #elif campaign.start_date <= current_date <= campaign.end_date and ad_request.status in ['Pending']:
        elif ad_request.status in ['Pending']:
            pending_requests.append((ad_request, campaign, influencer_name, new_amount))
        elif ad_request.status in ['Completed']:
            rejected_requests.append((ad_request, campaign, influencer_name, new_amount))
        elif ad_request.status in ['Negotiated']:
            negotiated_requests.append((ad_request, campaign, influencer_name, new_amount))
        else:
            others.append((ad_request, campaign, influencer_name, new_amount))

    return render_template('sponsor_dashboard.html',
                           username=user.username,
                           accepted_requests=accepted_requests,
                           pending_requests=pending_requests,
                           rejected_requests=rejected_requests,
                           negotiated_requests=negotiated_requests,
                           influencer_name=influencer_name, 
                           title='Sponsor Dashboard', 
                           active_page='profile')


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
api.add_resource(AcceptAdRequestResource, '/api/campaign/accept')
api.add_resource(RejectAdRequestResource, '/api/campaign/reject')
api.add_resource(GetUserProfileResource, '/api/getuser')
api.add_resource(GetInfluencerProfileResource, '/api/getinfluencer')
api.add_resource(ViewInfluencerProfileResource, '/api/fetchinfluencerprofile')
api.add_resource(EditInfluencerProfileResource, '/api/editinfluencerprofile')
api.add_resource(NegotiateAdRequestResource, '/api/campaign/negotiate')
api.add_resource(AddNegotiationResource, '/api/campaign/addnegotiation')
api.add_resource(AdRequestDetailsResource, '/api/ad-request/details/<int:ad_request_id>')
api.add_resource(GetInfluencersResource, '/api/influencers/<int:ad_request_id>')
api.add_resource(UpdateAdRequestResource, '/api/ad_requests/update/<int:ad_request_id>')
