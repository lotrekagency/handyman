# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.2

RUN apt-get update

RUN apt-get install gettext -y
RUN apt-get install sshpass -y
RUN apt-get install zip -y
RUN apt-get install rsync -y

# Copy keys

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh
COPY ./docker/production/keys /root/.ssh
RUN chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Create ssh files

RUN mkdir -p ~/.ssh/
RUN touch ~/.ssh/known_hosts

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
