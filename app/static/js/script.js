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

    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('profile-link').addEventListener('click', function(event) {
            event.preventDefault();
            var userId = this.getAttribute('data-user_id');
            var apiUrl = '/api/getinfluencer';  
            var requestData = {
                influencer_id: userId  
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
                
                document.getElementById('modal-followers').textContent = data.followers;
                document.getElementById('modal-niches').textContent = data.niches;
                document.getElementById('modal-platforms').textContent = data.platforms;

                $('#profileModal').modal('show');
            })
            .catch(function(error) {
                console.error('Error fetching influencer data:', error);
            });
        });
    });
    
    document.addEventListener('DOMContentLoaded', function() {
        let influencerData = {
            followers: [],
            platforms: [],
            niches: [],
            profile_ids: []
        };

        document.querySelector('.btn-edit').addEventListener('click', function() {
            $('#profileModal').modal('hide');
            var userId = document.getElementById('profile-link').getAttribute('data-user_id');
            var apiUrl = '/api/fetchinfluencerprofile';  
            
            var requestData = {
                influencer_id: userId
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
                influencerData.profile_ids = data.profile_ids || [];
                influencerData.followers = data.followers || [];
                influencerData.platforms = data.platforms || [];
                influencerData.niches = data.niches || [];
                var tableBody = document.getElementById('profile-table-body');
                tableBody.innerHTML = '';
                
                for (var i = 0; i < influencerData.followers.length; i++) {
                    var row = document.createElement('tr');
                    row.innerHTML = `
                        <td style="text-align: center;">${influencerData.platforms[i]}</td>
                        <td style="text-align: center;">${influencerData.niches[i]}</td>
                        <td style="text-align: center;">${influencerData.followers[i]}</td>
                        <td style="text-align: center;">
                            <button type="button" class="btn btn-sm btn-edit-profile" data-index="${i}">&#9998;</button>
                            <button type="button" class="btn btn-sm btn-delete-profile" data-index="${i}">&#10060;</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                }
                    var emptyRow = document.createElement('tr');
                    emptyRow.innerHTML = `
                        <td style="text-align: center;">Select</td>
                        <td style="text-align: center;">Select</td>
                        <td style="text-align: center;">0</td>
                        <td style="text-align: center;">
                            <button type="button" class="btn btn-sm btn-insert-profile">&#x2795;</button>
                        </td>
                    `;
                    tableBody.appendChild(emptyRow);
                $('#editModal').modal('show');
            })
            .catch(function(error) {
                console.error('Error fetching influencer data:', error);
            });
        });

        document.getElementById('profile-table-body').addEventListener('click', function(event) {
            if (event.target.classList.contains('btn-edit-profile')) {
                var rowIndex = event.target.getAttribute('data-index');
                var platform = influencerData.platforms[rowIndex];
                var niche = influencerData.niches[rowIndex];
                var followers = influencerData.followers[rowIndex];
                var userId = document.getElementById('profile-link').getAttribute('data-user_id'); 

                var row = event.target.closest('tr');
                row.innerHTML = `
                    <td style="text-align: center;">
                        <select id="edit-platform-${rowIndex}">
                            <option value="YouTube" ${platform === 'YouTube' ? 'selected' : ''}>YouTube</option>
                            <option value="Instagram" ${platform === 'Instagram' ? 'selected' : ''}>Instagram</option>
                            <option value="TikTok" ${platform === 'TikTok' ? 'selected' : ''}>TikTok</option>
                            <option value="Facebook" ${platform === 'Facebook' ? 'selected' : ''}>Facebook</option>
                            <option value="Twitter" ${platform === 'Twitter' ? 'selected' : ''}>Twitter</option>
                            <option value="LinkedIn" ${platform === 'LinkedIn' ? 'selected' : ''}>Linkedin</option>
                        </select>
                    </td>
                    <td style="text-align: center;">
                        <select id="edit-niche-${rowIndex}">
                            <option value="Cooking" ${niche === 'Cooking' ? 'selected' : ''}>Cooking</option>
                            <option value="Fashion" ${niche === 'Fashion' ? 'selected' : ''}>Fashion</option>
                            <option value="Fitness" ${niche === 'Fitness' ? 'selected' : ''}>Fitness</option>
                            <option value="Travel" ${niche === 'Travel' ? 'selected' : ''}>Travel</option>
                            <option value="Education" ${niche === 'Travel' ? 'Education' : ''}>Education</option>
                            <option value="Lifestyle" ${niche === 'Lifestyle' ? 'selected' : ''}>Lifestyle</option>
                        </select>
                    </td>
                    <td style="text-align: center;">
                        <input type="number" id="edit-followers-${rowIndex}" value="${followers}">
                    </td>
                    <td style="text-align: center;">
                        <button type="button" class="btn btn-sm btn-save-profile" data-index="${rowIndex}">&#10004;</button>
                    </td>

                `;
            }

            if (event.target.classList.contains('btn-save-profile')) {
                var rowIndex = event.target.getAttribute('data-index');
                var platform = document.getElementById(`edit-platform-${rowIndex}`).value;
                var niche = document.getElementById(`edit-niche-${rowIndex}`).value;
                var followers = document.getElementById(`edit-followers-${rowIndex}`).value;
                var userId = document.getElementById('profile-link').getAttribute('data-user_id'); 

                var requestData = {
                    action: 'edit',
                    profileId: influencerData.profile_ids[rowIndex],
                    influencer_id: userId,
                    platform: platform,
                    niche: niche,
                    followers: followers
                };

                console.log(requestData);

                fetch('/api/editinfluencerprofile', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status == "success"){
                        showNotification(data.message , 'success');
                        document.querySelector('.btn-edit').click();
                    }
                    else{
                        showNotification(data.message , 'error');
                        document.querySelector('.btn-edit').click();
                    }
                })
                .catch(error => console.error('Error editing profile:', error));
            }

            if (event.target.classList.contains('btn-delete-profile')) {
                var rowIndex = event.target.getAttribute('data-index');
                var userId = document.getElementById('profile-link').getAttribute('data-user_id'); 

                var requestData = {
                    action: 'delete',
                    influencer_id: userId,
                    profileId:influencerData.profile_ids[rowIndex]
                };

                fetch('/api/editinfluencerprofile', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                })
                .then(response => response.json())
                .then(data => {
                    showNotification(data.message , 'error');
                    document.querySelector('.btn-edit').click();
                })
                .catch(error => console.error('Error deleting profile:', error));
            }

            if (event.target.classList.contains('btn-insert-profile')) {
                console.log("Button Clicked");
                var rowIndex = event.target.getAttribute('data-index');
                var platform = influencerData.platforms[rowIndex];
                var niche = influencerData.niches[rowIndex];
                var followers = influencerData.followers[rowIndex];
                var userId = document.getElementById('profile-link').getAttribute('data-user_id'); 
                var row = event.target.closest('tr');
    
                    row.innerHTML = `
                        <td style="text-align: center;">
                            <select id="edit-platform-${rowIndex}">
                                <option value="Select" ${platform === '' ? 'selected' : ''}>Select</option>
                                <option value="YouTube" ${platform === 'YouTube' ? 'selected' : ''}>YouTube</option>
                                <option value="Instagram" ${platform === 'Instagram' ? 'selected' : ''}>Instagram</option>
                                <option value="TikTok" ${platform === 'TikTok' ? 'selected' : ''}>TikTok</option>
                                <option value="Facebook" ${platform === 'Facebook' ? 'selected' : ''}>Facebook</option>
                                <option value="Twitter" ${platform === 'Twitter' ? 'selected' : ''}>Twitter</option>
                                <option value="LinkedIn" ${platform === 'LinkedIn' ? 'selected' : ''}>Linkedin</option>
                            </select>
                        </td>
                        <td style="text-align: center;">
                            <select id="edit-niche-${rowIndex}">
                                <option value="Select" ${platform === '' ? 'selected' : ''}>Select</option>
                                <option value="Cooking" ${niche === 'Cooking' ? 'selected' : ''}>Cooking</option>
                                <option value="Fashion" ${niche === 'Fashion' ? 'selected' : ''}>Fashion</option>
                                <option value="Fitness" ${niche === 'Fitness' ? 'selected' : ''}>Fitness</option>
                                <option value="Travel" ${niche === 'Travel' ? 'selected' : ''}>Travel</option>
                                <option value="Education" ${niche === 'Travel' ? 'Education' : ''}>Education</option>
                                <option value="Lifestyle" ${niche === 'Lifestyle' ? 'selected' : ''}>Lifestyle</option>
                            </select>
                        </td>
                        <td style="text-align: center;">
                            <input type="number" id="edit-followers-${rowIndex}" value="0">
                        </td>
                        <td style="text-align: center;">
                            <button type="button" class="btn btn-sm btn-insert-save-profile" data-index="${rowIndex}">&#10004;</button>
                        </td>
    
                    `;
                }
    
                if (event.target.classList.contains('btn-insert-save-profile')) {
                    var rowIndex = event.target.getAttribute('data-index');
                    var platform = document.getElementById(`edit-platform-${rowIndex}`).value;
                    var niche = document.getElementById(`edit-niche-${rowIndex}`).value;
                    var followers = document.getElementById(`edit-followers-${rowIndex}`).value;
                    var userId = document.getElementById('profile-link').getAttribute('data-user_id'); 
    
                    if(platform=='Select' || niche=='Select'){
                        showNotification("Platform and Niche must be selected" , 'error');
                        return
                    }
    
                    var requestData = {
                        action: 'insert',
                        profileId: 0,
                        influencer_id: userId,
                        platform: platform,
                        niche: niche,
                        followers: followers
                    };
    
                    fetch('/api/editinfluencerprofile', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(requestData)
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status == "success"){
                            showNotification(data.message , 'success');
                            document.querySelector('.btn-edit').click();
                        }
                        else{
                            showNotification(data.message , 'error');
                            document.querySelector('.btn-edit').click();
                        }
                    })
                    .catch(error => console.error('Error editing profile:', error));
                }

        
        });

        function showNotification(message, type) {
            var notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = 'notification ' + (type || 'error');
            notification.style.display = 'block';
            setTimeout(function() {
                notification.style.display = 'none';
            }, 5000); 
        }

    });

    document.addEventListener('DOMContentLoaded', function() {
        var negotiateButtons = document.querySelectorAll('.btn-negotiate');
        var closeButtons = document.querySelectorAll('.btn-close');
    
        negotiateButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                console.log("Negotiate Button Clicked");
                var requestId = this.getAttribute('data-ad-request-id');
                console.log(requestId);
                var negotiateSection = document.getElementById('negotiate-section-' + requestId);
                negotiateSection.style.display = 'block';
            });
        });
    
        closeButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                var requestId = this.closest('.negotiate-section').getAttribute('id').split('-')[2];
                var negotiateSection = document.getElementById('negotiate-section-' + requestId);
                negotiateSection.style.display = 'none';
            });
        });
    
        // Prevent form submission for demonstration purposes
        document.querySelectorAll('.negotiation-form').forEach(function(form) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                var newAmount = this.querySelector('input[name="new-amount"]').value;
                var requestId = this.closest('.negotiate-section').getAttribute('id').split('-')[2];
                var negotiateSection = document.getElementById('negotiate-section-' + requestId);
                negotiateSection.style.display = 'none';
                var apiUrl = '/api/campaign/negotiate';
                var requestData = {
                ad_request_id: requestId
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
                    showNotification(data.message || 'Negotiation Initiated', 'success');
                    setTimeout(function() {
                        location.reload();
                    }, 2000); 
                })
                .catch(function(error) {
                    console.error('Error Initiating Negotiation', error);
                    showNotification('Error Initiating Negotiation', 'error');

                });
                function showNotification(message, type) {
                    var notification = document.getElementById('notification');
                    notification.textContent = message;
                    notification.className = 'notification ' + (type || 'error');
                    notification.style.display = 'block';
                    setTimeout(function() {
                        notification.style.display = 'none';
                    }, 5000); 
                }

            });
        });

        document.querySelectorAll('.negotiation-form').forEach(function(form) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                var newAmount = this.querySelector('input[name="new-amount"]').value;
                var requestId = this.closest('.negotiate-section').getAttribute('id').split('-')[2];
                var negotiateSection = document.getElementById('negotiate-section-' + requestId);
                negotiateSection.style.display = 'none';
                var apiUrl = '/api/campaign/addnegotiation';
                var requestData = {
                ad_request_id: requestId,
                new_amount: newAmount
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
                    console.log(data.message);
                })
                .catch(function(error) {
                    console.error('Error Initiating Negotiation', error);
                });

            });
        });
    });
    
    
    

    
    
    
    
