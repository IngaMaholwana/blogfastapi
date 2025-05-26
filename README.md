# Blog API

This is a FastAPI project for a blog API that includes user registration and authentication, CRUD operations for blog posts, comments on blog posts, and basic search functionality.

## Features

- User registration and authentication
- CRUD operations for blog posts
- Adding comments to blog posts
- Basic search functionality for posts

## Project Structure

```
blog-api
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── dependencies.py
│   └── routers
│       ├── __init__.py
│       ├── users.py
│       ├── posts.py
│       └── comments.py
├── tests
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_posts.py
│   └── test_comments.py
├── .env
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd blog-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your environment variables, such as database connection strings and secret keys.

5. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

### User Registration

- **POST** `/users/register`
  - Request body: `{"username": "string", "email": "string", "password": "string"}`
  - Response: User object

### User Login

- **POST** `/users/token`
  - Request body: `{"username": "string", "password": "string"}`
  - Response: JWT token

### Blog Posts

- **CRUD operations** for blog posts will be available under `/posts` endpoint.

### Comments

- **CRUD operations** for comments will be available under `/comments` endpoint.

## Testing

Run the tests using:
```
pytest
```