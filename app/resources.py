from flask import jsonify, request, url_for, session
from flask_restful import Resource
from app import db
from app.models import User, Campaign, AdRequest, InfluencerProfile, Negotiations
from app.forms import LoginForm, RegistrationForm, CampaignForm

class IndexResource(Resource):
    def get(self):
        return jsonify({"message": "Welcome to the Home Page"})

class LoginResource(Resource):
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                return jsonify({"message":'Invalid username or password', "status_code":400})
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            if user.role == 'admin':
                return jsonify({"redirect_url": url_for('admin_dashboard'),"status_code":200,"user_id":user.id})
            elif user.role == 'sponsor':
                return jsonify({"redirect_url": url_for('sponsor_dashboard'),"status_code":200,"user_id":user.id})
            elif user.role == 'influencer':
                return jsonify({"redirect_url": url_for('influencer_dashboard'),"status_code":200,"user_id":user.id})
            else:
                return jsonify({"message": "Invalid username or password","status_code":401})
        
        return jsonify({"errors": form.errors,"status_code":400})

class RegisterResource(Resource):
    def post(self):
        form = RegistrationForm(request.form)
        if (User.query.filter_by(email=form.email.data).first() and User.query.filter_by(email=form.email.data).first().email == form.email.data):
            return jsonify({"message":'Email address already registered.<br>Please log in.', "status_code":400})
        
        if (User.query.filter_by(username=form.username.data).first() and User.query.filter_by(username=form.username.data).first().username == form.username.data):
            return jsonify({"message":'Username already exists.<br>Please choose a different username.', "status_code":400})
            
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify({"redirect_url": url_for('login'),"status_code":200})

class CreateCampaignResource(Resource):
    def post(self):
        form = CampaignForm(request.form)
        if form.validate():
            campaign = Campaign(
                name=form.name.data,
                description=form.description.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                budget=form.budget.data,
                visibility=form.visibility.data,
                goals=form.goals.data,
                sponsor=form.sponsor.data  # Adjust this line based on your form
            )
            db.session.add(campaign)
            db.session.commit()
            return {"message": "Campaign created successfully!"}, 201
        return {"errors": form.errors}, 400
    
class AcceptAdRequestResource(Resource):
    def post(self):
        ad_request_id = request.json.get('ad_request_id')  # Assuming ad_request_id is sent from client
        ad_request = AdRequest.query.get(ad_request_id)
        if ad_request:
            ad_request.status = 'Accepted'
            db.session.commit()
            return jsonify({'message': 'AD request accepted successfully','status_code':200})
        else:
            return jsonify({'error': 'Ad request not found','status_code':404})
        
class RejectAdRequestResource(Resource):
    def post(self):
        ad_request_id = request.json.get('ad_request_id')  
        ad_request = AdRequest.query.get(ad_request_id)
        if ad_request:
            ad_request.status = 'Rejected'
            db.session.commit()
            return jsonify({'message': 'AD Request Rejected','status_code':200})
        else:
            return jsonify({'error': 'Ad request not found','status_code':404})
        
class GetUserProfileResource(Resource):
    def post(self):
        user_id = request.json.get('user_id')
        user_request = User.query.get(user_id)
        if user_request:
            email = user_request.email
            return jsonify({'email': email,'status_code':200})
        else:
            return jsonify({'error': 'User Not Found','status_code':404})
        
class GetInfluencerProfileResource(Resource):
    def post(self):
        influencer_id = request.json.get('influencer_id')
        profiles = InfluencerProfile.query.filter_by(influencer_id=influencer_id).all()
        if not profiles:
            return jsonify({'followers': 0, 'platforms': 'None', 'niches': 'None', 'status_code':200})
        followers_sum = sum(profile.followers for profile in profiles)
        platforms = ', '.join(set(profile.platform for profile in profiles))
        niches = ', '.join(set(profile.niche for profile in profiles))
        return jsonify({'followers': followers_sum, 'platforms': platforms, 'niches': niches, 'status_code':200})
    
class ViewInfluencerProfileResource(Resource):
    def post(self):
        influencer_id = request.json.get('influencer_id')
        profiles = InfluencerProfile.query.filter_by(influencer_id=influencer_id).all()

        if not profiles:
            return jsonify({
            'profile_ids':[],
            'followers': [],
            'platforms': [],
            'niches': [],
            'status_code': 200
            })
        
        profile_ids = [profile.id for profile in profiles]
        followers = [profile.followers for profile in profiles]
        platforms = [profile.platform for profile in profiles]
        niches = [profile.niche for profile in profiles]
        return jsonify({
        'profile_ids':profile_ids,   
        'followers': followers,
        'platforms': platforms,
        'niches': niches,
        'status_code': 200
        })
    
class EditInfluencerProfileResource(Resource):
    def post(self):
        action = request.json.get('action')
        profile_id = request.json.get('profileId')
        influencer_id = request.json.get('influencer_id')
        platform = request.json.get('platform')
        niche = request.json.get('niche')
        followers = request.json.get('followers')

        if action == 'edit':
            profile = InfluencerProfile.query.filter_by(id=profile_id, influencer_id=influencer_id).first()
            if profile:
                try:
                    profile.platform = platform
                    profile.niche = niche
                    profile.followers = followers
                    db.session.commit()
                    return jsonify({'status':'success','message': 'Profile updated successfully', 'status_code': 200})
                except Exception:
                    db.session.rollback()
                    return jsonify({'status':'error','message': 'Error - Platform + Niche Combination must be unique.', 'status_code': 500})
            return jsonify({'status':'error','message': 'Profile not found', 'status_code': 404})

        elif action == 'delete':
            profile = InfluencerProfile.query.filter_by(id=profile_id, influencer_id=influencer_id).first()
            if profile:
                db.session.delete(profile)
                db.session.commit()
                return jsonify({'message': 'Profile Entry deleted successfully', 'status_code': 200})
            return jsonify({'message': 'Profile not found', 'status_code': 404})

        elif action == 'insert':
            new_profile = InfluencerProfile(
                influencer_id=influencer_id,
                platform=platform,
                niche=niche,
                followers=followers
            )
            db.session.add(new_profile)
            db.session.commit()
            return jsonify({'status':'success','message': 'Profile inserted successfully', 'status_code': 200})

        return jsonify({'status':'error','message': 'Invalid action', 'status_code': 400})
    
class NegotiateAdRequestResource(Resource):
    def post(self):
        ad_request_id = request.json.get('ad_request_id')  
        ad_request = AdRequest.query.get(ad_request_id)
        if ad_request:
            ad_request.status = 'Negotiated'
            db.session.commit()
            return jsonify({'message': 'Negotiation Initiated','status_code':200})
        else:
            return jsonify({'error': 'Ad request not found','status_code':404})
        
class AddNegotiationResource(Resource):
    def post(self):
        ad_request_id = request.json.get('ad_request_id')
        new_amount = request.json.get('new_amount')
        new_entry = Negotiations(
            ad_id=ad_request_id,
            new_amount=new_amount
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Negotiation inserted successfully', 'status_code': 200})






