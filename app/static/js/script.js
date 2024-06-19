$(document).ready(function() {
    $('#campaignModal').on('show.bs.modal', function (event) {
        try {
            var button = $(event.relatedTarget); 
            var campaignName = button.data('campaign-name');
            var sponsorName = button.data('sponsor-name');
            var campaignDescription = button.data('campaign-description');
            var campaignRequirements = button.data('campaign-requirements');
            var campaignPayment = 'Rs. '+button.data('campaign-payment');
            var campaignStatus = button.data('campaign-status');
            var campaignMessages = button.data('campaign-messages');

            var modal = $(this);
            modal.find('#modal-campaign-name').text(campaignName);
            modal.find('#modal-sponsor-name').text(sponsorName);
            modal.find('#modal-campaign-description').text(campaignDescription);
            modal.find('#modal-campaign-requirements').text(campaignRequirements);
            modal.find('#modal-campaign-payment').text(campaignPayment);
            modal.find('#modal-campaign-status').text(campaignStatus);
            modal.find('#modal-campaign-messages').text(campaignMessages);
        } catch (error) {
            console.error('Error populating modal:', error);
        }
    });
});

$(document).ready(function() {
    $('#adModal').on('show.bs.modal', function (event) {
        try {
            var button = $(event.relatedTarget); 
            var campaignName = button.data('campaign-name');
            var sponsorName = button.data('sponsor-name');
            var campaignDescription = button.data('campaign-description');
            var campaignRequirements = button.data('campaign-requirements');
            var campaignPayment = 'Rs. '+button.data('campaign-payment');

            var modal = $(this);
            modal.find('#modal-campaign-name').text(campaignName);
            modal.find('#modal-sponsor-name').text(sponsorName);
            modal.find('#modal-campaign-description').text(campaignDescription);
            modal.find('#modal-campaign-requirements').text(campaignRequirements);
            modal.find('#modal-campaign-payment').text(campaignPayment);
        } catch (error) {
            console.error('Error populating modal:', error);
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.btn-accept');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var adRequestId = this.getAttribute('data-ad-request-id');
            var apiUrl = '/api/campaign/accept';
            var requestData = {
                ad_request_id: adRequestId
            };

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(function(data) {
                showNotification(data.message || 'Ad request accepted successfully', 'success');
                setTimeout(function() {
                    location.reload();
                }, 2000); 
            })
            .catch(function(error) {
                console.error('Error accepting ad request:', error);
                showNotification('Error accepting ad request', 'error');
            });
        });
    });
    function showNotification(message, type) {
        var notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = 'notification ' + (type || 'success');
        notification.style.display = 'block';
        setTimeout(function() {
            notification.style.display = 'none';
        }, 6000); 
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.btn-reject');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var adRequestId = this.getAttribute('data-ad-request-id');
            var apiUrl = '/api/campaign/reject';
            var requestData = {
                ad_request_id: adRequestId
            };

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(function(data) {
                showNotification(data.message || 'AD Request Rejected', 'error');
                setTimeout(function() {
                    location.reload();
                }, 2000); 
            })
            .catch(function(error) {
                console.error('Error rejecting ad request:', error);
                showNotification('Error rejecting ad request', 'error');
            });
        });
    });
    function showNotification(message, type) {
        var notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = 'notification ' + (type || 'error');
        notification.style.display = 'block';
        setTimeout(function() {
            notification.style.display = 'none';
        }, 6000); 
    }
});

 document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('profile-link').addEventListener('click', function(event) {
            event.preventDefault();
            var userId = this.getAttribute('data-user_id');
            var apiUrl = '/api/getuser';
            var requestData = {
                user_id: userId
            };
            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(function(data) {
                    document.getElementById('modal-email').textContent = data.email;
                })
                .catch(function(error) {
                    console.error('Error fetching user data:', error);
                });
        });
    });

