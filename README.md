# Project Name
> Abstract of the project or small introduction of what the project is about
<hr>

Prerequisite
Linux
Docker
Postman





Installation
From the repository get these files and put it on your linux machine (you don't need the whole repository sine we are using docker):
appts_api.postman_collection.json – for postman
docker-compose.yaml – for docker


Start Postman and import the file:
appts_api.postman_collection.json
you should have a new collection called appts api

In postman we are using localhost with the endpoints
We are using 0.0.0.0 for the localhost so make sure your localhost is set to 0.0.0.0
We are using default port 80

Run this command on your linux machine :

make sure the docker-compose.yaml file is in the same directory you run this command in:
docker-compose run --service-ports  web_run

The reason for the service-ports flag is to let postman send info to the container


Once this command is done you should have two images:

mongo                               3.6.3
rasaldocker/carapptapi_web          latest

You should also have two containers running:
<directory name>_web_run_run_<num> 
carapi_db_1

Test
There are two ways of testing
1. Postman:
1. Run the collection name appts api
2. It will output the test success or failures
3. if you run it again it will failure in some place
1. If you want to rerun again just drop the database (instructions below in extra)
2. unnitest 
1. docker exec -it <container name>_web_run_run_<number> python test.py
2. this will report any failures or success from any tests.py files
1. app_auth/tests.py
2. appt/tests.py



Extra
If you need to access the mongodb you can do this (while your containers are running):
docker ps
get the container name for carapptapi_web:latest

docker exec  -it <container name> mongo -host mongodb

You should be on the mongodb.  To show database:
show dbs

To select our database:
use appts-api

To see the collections:
 show collections

To see what's in the collection (for example we want to see what's inside of our token collection):
db.tokens.find()

To drop the  appts-api database
use  appts-api
db. dropDatabase()

Creation of the appts-api database is automatic the first time you run a valid endpoint:
	1. In postman just run the entire collection or the 'POST create new auth creds' end point

