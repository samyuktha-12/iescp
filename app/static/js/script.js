document.addEventListener("DOMContentLoaded", function() {
    // Fetch influencers and populate dropdown
    fetch('/api/influencer/getall')
        .then(response => response.json())
        .then(data => {
            const influencerSelect = document.getElementById('influencerId');
            data.influencers.forEach(influencer => {
                const option = document.createElement('option');
                option.value = influencer.id;
                option.textContent = influencer.username;
                influencerSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching influencers:', error);
        });

    document.getElementById('addAd').addEventListener('click', function() {
        const form = document.getElementById("createAdForm");
        const formData = new FormData(form);
        const formDataObject = {};
        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });
        const campaignId = this.getAttribute("data-campaign-id");
        const adJson = {
            messages: formDataObject.messages,
            requirements: formDataObject.requirements,
            payment_amount: formDataObject.payment_amount,
            status: "Pending",
            campaign_id: parseInt(campaignId, 10), // Ensure campaign_id is a number
            influencer_id: parseInt(formDataObject.influencer_id, 10) // Ensure influencer_id is a number
        };
        console.log(adJson);

        fetch('/api/campaign/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(adJson)
        })
        .then(response => {
            // Check if the response is OK (status code 200-299)
            if (response.ok) {
                return response.json(); // Parse JSON if response is OK
            } else {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'An error occurred'); // Throw error if response is not OK
                });
            }
        })
        .then(data => {
            showNotification(data.message || 'Ad Request created successfully!', 'success');
            setTimeout(function() {
                $('#createAdModal').modal('hide'); 
                location.reload();
            }, 1000); 
        })
        .catch(error => {
            console.error('Error creating Ad Request:', error);
            showNotification(error.message || 'Error creating Ad Request', 'error');
        });

        function showNotification(message, type) {
            var notification = document.getElementById('notification');
            if (notification) {
                notification.textContent = message;
                notification.className = 'notification ' + (type || 'error');
                notification.style.display = 'block';
                setTimeout(function() {
                    notification.style.display = 'none';
                }, 1000);
            } else {
                console.error('Notification element not found');
            }
        }
    });

    document.getElementById('edit-ad-request').addEventListener('click', function() {
            var adRequestId = this.getAttribute('data-ad-request-id');
            var campaignName = this.getAttribute('data-campaign-name');
            var messages = this.getAttribute('data-messages');
            var requirements = this.getAttribute('data-requirements');
            var payment = this.getAttribute('data-payment-amount');
            var campaignName = this.getAttribute('data-campaign-name');
        
            console.log("EDIT CLICKED");

            document.getElementById('adRequestId').value = adRequestId;
            document.getElementById('campaignName').value = campaignName;
            document.getElementById('messages').value = messages;
            document.getElementById('requirements').value = requirements;
            document.getElementById('payment').value = payment;

                fetch(`/api/influencers/${adRequestId}`)
                .then(response => response.json())
                .then(data => {
                    const influencerSelect = document.getElementById('influencer');
                    influencerSelect.innerHTML = ''; 
                    data.influencers.forEach(influencer => {
                        const option = document.createElement('option');
                        option.value = influencer.id;
                        option.textContent = influencer.username;
                        influencerSelect.appendChild(option);
                    });

                    influencerSelect.value = data.assigned_influencer || '';

                    $('#editAdRequestModal').modal('show');
                })
                .catch(error => console.error('Error fetching influencers:', error));

    });

    document.getElementById('delete-ad-request').addEventListener('click', function() {
        var adRequestId = this.getAttribute('data-ad-request-id');
        var campaignName = this.getAttribute('data-campaign-name');
        document.getElementById('adRequestId').value = adRequestId;
        document.getElementById('campaignName').value = campaignName;
        $('#deleteAdModal').modal('show');
        console.log("DELETE CLICKED");
    });
});

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('addCampaign').addEventListener('click', function() {
        // Get the form data
        const form = document.getElementById("createCampaignForm");
        const formData = new FormData(form);
        const formDataObject = {};
        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });

        // Get sponsor ID from the button's data attribute
        const sponsorId = this.getAttribute("data-sponsor-id");

        // Construct the campaign JSON object
        const campaignJson = {
            name: formDataObject.name,
            description: formDataObject.description,
            start_date: formDataObject.start_date,  // Ensure format is correct
            end_date: formDataObject.end_date,      // Ensure format is correct
            budget: parseFloat(formDataObject.budget), // Ensure budget is a number
            visibility: formDataObject.visibility,
            goals: formDataObject.goals,
            sponsor_id: parseInt(sponsorId, 10) // Ensure sponsor_id is a number
        };

        // API URL
        const apiUrl = '/api/campaigns/create';

        // Send data to the server
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(campaignJson)
        })
        .then(function(response) {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Network response was not ok');
                });
            }
            return response.json();
        })
        .then(function(data) {
            showNotification(data.message || 'Campaign created successfully!', 'success');
            setTimeout(function() {
                $('#createCampaignModal').modal('hide'); // Hide modal
                location.reload(); // Reload the page to reflect changes
            }, 100); 
        })
        .catch(function(error) {
            console.error('Error creating campaign:', error);
            showNotification(error.message || 'Error creating campaign', 'error');
        });

        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = 'notification ' + (type || 'error');
            notification.style.display = 'block';
            setTimeout(function() {
                notification.style.display = 'none';
            }, 1000); 
        }
    });
});

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
                }, 1000); 
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
                }, 1000); 
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
            }, 1000); 
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
                    }, 1000); 
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
                    }, 1000); 
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

    document.addEventListener('DOMContentLoaded', function() {
        document.addEventListener('click', function(event) {
            if (event.target.closest('#button-container-pending, #button-container-rejected, .btn-secondary gradient')) {
                const adRequestId = event.target.dataset.adRequestId;
                const messages = event.target.dataset.messages;
                const requirements = event.target.dataset.requirements;
                const paymentAmount = event.target.dataset.paymentAmount;
                console.log("EDIT CLICKED");
    
                fetch(`/api/ad-request/details/${adRequestId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('adRequestId').value = adRequestId;
                    document.getElementById('campaignName').value = data.campaign_name;
                    document.getElementById('messages').value = messages;
                    document.getElementById('requirements').value = requirements;
                    document.getElementById('payment').value = paymentAmount;
    
                    fetch(`/api/influencers/${adRequestId}`)
                    .then(response => response.json())
                    .then(data => {
                        const influencerSelect = document.getElementById('influencer');
                        influencerSelect.innerHTML = ''; 
                        data.influencers.forEach(influencer => {
                            const option = document.createElement('option');
                            option.value = influencer.id;
                            option.textContent = influencer.username;
                            influencerSelect.appendChild(option);
                        });
    
                        influencerSelect.value = data.assigned_influencer || '';
    
                        $('#editAdRequestModal').modal('show');
                    })
                    .catch(error => console.error('Error fetching influencers:', error));
                })
                .catch(error => console.error('Error fetching ad request details:', error));
            }
        });
    });

    document.getElementById('saveChangesBtn').addEventListener('click', function() {
        var adRequestId = document.getElementById('adRequestId').value;
        var campaignName = document.getElementById('campaignName').value;
        var messages = document.getElementById('messages').value;
        var requirements = document.getElementById('requirements').value;
        var paymentAmount = document.getElementById('payment').value;
        var selectedInfluencer = document.getElementById('influencer').value;

        var apiUrl = '/api/ad_requests/update/' + adRequestId;

        var requestData = {
            campaignName: campaignName,
            messages: messages,
            requirements: requirements,
            paymentAmount: paymentAmount,
            influencerId: selectedInfluencer
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
            showNotification(data.message || 'Ad Request Updated Successfully', 'success');
            setTimeout(function() {
                $('#editAdRequestModal').modal('hide');
                location.reload(); 
            }, 1000); 
        })
        .catch(function(error) {
            console.error('Error Updating Ad Request', error);
            showNotification('Error Updating Ad Request', 'error');
        });

        function showNotification(message, type) {
            var notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = 'notification ' + (type || 'error');
            notification.style.display = 'block';
            setTimeout(function() {
                notification.style.display = 'none';
            }, 1000); 
        }
    });

    document.getElementById('delete-ad').addEventListener('click', function() {
        var adRequestId = document.getElementById('adRequestId').value;
        console.log(adRequestId);

        var apiUrl = '/api/ad_requests/delete/' + adRequestId;

        var requestData = {
            adRequestId: adRequestId
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
            showNotification(data.message || 'Ad Request Deleted Successfully', 'success');
            setTimeout(function() {
                $('#deleteAdModal').modal('hide');
                location.reload(); 
            }, 1000); 
        })
        .catch(function(error) {
            console.error('Error Deleting Ad Request', error);
            showNotification('Error Deleting Ad Request', 'error');
        });

        function showNotification(message, type) {
            var notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = 'notification ' + (type || 'error');
            notification.style.display = 'block';
            setTimeout(function() {
                notification.style.display = 'none';
            }, 1000); 
        }
    });

    


    