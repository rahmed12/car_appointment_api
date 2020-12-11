#
#
# car appointment api Dockerfile
#
#
#


# Pull base image of python
FROM python:3.7.3-slim

# Get some custom packages
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gcc \
    python3-dev \
    vim \
    mongodb


## make a local directory
RUN mkdir -p /opt/car_appt_api

# set "car_appt_api" as the working dir from which CMD, RUN, ADD references
WORKDIR /opt/car_appt_api

# now copy all the files in this dir
ADD . .

# pip install the local requirements.txt
RUN pip install -r requirements.txt

# Listen to port 5000 at runtime
EXPOSE 5000

# start the app server with a custum command
#CMD python manage.py runserver
CMD /opt/car_appt_api/docker_cmd_commands
