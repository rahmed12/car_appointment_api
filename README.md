# Car appointment api
> REST API that can store and manage appointments fora car service center.
<hr>



# Table of Contents
* [Prerequisite: Make sure you have the following](#Prerequisite)
* [Technologies](#Technologies)
* [Design](#Design)
* [Setup](#Setup)
* [Test](#Test)
* [Extra](#Extra)




# <a name="Prerequisite"></a>Prerequisite
* Linux
* Docker
* Postman






# <a name="Technologies"></a>Technologies
* Docker
	* To allow easy installation and scaling if needed
* Flask
	* To allow quick development of this simple web applications
* MongoDb
	* Good for scaling and for model with very little relationships
* Postman
	* Easy to test Rest api
* Python3
	* For the fun of it
* Json
	* Standard reply back to the client

# <a name="Design"></a>Design
* Simple, and I mean simple flow chart

![Untitled Diagram](https://user-images.githubusercontent.com/47451663/101845077-c5958b80-3b1b-11eb-8c8f-4ed85de8baa9.png)

* __1. Why do we need a car service appointment API?__
	* We want external developers to have access to our appointment app to be able to build their own application

* __2. Requirements__
	* The application should have REST endpoints that do the following:
 		* Create users credential for token
  		* Create token
  		* Delete appointments from the database
  		* Create new appointments
 		*  Update the status of an existing appointment
  		* Retrieve a specific appointment from the database.
  		* Retrieve all appointments that are scheduled between a date range and sorted by price.
  		* Randomly generate appointments and store inside db


 	* The system highly available
 	* The system should update in mealtime
 


* __3. Capacity Estimation and Constraints__
	* Since this car service only has one location there is a finite amount of appointments it can take in one day.  We are going to assume 12 appointments can be made in a given day.

	* We are going to assume one record takes up 400KB

	* The read/write will be at a ratio of 1:1 (1 record creating: 1 record read)

	* New appointment:   1 every 2 hours
	* Retrieve appointment: 1 every 2 hours
	* Incoming data: 12 * 400 = 4800KB per day
	* Outgoing data: 12 * 400 = 4800KB per day
	* Storage for 10  years: 17G


* <a name="systemApiSec"></a> __4. System APIs__ 
	* Generating user's credentials:
	
 POST body
{
    "appauth_id": "",
    "appauth_secret": ""
} 

url: http://`<your host`>/appsauth/


	* Generating Token:
 POST body
{
    "appauth_id": "",
    "appauth_secret": ""
} 

url: http://`<your host`>/appsauth/tokens/

	* Create record:
 POST body
{
    "first_name": "",
    "last_name": "",
    "service": " ",
    "status": "",
    "street_address": "  ",
    "city": "",
    "state": "”
     "zip": "",
    "phone": “”
    "date": "",
    "price": ""
} 

header:
x-access-id  `<user credential id`>
x-access-token  `<user token`> 

POST header:
x-access-id  <user credential id>
x-access-token  <user token> 


	* Get all records:
GET
header:
x-access-id  `<user credential id`>
x-access-token  `<user token`> 


	* Get one record:
 header:
x-access-id  `<user credential id`>
x-access-token  `<user token`>

url: http://`<your host`>/appts/`<record id`> 


	* Get data range records
header:
x-access-id  `<user credential id`>
x-access-token  `<user token`>

url: http://`<your host`>/appts/?startdate=`<yyyy-mm-dd`>&enddate=`<yyyy-mm-dd`>

	* Update one record:
PUT
body:
{

    "status": "close"
}

header:
x-access-id  `<user credential id`>
x-access-token  `<user token`>

	* Delete one record:
DELETE
header:
x-access-id  `<user credential id`>
x-access-token  `<user token`>

url: http://`<your host`>/appts/`<record id`>




* __5. Database Design__
	* Not a lot of data to store
	* Each object is about 400K
There are no relationship
		* We are assuming that the user and service tables are external to us.  Meaning we don't have knowledge of their user id and service table id and just need to store user appointments
	* NoSQL is what we are going to use also if we ever need to scale it will be easier to do with with NoSQL


* __6. System Design__ 
* For incoming appointment, we are going to generate our own record id using uuid4.  We are doing this because we don't want users to be able to guess our internal ids to prevent hacking

* The user will need to create their own credentials and token with the APIs we have given them.  The user's secrete id will be encrypted on our system using bcrypt.
		* The good about this is if the database is compromised their password is safe

* We create the token using uuid and if there are any old tokens for this user we will delete them.  Every 30 days, the user token will expire.  If user token has been expired they will have to generate a new token

* For all the endpoints we are using the json format.  We only return json back to the client

* For testing we are using Postman (and unittest).  It's better to test with postman as it is easy to test outbound/inbound 



# <a name="Setup"></a>Setup
* If you want to watch a video version of this, here is the link [![Car Serive appointment API](https://img.youtube.com/vi/VID/0.jpg)](https://youtu.be/UVpPy3DLpBs)
* Take note, the random_schedule.py script randomly (between 1-30 secs) generates appointments inside the database with a future date
	* To verify, log into the mongodb (steps in the Extra section) and you will see records appearing within 30 sec.
* From the repository https://github.com/rahmed12/car_appointment_api.git get these files and put it on your linux machine (you don't need the whole repository since we are using docker):
	* __appts_api.postman_collection.json__
		* This is for Postman
	* __docker-compose.yaml__
		* This is for docker

* Start Postman and import the file __appts_api.postman_collection.json__
	* you should have a new collection called appts api
	
	![1_postman](https://user-images.githubusercontent.com/47451663/101697730-569a3300-3a46-11eb-9750-67a7b6a37e5e.PNG)
	* If you expand the collection you should have two entries called auth and appts
	
	![2_postman](https://user-images.githubusercontent.com/47451663/101698259-328b2180-3a47-11eb-9d04-a761eb8d4c78.PNG)
	* If you expand those folders you will see the endpoints
	
	![3_postman](https://user-images.githubusercontent.com/47451663/101698215-21daab80-3a47-11eb-8c74-5f1f2f3a68f0.PNG)


	* Note:
		* In postman we are using __localhost__ with the endpoints
		
		![4_postman](https://user-images.githubusercontent.com/47451663/101699203-c14c6e00-3a48-11eb-9933-f1d29e8194de.PNG)
		
		* In my system the ip __0.0.0.0__ is set for localhost.  Make sure your localhost is set to 0.0.0.0
		* We are using default port __80__



* Run this docker-compose command on your linux machine :
	* Make sure the docker-compose.yaml file is in the same directory you run this command in:
	* __docker-compose run --service-ports  web_run__

	* The reason for the service-ports flag is to let postman send info to the container
	* Once this command is done you should have two images:
		* mongo 3.6.3
		* rasaldocker/carapptapi_web latest
		
		![1_docker_images](https://user-images.githubusercontent.com/47451663/101699621-72eb9f00-3a49-11eb-80ad-e8bd9f867d05.PNG)
		
		![2_docker_images](https://user-images.githubusercontent.com/47451663/101699628-7848e980-3a49-11eb-90bb-29054de622cb.PNG)

	* You should also have two containers running:
		* `<directory name>_web_run_run_<num> `
		* carapi_db_1
	
		![1_container](https://user-images.githubusercontent.com/47451663/101699810-e5f51580-3a49-11eb-9a1c-b7f004d8eaed.PNG)
		
		
		

# <a name="Test"></a>Test
* There are two ways of testing
	* Using Postman:
		* Run the collection name appts api
		* It will output the test success or failures
		* if you run it again it will failure in some place
		* If you want to rerun again just drop the database (instructions below in extra)
	* Using unnitest 
 		* docker exec -it `<container name>_web_run_run_<number>` python tests.py
 		* this will report any failures or success from any tests.py files
 		* app_auth/tests.py
		* appt/tests.py
	* Manual testing
		* If you hate yourself you can do manual testing by using the endpoints.  They are listed in the [System API section](#systemApiSec)
		* You can also look at the postman endpoint's header and body to see the setup
			* For creating creds you will need this in the body:
			 
			{
    			"appauth_id": "make up an id",
    			"appauth_secret": "make up a secret"
			}
			
			
			* To create token you will need this in the body:
			
			{
    			"appauth_id": "your id",
    			"appauth_secret": "your secret"
			}
			
			    
			* Write down the token that is sent back to you
			    

		* For the rest of the endpoints you will need this in your header:
		
		x-access-id `<your id`>
		x-access-token `<the token you wrote down`>
		
		
		



# <a name="Extra"></a>Extra
* If you need to access the mongodb you can do this (while your containers are running):
	* docker ps
	* get the container name for carapptapi_web:latest

	* `docker exec  -it <container name> mongo -host mongodb`

	* You should be on the mongodb.  To show database:
		* `show dbs`

	* To select our database:
		* `use appts-api`

	* To see the collections:
 		* `show collections`

	* To see what's in the collection (for example we want to see what's inside of our token collection):
		* `db.tokens.find()`

	* To drop the  appts-api database
		* `use  appts-api`
		* `db. dropDatabase()`

* Creation of the appts-api database is automatic the first time you run a valid endpoint:
	* In postman just run the entire collection or the 'POST create new auth creds' end point





