const API_BASE_URL = 'http://localhost:8000/api/v1';

// Check if user is already logged in
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    const currentPage = window.location.pathname.split('/').pop();

    if (token && currentPage !== 'dashboard.html') {
        window.location.href = 'dashboard.html';
    } else if (!token && currentPage === 'dashboard.html') {
        window.location.href = 'login.html';
    }

    // Initialize event listeners based on current page
    if (currentPage === 'login.html') {
        initializeLoginForm();
    } else if (currentPage === 'register.html') {
        initializeRegisterForm();
    } else if (currentPage === 'dashboard.html') {
        initializeDashboard();
    }
});

// Login form handler
function initializeLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                console.log('Attempting login with:', { email });
                const response = await fetch(`${API_BASE_URL}/auth/login/email`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                console.log('Login response status:', response.status);
                const data = await response.json();
                console.log('Login response data:', data);

                if (response.ok) {
                    console.log('Login successful, storing token:', data.access_token);
                    // Store the raw token without Bearer prefix
                    localStorage.setItem('token', data.access_token);
                    console.log('Token stored, redirecting to dashboard');
                    window.location.href = 'dashboard.html';
                } else {
                    console.error('Login failed:', data.detail);
                    alert(data.detail || 'Login failed');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login');
            }
        });
    }
}

// Register form handler
function initializeRegisterForm() {
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const userData = {
                name: formData.get('name'),
                email: formData.get('email'),
                password: formData.get('password'),
                phone_number: formData.get('phone_number'),
                license_plate_number: formData.get('license_plate_number'),
                address: {
                    street: formData.get('address'),
                    city: '',
                    state: '',
                    country: '',
                    postal_code: ''
                }
            };

            try {
                console.log('Attempting registration with:', userData);
                const response = await fetch(`${API_BASE_URL}/auth/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userData),
                });

                const data = await response.json();
                console.log('Registration response:', data);

                if (response.ok) {
                    alert('Registration successful! Please login.');
                    window.location.href = 'login.html';
                } else {
                    const errorMessage = data.detail || 'Registration failed';
                    console.error('Registration failed:', errorMessage);
                    alert(errorMessage);
                }
            } catch (error) {
                console.error('Registration error:', error);
                alert('An error occurred during registration');
            }
        });
    }
}

// Dashboard initialization
function initializeDashboard() {
    console.log('Initializing dashboard...');
    const token = localStorage.getItem('token');
    console.log('Current token in localStorage:', token);

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            console.log('Logout clicked');
            localStorage.removeItem('token');
            window.location.href = 'login.html';
        });
    }

    // Fetch and display user information
    fetchUserInfo();
}

// Fetch user information
async function fetchUserInfo() {
    const token = localStorage.getItem('token');
    console.log('Fetching user info, current token:', token);
    
    if (!token) {
        console.error('No token found in localStorage');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 5000);
        return;
    }

    try {
        console.log('Making request to:', `${API_BASE_URL}/users/me`);
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        });

        console.log('Response status:', response.status);
        const responseText = await response.text();
        console.log('Response text:', responseText);

        if (response.ok) {
            const userData = JSON.parse(responseText);
            console.log('User data received:', userData);
            displayUserDetails(userData);
        } else if (response.status === 401) {
            console.error('Token invalid or expired');
            localStorage.removeItem('token');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 5000);
        } else {
            console.error('Error response:', responseText);
            throw new Error(`Failed to fetch user data: ${response.status} ${responseText}`);
        }
    } catch (error) {
        console.error('Error fetching user info:', error);
        alert('Failed to load user information. Please login again.');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 5000);
    }
}

// Display user information
function displayUserDetails(user) {
    const userDetails = document.getElementById('userDetails');
    const userName = document.getElementById('userName');
    
    userName.textContent = user.name || 'User';
    
    if (user.profile_pic_url) {
        document.getElementById('profilePic').src = user.profile_pic_url;
    }

    // Format the date
    const createdDate = new Date(user.created_at);
    const formattedDate = createdDate.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    userDetails.innerHTML = `
        <p><i class="fas fa-envelope"></i> <strong>Email:</strong> ${user.email}</p>
        <p><i class="fas fa-phone"></i> <strong>Phone:</strong> ${user.phone_number || 'Not provided'}</p>
        <p><i class="fas fa-car"></i> <strong>License Plate:</strong> ${user.license_plate_number || 'Not provided'}</p>
        <p><i class="fas fa-map-marker-alt"></i> <strong>Address:</strong> ${user.address ? `${user.address.street}, ${user.address.city}` : 'Not provided'}</p>
        <p><i class="fas fa-calendar"></i> <strong>Member since:</strong> ${formattedDate}</p>
        <p><i class="fas fa-check-circle"></i> <strong>Email Verified:</strong> ${user.email_verified ? 'Yes' : 'No'}</p>
        <p><i class="fas fa-check-circle"></i> <strong>Phone Verified:</strong> ${user.phone_verified ? 'Yes' : 'No'}</p>
        <p><i class="fas fa-user"></i> <strong>Account Status:</strong> ${user.is_active ? 'Active' : 'Inactive'}</p>
    `;
}

// Add this function to handle profile picture changes
async function handleProfilePictureChange(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('profile_picture', file);

    try {
        const response = await fetch('/api/me/profile-picture', {
            method: 'PUT',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('profilePic').src = data.profile_picture_url;
        } else {
            console.error('Failed to update profile picture');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Add event listeners for profile picture
document.addEventListener('DOMContentLoaded', function() {
    const changePicBtn = document.getElementById('changePicBtn');
    if (changePicBtn) {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);

        changePicBtn.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', handleProfilePictureChange);
    }
}); 