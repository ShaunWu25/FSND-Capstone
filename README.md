## Content
1. Motivation
2. Setup
3. RESTful API Documentation
4. Authentification
5. Deployment

## Motivations
This is the final project of the Udacity Full-Stack Web Developer Nonodegree. It covers following topics in the captone project.

1. Database modeling with postgres and sqlalchemy. File: model.py
2. API development and perform CRUD operations on database with flask. File: app.py
3. Unit testing. File: test_app.py
4. Authorization and Role Based Authentification Control with Auth0. File: auth.py
5. Depoloyment on Heroku

The app is used like a casting agency, where roles include casting assitant and executive producer. The app focuses on the management of the casting agency in actors and movies.

## Setup
### Installing Dependencies
Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

### Virtual Enviornment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the root directory and running:
```
pip install -r requirements.txt
```
This will install all of the required packages we selected within the requirements.txt file.

### Key Dependencies
[Flask](https://flask.palletsprojects.com/en/1.1.x/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

[SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in ./src/database/models.py. We recommend skimming this code first so you know how to interface with the Drink model.

[jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the server
From within the directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:
```
export FLASK_APP=api.py;
```
To run in the development mode, run:
```
export FLASK_END=development;
```
To run the server, execute:
```
flask run --reload
```
The --reload flag will detect file changes and restart the server automatically.

To login or set up an account, go to the following url:
```
https://fsnd-shaun.auth0.com/authorize?audience=Casting-Agency-Identifier&response_type=token&client_id=0MurronB3kgb8aSa5A31PQc1LGQmVhu9&redirect_uri=https://shaun-casting-agency.herokuapp.com/login-results
```

There will be two roles: 
1. Casting Assitant: able to perform GET both in actors and movies.
2. Executive Producer: able to perform all the permissions.

Two non-expired tokens for casting asistant and executive producer should be applied in the file of test_app.py to perform unit-testing.
You should access [Auth0](https://auth0.com/) and create relevant roles and users, subsequently assign it the the signed accounts to perform proper authtification.
The access token should be extracted from the redirected url and use it accorgingly when you sent the request in authorization header.

## RESTful API Documentation
RESTful principles are followed throughout the project, including appropriate naming of endpoints, use of HTTP methods GET, POST, PATCH, and DELETE.
Routes perform CRUD operations.

Utilize the @app.errorhandler decorator to format error responses as JSON objects for at least four different status codes

Project includes a custom @requires_auth decorator that:
* get the Authorization header from the request
* Decode and verify the JWT using the Auth0 secret
* take an argument to describe the action
* raise an error if:
  1. the token is expired
  2. the claims are invalid
  3. the token is invalid
  4. the JWT doesn’t contain the proper action

The base url for the API: https://shaun-casting-agency.herokuapp.com/

Available Endpoints
|Endpoints|  GET |  POST |  DELETE | PATCH  |
|------|-------|---------|--------|--------|
|/actors|  [o] |  [o]  |   [o]   |   [o]  |   
|/movies|  [o] |  [o]  |   [x]   |   [x]  |  

Role Based Permission
|Roles|  GET |  POST |  DELETE | PATCH  |
|------|-------|---------|--------|--------|
|casting assistant|  [o] |  [x]  |   [x]   |   [x]  |   
|executive producer|  [o] |  [o]  |   [o]   |   [o]  |  

    
------------------------------------------------------------------------------------------------


1. GET /actors
Query paginated actors.
```
$ curl -X GET https://shaun-casting-agency.herokuapp.com/actors?page1
```
Example response
```
{
  "actors": [
    {
      "age": 30,
      "gender": "Male",
      "id": 1,
      "name": "Shaun"
    }
  ],
  "success": true,
  "total_actors": 1
}
```
2. POST /actors
Create new actor into database.
```
$ curl -X POST -H "Content-Type: application/json" -d '{"name":"Shaun", "gender":"Male", "age":"30"}' https://shaun-casting-agency.herokuapp.com/actors
```
Example response
```
{ 
    "actors": [
      {
        "age": 30,
        "gender": "Male",
        "id": 1,
        "name": "Shaun"
      }
    ],
    "created": 1,
    "success": true,
    "total_actors": 1
}
```
3. PATCH /actors
Edit an existing Actor
```
$ curl https://shaun-casting-agency.herokuapp.com/actors/1 -X PATCH -H "Content-Type: application/json" -d '{"age":"36"}'
```
Example response
```
{
  "success": true,
  "id": 1
}
```
4. DELETE /actors
Delete an existing Actor
```
$ curl -X DELETE https://shaun-casting-agency.herokuapp.com/actors/1
```
Example response
```
{
  "actors": [
      {
        "age": 30,
        "gender": "Male",
        "id": 2,
        "name": "Shaun"
      }
    ],
  'success' : True,
  'deleted': 1,
  'total_movies': 1
}
```
5. GET /movies
Query paginated movies.
```
$ curl -X GET https://shaun-casting-agency.herokuapp.com/movies?page1
```
Example response
```
{
  "movies": [
    {
      "id":11,
      "release_date":"Sun, 12 Jul 2020 00:00:00 GMT",
      "title":"Swim"
    }
  ],
  "success":true
}
```
6. POST /movies
Insert new movie into database.
```
$ curl -X POST -H "Content-Type: application/json" -d '{"title":"Bat Man", "release_date":"2016-02-15"}' https://shaun-casting-agency.herokuapp.com/movies
```
Example response
```
{
  "movies": [
    {
      "id":11,
      "release_date":"Sun, 15 Feb 2016 00:00:00 GMT",
      "title":"Bat Man"
    }
  ],
  "success":true,
  'created': 11,
  'total_movies': 10
}
```
## Authentification
In your API Calls, add them as Header, with Authorization as key and the Bearer token as value. Don´t forget to also prepend Bearer to the token (seperated by space).

* Roles and permission tables are configured in Auth0.
* Access of roles is limited. Includes at least two different roles with different permissions.
* The JWT includes the RBAC permission claims.

For example: (Bearer token for Executive Producer)
```
{
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVuR2NFaHJia3I5akY2cmF0S25nQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEzODI1MDA0MDUxMjU0ODIzMjA2IiwiYXVkIjpbIkNhc3RpbmctQWdlbmN5LUlkZW50aWZpZXIiLCJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDU2Mzg1MiwiZXhwIjoxNTk0NTcxMDUyLCJhenAiOiIwTXVycm9uQjNrZ2I4YVNhNUEzMVBRYzFMR1FtVmh1OSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.IyXHNlvrM3UPbV9L0FlUuPZL6L2DRUpskHZjTdEXFWpnXjogtMmrNqGsbrdYXWtStCqS6yGcrdfleJf-KJjKr56GlK5BiRkkQY5At5eYQrk5tSqixPVFS_oILxSQed6kvNVllk-eF6JIIoctx7nJfZrEk5eGxSdZwE33fxpf6fO84x9SNer9l_lY7rG1kWQdzWNl6aCc9D26McXWXzk9VPbJYxa6EaKNufsJYgohk-iHHRtVVuhLslEGNK2K7SsNzHXUtUlXM8Vg-E12sYTGabhx6NXpU0S2OUYrReCP56cWmh_droLvgz10bl4nHLBIqGtud7BofTWwy-ya46a3NA"
}
```
Go to JWT.io for debugging to see if the token has relevent permission to perfrom relevent requests : https://jwt.io/#debugger-io

An Example to add an actor to heroku database with bearer attached as authentification:
```
$ curl -X POST -H "Content-Type: application/json" -d '{"name":"Shaun", "gender":"Male", "age":"30"}' "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVuR2NFaHJia3I5akY2cmF0S25nQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEzODI1MDA0MDUxMjU0ODIzMjA2IiwiYXVkIjpbIkNhc3RpbmctQWdlbmN5LUlkZW50aWZpZXIiLCJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDI4Njk2MiwiZXhwIjoxNTk0Mjk0MTYyLCJhenAiOiIwTXVycm9uQjNrZ2I4YVNhNUEzMVBRYzFMR1FtVmh1OSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyJdfQ.IXiYjwnGSxpYDjlQlgCfaVX677oA-tSM14GtDwcqs7YEU-SQBqy2qXDg60KFNGcqBgxglWy8zrVCGE6epsfMdFe-PfqDChaGnKt5DQ8wwaOBeYHHQVPR581vviBEtVewyzIZpx7XQefU6iuV_mgLWOiwSlRawB5wlnbp_H0a9S_xZitVD7g-mgEADx_9mr3GIaxH32PeFG7a0tQgxX0LuZsKQ3JKk-TFsDaV2W0HhakGyvwQhClQtJc-zcFEqkuLpa2P9_1swGTe5Mc2d0fkl_w9t9495IaZs-B2jOfyD72MU-gjEGkMmB3z_HwA4A2bCwtpB1I2RGIPxzDNjaNq6w" https://shaun-casting-agency.herokuapp.com/actors 
```
An Example to patch an actor in id 2 to heroku database with bearer attached as authentification:
```
$ curl https://shaun-casting-agency.herokuapp.com/actors/2 -X PATCH -H "Content-Type: application/json" -d '{"age":"36"}' "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVuR2NFaHJia3I5akY2cmF0S25nQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEzODI1MDA0MDUxMjU0ODIzMjA2IiwiYXVkIjpbIkNhc3RpbmctQWdlbmN5LUlkZW50aWZpZXIiLCJodHRwczovL2ZzbmQtc2hhdW4uYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDI4Njk2MiwiZXhwIjoxNTk0Mjk0MTYyLCJhenAiOiIwTXVycm9uQjNrZ2I4YVNhNUEzMVBRYzFMR1FtVmh1OSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyJdfQ.IXiYjwnGSxpYDjlQlgCfaVX677oA-tSM14GtDwcqs7YEU-SQBqy2qXDg60KFNGcqBgxglWy8zrVCGE6epsfMdFe-PfqDChaGnKt5DQ8wwaOBeYHHQVPR581vviBEtVewyzIZpx7XQefU6iuV_mgLWOiwSlRawB5wlnbp_H0a9S_xZitVD7g-mgEADx_9mr3GIaxH32PeFG7a0tQgxX0LuZsKQ3JKk-TFsDaV2W0HhakGyvwQhClQtJc-zcFEqkuLpa2P9_1swGTe5Mc2d0fkl_w9t9495IaZs-B2jOfyD72MU-gjEGkMmB3z_HwA4A2bCwtpB1I2RGIPxzDNjaNq6w"
```

### Deployment 
API is hosted live via [Heroku](https://www.heroku.com). API can be accessed by URL and requires authentication.




