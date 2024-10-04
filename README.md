# Influencer Engagement and Sponsorship Coordination Platform (IESCP)

The **Influencer Engagement and Sponsorship Coordination Platform** (IESCP) connects sponsors with influencers, enabling streamlined advertisement campaigns where sponsors can promote their products or services and influencers earn monetary benefits. <br>
[Click Here to View Demo](https://www.youtube.com/watch?v=zogw1-0ZPSs)

## Features
- **User Roles**: Tailored dashboards for:
  - **Admins**: Manage platform-wide activities.
  - **Sponsors**: Create and manage ad campaigns, submit ad requests, and negotiate with influencers.
  - **Influencers**: Respond to ad requests and manage campaign participation.
  
- **Campaign Management**: Create, update, and track advertisement campaigns.
- **Ad Requests**: Handle the submission, acceptance, rejection, and negotiation of ad requests between sponsors and influencers.
- **Negotiations**: Enable sponsors and influencers to negotiate terms for ad campaigns.
- **Advanced Filtering & Search**: Find relevant influencers and sponsors based on detailed criteria.

## Key Technologies
- **Flask**: Web framework used for routing and templating.
- **SQLAlchemy**: ORM for database interactions.
- **Flask-RESTful**: Creating RESTful APIs for CRUD operations.
- **Jinja2**: Template engine for rendering dynamic HTML pages.
- **Requests**: Handles HTTP requests to APIs.

## ER Diagram
![ER](https://github.com/user-attachments/assets/8d89f4a4-cc07-4eb6-a83f-8b95ae1ab3b5)

## API Endpoints

### Authentication
- `POST /api/login`: Logs in users and provides authentication tokens.
- `POST /api/register`: Registers a new user account.

### Campaign Management
- `POST /api/campaign/accept`: Accept an ad request for a campaign.
- `POST /api/campaign/reject`: Reject an ad request for a campaign.
- `GET /api/campaign/<int:campaign_id>`: Retrieves detailed information about a specific campaign.
- `PUT /api/campaign/update/<int:campaign_id>`: Updates a specific campaign.
- `DELETE /api/campaign/delete/<int:campaign_id>`: Deletes a campaign.

### Ad Requests
- `GET /api/ad-request/details/<int:ad_request_id>`: Retrieves ad request details.
- `PUT /api/ad_requests/update/<int:ad_request_id>`: Updates ad request details.
- `DELETE /api/ad_requests/delete/<int:ad_request_id>`: Deletes an ad request.

### User & Influencer Management
- `GET /api/getuser`: Retrieves user information.
- `GET /api/getinfluencer`: Retrieves influencer information.
- `PUT /api/editinfluencerprofile`: Edits an influencer's profile.
- `GET /api/influencers/<int:ad_request_id>`: Lists influencers related to an ad request.
- `GET /api/influencer/getall`: Retrieves a list of all influencers.

### Miscellaneous
- `GET /api/get_users`: Retrieves a list of users.
- `POST /api/flag_user`: Flags a user for moderation.
- `GET /api/get_all_flagged_users`: Retrieves a list of flagged users.

## Screenshots
![image](https://github.com/user-attachments/assets/0e7608f4-747a-4f8a-a2dc-173ebfbe8aba)
![image](https://github.com/user-attachments/assets/6c57c468-b385-458d-8326-d49904eeacd6)
![image](https://github.com/user-attachments/assets/d6269b53-3e1b-4749-89cb-b4dbcbf6088e)
![image](https://github.com/user-attachments/assets/c93b3688-eec3-4923-a871-fb61a7568a1d)



