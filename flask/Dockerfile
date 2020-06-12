FROM tiangolo/uwsgi-nginx-flask:python3.7

# Set working directory to /app
WORKDIR /app

# Copy the current directory (flask) contents into the container at /app
ADD . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# start uWSGI
CMD ["uwsgi", "uwsgi.ini"]

