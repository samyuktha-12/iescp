from flask import jsonify, request, url_for, session
from flask_restful import Resource
from app import db
from app.models import User, Campaign, AdRequest, InfluencerProfile, Negotiations, FlaggedUsers
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
                return jsonify({"redirect_url": url_for('admin_dashboard', role=user.role),"status_code":200,"user_id":user.id,"role":user.role})
            elif user.role == 'sponsor':
                return jsonify({"redirect_url": url_for('sponsor_dashboard', role=user.role),"status_code":200,"user_id":user.id, "role":user.role})
            elif user.role == 'influencer':
                return jsonify({"redirect_url": url_for('influencer_dashboard', role=user.role),"status_code":200,"user_id":user.id, "role":user.role})
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
        data = request.get_json() 

        name = data.get('name')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        budget = data.get('budget')
        visibility = data.get('visibility')
        goals = data.get('goals')
        sponsor_id = data.get('sponsor_id') 

        if not all([name, description, start_date, end_date, budget, visibility, goals, sponsor_id]):
            return jsonify({"errors": "Missing required fields"}), 400

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
            return jsonify({"errors": str(e)}), 400

class AcceptAdRequestResource(Resource):
    def post(self):
        ad_request_id = request.json.get('ad_request_id')  
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
    
class AdRequestDetailsResource(Resource):
    def get(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        campaign = Campaign.query.get_or_404(ad_request.campaign_id)
        return jsonify({
            'campaign_name': campaign.name,
        })
    
class GetInfluencersResource(Resource):
    def get(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        influencers = User.query.filter_by(role='influencer').all()
        return jsonify({
            'influencers': [{'id': influencer.id, 'username': influencer.username} for influencer in influencers],
            'assigned_influencer': ad_request.influencer_id
        })
    
class GetAllInfluencersResource(Resource):
    def get(self):
        influencers = User.query.filter_by(role='influencer').all()
        return jsonify({
            'influencers': [{'id': influencer.id, 'username': influencer.username} for influencer in influencers]
        })

class UpdateAdRequestResource(Resource):
    def post(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        
        data = request.get_json()
        
        ad_request.messages = data.get('messages', ad_request.messages)
        ad_request.requirements = data.get('requirements', ad_request.requirements)
        ad_request.payment_amount = data.get('paymentAmount', ad_request.payment_amount)
        
        try:
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 400

class DeleteAdRequestResource(Resource):
    def post(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        try:
            db.session.delete(ad_request)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 400
        
class CampaignDetailsResource(Resource):
    def get(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        print(campaign.name)
        return jsonify({
            'campaign_name': campaign.name,
            'campaign_description': campaign.description,
            'campaign_start_date': campaign.start_date.strftime('%d-%m-%Y') if campaign.start_date else None,
            'campaign_end_date': campaign.end_date.strftime('%d-%m-%Y') if campaign.end_date else None,
            'campaign_budget': campaign.budget,
            'campaign_visibility': campaign.visibility,
            'campaign_goals': campaign.goals,
        })
    
class DeleteCampaignResource(Resource):
    def post(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        subquery = (
            db.session.query(AdRequest.id)
            .filter(AdRequest.campaign_id == campaign_id)
            .subquery()
        )
        try:
            db.session.query(Negotiations).filter(Negotiations.ad_id.in_(subquery)).delete(synchronize_session=False)
            AdRequest.query.filter_by(campaign_id=campaign_id).delete()
            db.session.delete(campaign)
            db.session.commit()
            response = jsonify({'success': True})
            return response
        except Exception as e:
            response = jsonify({'success': False, 'error': str(e)}) 
            return response, 400
        
class UpdateCampaignResource(Resource):
    def post(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        
        data = request.get_json()

        new_name = data.get('campaignName')
        new_goals = data.get('goals', campaign.goals)
        new_visibility = data.get('visibility', campaign.visibility)
        new_budget = data.get('budget', campaign.budget)

        campaign.name = new_name if new_name else campaign.name
        campaign.goals = new_goals
        campaign.visibility = new_visibility
        campaign.budget = new_budget

        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Campaign updated successfully!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

class GetUserResource(Resource):
    def get(self):
        users = User.query.filter(User.role!='admin').all()
        return jsonify({
            'users': [{'id': user.id, 'username': user.username} for user in users]
        })

class FlagUserResource(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        username = data.get('username')
        existing_flagged_user = FlaggedUsers.query.filter_by(id=user_id).first()
        if existing_flagged_user:
            return jsonify({'success': False, 'message': 'User is already flagged'}), 400
        flagged_user = FlaggedUsers(id=user_id, username=username)
        db.session.add(flagged_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User flagged successfully'})
    
class GetAllFlaggedUsersResource(Resource):
    def get(self):
        flagged_users = FlaggedUsers.query.all()
        users = [{'id': user.id, 'username': user.username} for user in flagged_users]
        return jsonify(users)
        


        
    






