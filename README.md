# Casting Agency
**This project is currently hosted on [https://casting-agency-app.herokuapp.com/](https://casting-agency-app.herokuapp.com/)**

## Introduction
This project is here to help casting agencies more easily handle and assign movies and their actors. Easily add, remove, and edit your movie listings and actors with this API. 

## Getting started
### Installing Dependencies
#### Python 3.8
To make sure you have the latest version of python running on your machine, follow the steps here in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Environment
When working on python projects, it is recommended that you run things on a virtual environment. This way, you will be able to run modules on different versions as needed. These instructions will get you set up on a mac. To see a more thorough walk-through or if you're running on another OS, take a look at the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

 1. Install/upgrade pip `python3 -m pip install --user --upgrade pip`
 2. Install virtualenv `python3 -m pip install --user virtualenv`
 3. Create a virtual environment `python3 -m venv env`
 4. Activate it `source env/bin/activate`
 5. To deactivate: `deactivate`

#### PIP Dependencies
With the virtual environment run: 
```bash
pip install -r requirements.txt
```
This will install all the dependencies listed in `requirements.txt`.

### Running the server locally
To run the server locally, run:
```bash
source setup.sh
python app.py
```

**This project is currently hosted on [https://casting-agency-app.herokuapp.com/](https://casting-agency-app.herokuapp.com/)**

## API Reference

 - Base URL: The live backend can be accessed [here](https://casting-agency-app.herokuapp.com/).
 - Authentication: Endpoints require different levels of authentication, depending on user roles.
	 - Casting Assistant
		 - Can view actors and movies
	 - Executive Producer
		 - Can view actors and movies
		 - Can modify actors and movie information
		 - Can add or remove actors
		 - Can add or remove movies

### Getting Authenticated
To log, please visit this [Auth0 login interface](https://casting-agency-tenant.auth0.com/authorize?audience=CastingAgencyIdentifier&response_type=token&client_id=FQROMWmj8u7f3jGlb0xAgA0Xicjtb7ub&redirect_uri=http://127.0.0.1:8080/). You will be redirected back with your authorization token in the browser bar. This token will be used to access the endpoints.

Three test users with different permission levels have been created in order to test the endpoints (tokens will expire every 2 hours):

 - Casting Assistant
	 - Email: casting.assistant@example.com
	 - Password: Password1

- Executive Director
	- Email: exective.director@example.com
	- Password: Password2

### Error Handling
Errors are returned as JSON objects that look something like this:
```
{
	"error": 404,
	"message": "resource not found",
	"success": false
}
```
The API will return objects like this when requests fail because of errors of type:
- 400: Bad Request (usually bad syntax)
- 401: Unauthorizied Request
- 403: Forbidden 
- 404: Resource not found
- 500: Internal server error
- AuthError: AuthError.error


### Endpoints
#### Movies
##### GET /movies TODO
- General:
	- Required permission: get movies
	- Fetches available movies as an array of objects that contain a movie id, title, and release date
	- Request arguments: None
    -Response: Success state which true and list of movies
- Sample: 
	```
	curl -XGET -H 'Authorization: Bearer {token}' -H "Content-type: application/json" 'https://casting-agency-app.herokuapp.com/movies'
	```
- Response: 
	```
	{"movies":[],"success":true}
	```

##### POST /movies
- General:
	- Required permission: Post movies
	- Posts a new movie to the database. Required fields are `title` and `release_date`
	- Request arguments: None
	- Response: Success state which true
- Sample: 
	```
	curl -XPOST -H 'Authorization: Bearer {token}' -H "Content-type: application/json" -d '{"title":"kingdom", "release_date":"1-9-2019"}' 'https://casting-agency-app.herokuapp.com/movies'
	```
- Response: 
	```
	{"success":true}
	```
	
##### PATCH /movies/<movie_id>
- General:
	- Required permission: patch movies
	- Edits a movie. Available fields are `title` and `release_date`
	- Request arguments: `movie_id`
	- Response: Success state which true
- Sample: 
	```
	curl -XPATCH -H 'Authorization: Bearer {token}' -H "Content-type: application/json" -d '{"title":"dexter", "release_date":"1-9-2019"}' 'https://casting-agency-app.herokuapp.com/movies/2'
	```
- Response: 
	```
	{"success":true}
	```

##### DELETE /movies/<movie_id>
- General:
	- Required permission: delete movies
	- Deletes a movie from the database.
	- Request arguments: `movie_id`
	- Response: Success state which true
- Sample: 
	```
	curl -XDELETE -H 'Authorization: Bearer {token}' -H "Content-type: application/json" 'https://casting-agency-app.herokuapp.com/movies/2'
	```
- Response: 
	```
	{"success":true}
	```

#### Actors
##### GET /actors
- General:
	- Required permission: get actors
	- Fetches available actors as an array of objects that contain a actor id, name, age, and gender
	- Request arguments: None
	- Response: Success state which true and list of actors
- Sample: 
	```
	curl -XGET -H 'Authorization: Bearer {token}' -H "Content-type: application/json" 'https://casting-agency-app.herokuapp.com/actors'
	```
- Response: 
	```
	{"actors":[],"success":true}
	```

##### POST /actors
- General:
	- Required permission: Post actors
	- Posts a new actor to the database. Required fields are `name`, `age`, and `gender`
	- Request arguments: None
	- Response: Success state which true
- Sample: 
	```
	curl -XPOST -H 'Authorization: Bearer {token}' -H "Content-type: application/json" -d '{"name":"Menna shalaby", "age":30, "gender": "female"}' 'https://casting-agency-app.herokuapp.com/actors'
	```
- Response: 
	```
	{"success":true}
	```
		
##### PATCH /actors/<actor_id>
- General:
	- Required permission: patch actors 
	- Edits an actor. Available fields are `name`, `age`, and `gender`
	- Request arguments: `actor_id`
	- Response: Success state which true
- Sample: 
	```
	curl -XPATCH -H 'Authorization: Bearer {token}' -H "Content-type: application/json" -d '{"name":"zenna", "age":45, "gender": "female"}' 'https://casting-agency-app.herokuapp.com/actors/2'
	```
- Response: 
	```
	{"success":true}
	```

##### DELETE /actors/<actor_id>
- General:
	- Required permission: delete actors
	- Deletes an actor from the database.
	- Request arguments: `actor_id`
	- Response: Success state which true
- Sample: 
	```
	curl -XDELETE -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUVXlOelF6TmpCQ01qSTRORGd4UXpsRE9UTkRRMFkzT0RnNFFqRTJNa1kxUWtaQ01VWkRNZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXRlbmFudC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3ZjI3ZDQ5MThlYzMwY2IxNDY0ODRlIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUlkZW50aWZpZXIiLCJpYXQiOjE1ODU0MzM0MDYsImV4cCI6MTU4NTUxOTgwNiwiYXpwIjoiRlFST01XbWo4dTdmM2pHbGIweEFnQTBYaWNqdGI3dWIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.NAl6wYew3j1iAr2Aekboi0cZZYqQxSs0XIp-XwJY__WFofjTaiNN8i0vdzKr-yYdHHWqYoE-HNI1pW0J3lqHPR2IKyY6Kqke4x0So_ItdVA2MAofv8Z8LtrtmpHUlXU9UfvouwQKH-SRAiDT3fgL0cVnxUZD_UjOZMqXxrRp9FmBe8zzlcoNaeB2TSqIyEHsaGmuZIFnmyccVI2Y-gmVd6_z5QVg2a-YXyTrKwgaFmeLv5Au6_ZN_or80XPIhC3B2Zn_M6suC2VYRpfxgBJkwxFjHeOoT1OQHRoIvz8il4Ty1CzGh6NsNbfuETHQ1-n23k8AAC_B31t-mswFVxvbFA' -H "Content-type: application/json" 'https://casting-agency-app.herokuapp.com/actors/2'
	```
- Response: 
	```
	{"success":true}
	```

### Testing
To run the tests, run
```
source setup.sh
python test_app.py
```
