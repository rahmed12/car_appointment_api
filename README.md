# Car appointment api
> REST API that can store and manage appointments fora car service center.
<hr>



# Table of Contents
* [Prerequisite: Make sure you have the follow](#Prerequisite)
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


# <a name="Setup"></a>Setup
* If you want to watch a video version of this, here is the link [![Car Serive appointment API](https://img.youtube.com/vi/VID/0.jpg)](https://youtu.be/UVpPy3DLpBs)
* From the repository https://github.com/rahmed12/car_appointment_api.git get these files and put it on your linux machine (you don't need the whole repository since we are using docker):
	* __appts_api.postman_collection.json__
		* This is for Postman
	* __docker-compose.yaml__
		* This is for docker

* Start Postman and import the file __appts_api.postman_collection.json__
	* you should have a new collection called appts api
	
	![1_postman](https://user-images.githubusercontent.com/47451663/101697730-569a3300-3a46-11eb-9750-67a7b6a37e5e.PNG)
	* If you expand the collection you should have tow entries called auth and appts
	
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





