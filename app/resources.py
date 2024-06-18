from flask import jsonify, request, url_for, session
from flask_restful import Resource
from app import db
from app.models import User, Campaign
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
                return jsonify({"redirect_url": url_for('admin_dashboard'),"status_code":200})
            elif user.role == 'sponsor':
                return jsonify({"redirect_url": url_for('sponsor_dashboard'),"status_code":200})
            elif user.role == 'influencer':
                return jsonify({"redirect_url": url_for('influencer_dashboard'),"status_code":200})
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


class AdminDashboardResource(Resource):
    def get(self):
        # Implement admin dashboard view logic here
        return {"message": "Admin Dashboard"}

class SponsorDashboardResource(Resource):
    def get(self):
        # Implement sponsor dashboard view logic here
        return {"message": "Sponsor Dashboard"}

class InfluencerDashboardResource(Resource):
    def get(self):
        # Implement influencer dashboard view logic here
        return {"message": "Influencer Dashboard"}

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
