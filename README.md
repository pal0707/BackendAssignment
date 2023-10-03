# Post System

The Post System is a REST API-based application that allows users to create and manage post.

## Requirements

- Ubuntu (Preferred)
- Python 3.9 and above
- Postgres (Preferred)
- Django 4.x
- Django Rest Framework (DRF)
- Postman (for testing the APIs)

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/pal0707/BackendAssignment.git
   cd BackendAssignment

2. Create and activate a virtual environment:
```
python -m venv env
source env/bin/activate
```

3. Create and activate a virtual environment::
```shell
       python -m venv env
       source env/bin/activate
```
4. Install the required packages:

```shell
      pip install -r requirements.txt
```
5. Configure the database settings:

Open the settings.py file in the incidentmanagement directory.
Update the DATABASES configuration with your Postgres database settings.

set .env variable
# Local Setting
ENV=LOCAL
DEBUG=True
# Database Settings
DATABASE_NAME=DataBase Name
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432

6. Apply database migrations:

```shell
      python manage.py migrate
```
7. Start the development server:

```shell
    python manage.py runserver
```
8. The API endpoints will be available at http://localhost:8000/api/.

## Usage
Register a new user by making a POST request to http://localhost:8000/api/register/. Provide the username and password and other in the request body.

Log in with a user by making a POST request to http://localhost:8000/api/login/. Provide the username and password in the request body. The response will include an authentication token.

Use the provided authentication token in the Authorization header for subsequent requests. Example: Authorization: Token <token>.

Create Post by making a POST request to http://localhost:8000/api/posts/. Provide the i

View Post created by the logged-in user by making a GET request to http://localhost:8000/api/posts/.

View Particular Post created by the logged-in user by making a GET request to http://localhost:8000/api/posts/post_id//.

