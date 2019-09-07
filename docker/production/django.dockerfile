# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

RUN apt-get update

RUN apt-get install gettext -y

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /handyman

# Set the working directory to /handyman
WORKDIR /handyman

RUN pip install gunicorn
RUN pip install setproctitle

# Copy the current directory contents into the container at /handyman
COPY ./requirements.txt /handyman/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . /handyman/

COPY ./docker/production/django_conf/local_settings.py /handyman/markino/

# RUN python manage.py compilemessages

RUN rm -rf error_logs.log
