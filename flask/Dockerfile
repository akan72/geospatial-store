FROM tiangolo/uwsgi-nginx-flask

# Set working directory to /app
WORKDIR /app

# Copy the current directory (flask) contents into the container at /app
ADD . /app

# Install dependencies 
RUN pip install -r requirements.txt

# start uWSGI
CMD ["uwsgi", "uwsgi.ini"]