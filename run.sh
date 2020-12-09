docker-compse build



docker-compose up -d db
# expose service ports if you need to run pdb with docker
docker-compose run --service-ports web
docker exec  -it carapptapi_web_run_run_39 mongo -host mongodb


# for testing
docker exec -it carapptapi_web_run_run_41 python test.py


# to get docker web number running
docer_web_nu=`docker ps | grep -Eo '(_web_run_run_)[0-9]{1,3}' | grep -Eo '[0-9]{1,3}'`

docker exec -it carapptapi_web_run_run_`docker ps | grep -Eo '(_web_run_run_)[0-9]{1,3}' | grep -Eo '[0-9]{1,3}'`  mongo -host mongodb
use appts-api
use appts-api


