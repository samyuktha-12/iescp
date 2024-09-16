# app/routes.py
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from app import app, db, api
from app.forms import LoginForm, RegistrationForm, CampaignForm
from app.models import User, Campaign, AdRequest, Negotiations, InfluencerProfile
from app.resources import IndexResource, LoginResource, RegisterResource, GetAllInfluencersResource, AcceptAdRequestResource,RejectAdRequestResource, GetUserProfileResource, GetInfluencerProfileResource, ViewInfluencerProfileResource, EditInfluencerProfileResource, NegotiateAdRequestResource, AddNegotiationResource, AdRequestDetailsResource, GetInfluencersResource, UpdateAdRequestResource, DeleteAdRequestResource, CampaignDetailsResource, DeleteCampaignResource, UpdateCampaignResource
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
                session['role']=json_response['role']
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


@app.route('/campaigns')
def campaigns():
    sponsor_id = request.args.get('sponsor_id')
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
    return render_template('campaigns.html', active_page='campaigns', campaigns=campaigns, sponsor_id=sponsor_id)

@app.route('/find_influencer')
def find_influencer():
    # Get filter values from query parameters
    niche_filter = request.args.get('niche', '').lower()
    platform_filter = request.args.get('platform', '').lower()
    selected_niche = request.args.get('niche', '')
    selected_platform = request.args.get('platform', '')

    # Perform a join to get user information along with influencer profiles
    profiles_query = db.session.query(
        InfluencerProfile,
        User.username.label('user_name')
    ).join(User, InfluencerProfile.influencer_id == User.id)

    profiles = profiles_query.all()

    # Aggregate followers by influencer_id, platform, and niche
    aggregated_data = {}
    for profile, user_name in profiles:
        influencer_id = profile.influencer_id
        if influencer_id not in aggregated_data:
            aggregated_data[influencer_id] = {
                'username': user_name,
                'total_followers': 0,
                'platforms': {}
            }
        
        # Initialize platform if not already present
        if profile.platform not in aggregated_data[influencer_id]['platforms']:
            aggregated_data[influencer_id]['platforms'][profile.platform] = {
                'total_followers': 0,
                'niches': {}
            }
        
        # Update total followers for the platform and niche
        aggregated_data[influencer_id]['total_followers'] += profile.followers
        platform_data = aggregated_data[influencer_id]['platforms'][profile.platform]
        platform_data['total_followers'] += profile.followers
        
        if profile.niche not in platform_data['niches']:
            platform_data['niches'][profile.niche] = 0
        platform_data['niches'][profile.niche] += profile.followers

    # Prepare data to be passed to the template
    profiles_data = []
    for influencer_id, data in aggregated_data.items():
        platforms_data = []
        for platform, platform_data in data['platforms'].items():
            niches_data = [{'niche': niche, 'followers': followers} for niche, followers in platform_data['niches'].items()]
            platforms_data.append({
                'platform': platform,
                'total_followers': platform_data['total_followers'],
                'niches': niches_data
            })
        
        profiles_data.append({
            'influencer_id': influencer_id,
            'username': data['username'],
            'total_followers': data['total_followers'],
            'platforms': platforms_data
        })

    if niche_filter:
        profiles_data = [
            {
                **profile,  # Copy all original profile data
                'platforms': [
                    {
                        **platform,  # Copy all original platform data
                        'niches': [
                            n  # Keep only the niche matching niche_filter
                            for n in platform['niches']
                            if n['niche'].lower() == niche_filter.lower()
                        ]
                    }
                    for platform in profile['platforms']
                    if any(n['niche'].lower() == niche_filter.lower() for n in platform['niches'])
                ]
            }
            for profile in profiles_data
            if any(
                niche['niche'].lower() == niche_filter.lower()
                for platform in profile['platforms']
                for niche in platform['niches']
            )
        ]

    if platform_filter:
        profiles_data = [
            {
                **profile,  # Copy all original profile data
                'platforms': [
                    {
                        **platform,  # Copy all original platform data
                        'niches': platform['niches']  # Keep all niches as is for the filtered platform
                    }
                    for platform in profile['platforms']
                    if platform['platform'].lower() == platform_filter.lower()
                ]
            }
            for profile in profiles_data
            if any(
                platform['platform'].lower() == platform_filter.lower()
                for platform in profile['platforms']
            )
        ]
    return render_template('find_influencer.html', active_page='find', profiles=profiles_data, selected_niche=selected_niche, selected_platform=selected_platform)

@app.route('/find_sponsor')
def find_sponosr():
    return render_template('find_sponsor.html', active_page='find')

@app.route('/campaign')
def campaign():
    campaign_id = request.args.get('campaign_id')
    campaign = Campaign.query.get(campaign_id)
    ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
    ad_requests_with_influencer = []
    for ad_request in ad_requests:
        influencer = User.query.get(ad_request.influencer_id)
        influencer_name = influencer.username if influencer else "Unknown"
        ad_requests_with_influencer.append({
            'campaign_id': campaign_id,
            'ad_request_id': ad_request.id,
            'ad_request_payment': ad_request.payment_amount,
            'influencer_name': influencer_name,
            'requirements': ad_request.requirements,
            'status': ad_request.status,
            'messages': ad_request.messages
        })
    
    return render_template('campaign.html', active_page='campaigns', campaign=campaign, campaign_id=campaign_id, ad_requests=ad_requests_with_influencer)

@app.route('/api/campaigns/create', methods=['POST'])
def create_campaign():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    budget = data.get('budget')
    visibility = data.get('visibility')
    goals = data.get('goals')
    sponsor_id = data.get('sponsor_id')

    if not all([name, description, start_date_str, end_date_str, budget, visibility, goals, sponsor_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Convert date strings to datetime objects
        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    # Check if a similar campaign already exists
    existing_campaign = db.session.query(Campaign).filter_by(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        visibility=visibility,
        goals=goals,
        sponsor_id=sponsor_id
    ).first()

    if existing_campaign:
        return jsonify({"error": "A similar campaign already exists"}), 400

    # Create the new campaign
    campaign = Campaign(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        visibility=visibility,
        goals=goals,
        sponsor_id=sponsor_id
    )

    try:
        db.session.add(campaign)
        db.session.commit()
        return jsonify({"message": "Campaign created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/api/campaign/create', methods=['POST'])
def create_ad_request():
    data = request.get_json()

    campaign_id=data.get('campaign_id')
    influencer_id = data.get('influencer_id')
    messages = data.get('messages')
    requirements = data.get('requirements')
    payment_amount = data.get('payment_amount')
    status = data.get('status')


    if not all([campaign_id, influencer_id, messages, requirements, payment_amount, status]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if a similar campaign already exists
    existing_ad_request = db.session.query(AdRequest).filter_by(
        campaign_id=campaign_id,
        influencer_id=influencer_id,
    ).first()

    if existing_ad_request:
        return jsonify({"error": "A similar campaign already exists"}), 400

    # Create the new campaign
    ad_request = AdRequest(
        campaign_id=campaign_id,
        influencer_id=influencer_id,
        messages=messages,
        requirements=requirements,
        payment_amount=payment_amount,
        status=status
    )

    try:
        db.session.add(ad_request)
        db.session.commit()
        return jsonify({"message": "Ad Request created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Add API resource routes
api.add_resource(IndexResource, '/api/')
api.add_resource(LoginResource, '/api/login')
api.add_resource(RegisterResource, '/api/register')
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
api.add_resource(GetAllInfluencersResource, '/api/influencer/getall')
api.add_resource(DeleteAdRequestResource, '/api/ad_requests/delete/<int:ad_request_id>')
api.add_resource(CampaignDetailsResource, '/api/campaign/<int:campaign_id>')
api.add_resource(DeleteCampaignResource, '/api/campaign/delete/<int:campaign_id>')
api.add_resource(UpdateCampaignResource, '/api/campaign/update/<int:campaign_id>')
