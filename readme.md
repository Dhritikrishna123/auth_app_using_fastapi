# FastAPI Authentication App with MongoDB and OTP

A complete authentication system with FastAPI backend and HTML/CSS/JS frontend. Features include JWT authentication, OTP verification, and location tracking.

## Features

- User registration with profile picture and location tracking
- JWT token-based authentication
- Email OTP verification
- Location tracking and address updating
- MongoDB integration for data storage
- Responsive frontend design

## Project Structure

```
auth_app/
├── backend/        # FastAPI backend
├── frontend/       # HTML/CSS/JS frontend
└── README.md       # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB
- SMTP server access for email OTP

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd auth_app/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory with the following variables:
   ```
   SECRET_KEY=your_secret_key_here
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=auth_app_db
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

6. Start the backend server:
   ```
   python -m app.main
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd auth_app/frontend
   ```

2. You can serve the frontend files using any static file server. For development, you can use Python's built-in HTTP server:
   ```
   python -m http.server 5000
   ```

3. Open your browser and navigate to `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login/email` - Login with email and password
- `POST /api/v1/auth/request-otp` - Request OTP verification email
- `POST /api/v1/auth/verify-otp` - Verify OTP code

### User Management

- `GET /api/v1/users/me` - Get current user information
- `PUT /api/v1/users/me/address` - Update user address
- `POST /api/v1/users/me/profile-picture` - Update profile picture

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens expire after 7 days
- OTPs expire after 10 minutes
- CORS is enabled for frontend access
- Environment variables are used for sensitive information

## Future Improvements

- Phone number OTP verification via SMS
- Social media authentication
- User roles and permissions
- Password reset functionality
- Two-factor authentication
- Email change verification
- Better map integration
- Unit tests

## License

MIT