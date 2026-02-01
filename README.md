# UserRegAPI

<div align="center">

<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.10+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
</a>
<a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
</a>
<a href="https://www.mysql.com/">
    <img src="https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white" alt="mysql logo"  />
</a>
<a href="https://pyjwt.readthedocs.io/en/stable/">
    <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens" alt="JWT">
</a>
<a href="https://curl.se/">
    <img src="https://img.shields.io/badge/curl-7A81AD?style=for-the-badge&logo=curl&logoColor=white" alt="curl">
</a>
<a href="https://www.postman.com/">
    <img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman">
</a>

</div>

A simple side project focused on utilizing Python FastAPI resources and navigating the world of user registration systems. This project explores what happens behind the scenes when interacting with styled web pages, providing a practical implementation of user registration, authentication, and email verification.

Feel free to use it, play around with it, and update whatever doesn't suit your needs.

## Features

- User registration with email verification
- JWT-based authentication (access tokens and refresh tokens)
- User profile management
- Secure password handling
- Email confirmation system
- Token-based session management
- Account deletion functionality

## Requirements

- Python 3.10+
- MySQL database
- FastAPI (with standard dependencies)
- curl 
- postman

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/debil746429/UserRegAPI.git
cd UserRegAPI
```

### 2. Create a virtual environment

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Database Setup

1. **Create a MySQL database** (make sure you don't have a database named `chat` if you're using the default configuration)

2. **Update the `.env` file** with your configuration:

```env
# Database Configuration
db_host = localhost
db_name = chat
db_user = your_database_user
db_password = your_database_password

# JWT Configuration
JWT_SECRET = your_secret_key_here
JWT_ALGORITHM = HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 100  # in minutes
REFRESH_TOKEN_EXPIRY_DAYS = 3000  # in days

# Email Configuration (for email verification)
sender_email = your_email@gmail.com
email_password = your_app_password
```

3. **Import the database schema:**

```bash
mysql -u your_db_user -p your_database_name < schema.sql
```

Or manually execute the SQL commands from `schema.sql` in your MySQL client.

## Running the Application

Start the development server:

```bash
fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, you can view the interactive API documentation at:

- **ReDoc**: http://127.0.0.1:8000/redoc
- **Swagger UI**: http://127.0.0.1:8000/docs

## API Endpoints

### Public Endpoints

- `GET /api/v1/` - Test endpoint
- `POST /api/v1/register` - Register a new user
- `GET /api/v1/auth/verify_email/{token}` - Verify email and complete registration
- `POST /api/v1/login` - User login

### Protected Endpoints (Require Authentication)

- `PATCH /api/v1/update-profile` - Update user profile
- `DELETE /api/v1/delete-account` - Delete user account
- `POST /api/v1/logout` - Logout user

## Testing

You can test the endpoints using:

- **cURL** - Command-line tool for making HTTP requests
- **Postman** - API testing and development platform
- **Swagger UI** - Interactive documentation at `/docs` endpoint


## Project Structure

```
UserRegAPI/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   └── user.py      # User-related endpoints
│   │   └── main.py          # API router configuration
│   ├── core/
│   │   ├── config.py        # Application configuration
│   │   ├── db.py            # Database connection
│   │   ├── emailConf.py     # Email configuration
│   │   └── security.py      # Security utilities (JWT, etc.)
│   ├── model/
│   │   └── models.py        # Pydantic models
│   ├── services/
│   │   └── user.py          # User business logic
│   └── main.py              # FastAPI application entry point
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── schema.sql              # Database schema
├── LICENSE.md              # License information
└── README.md               # This file
```

## License

See [LICENSE.md](LICENSE.md) for details.

## Contributing

Feel free to fork this project, make changes, and submit pull requests. This is a learning project, so contributions and improvements are welcome!
