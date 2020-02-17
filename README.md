COMP590
==============================

Final project for UNC COMP 590: Geospatial Store

We use the [uwsgi-nginx-flask](https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/) Docker image to deploy the application, along with Docker Compose to build and configure our services. We have one service for `Flask` and one service for `Nginx`.

Setup
------------
First, clone this repository to your local machine and `cd` into it: 
```
git clone https://github.com/akan72/comp590
cd comp590
```

Next, we must set up the `Flask` development environment. This repository utilizes the `dotenv` package to manage app settings. 
Starting off, we will use `development` mode and thus flask requires us to define two environment variables.

```
echo "FLASK_APP=src/app/__init__.py" >> flask/.env
echo "FLASK_ENV=development" >> flask/.env
```

Build and Test 
------------
To build our services, we will now begin using `Docker Compose`. After starting up the Docker daemon on your machine, run:

```
docker-compose build
docker-compose up 
```

The following achieves the same result:

```
docker-compose up --build
```
The app may now be viewed by visiting http://127.0.0.1/ or http://localhost/ in a web browser.
You must rebuild the image every time changes are made, but if you wish to restart the application without having made changes, only need to run:

```
docker-compose up
```

For rapid development and testing, the `Flask` application can be run without the web services by running `flask run` within the `flask` directory and navigating to http://127.0.0.1:5000/.


Project Directory Organization
------------
```
├── LICENSE                     
├── README.md                   
├── docker-compose.yml          <- Configuration file for Docker Compose 
├── flask                        
│   ├── Dockerfile              <- Dockerfile for the `Flask` service
│   ├── data                    
│   │   ├── external            <- Data from third party sources
│   │   ├── interim             <- Intermediate data that has been transformed
│   │   ├── processed           <- The final, canonical data sets for modeling
│   │   ├── raw                 <- The original, immutable data dump
│   │   └── uploads             <- Directory to store images uploaded to the application
│   ├── main.py                 <- Entrypoint for the `Flask` application
│   ├── models                  <- Trained and serialized models, model predictions, or model summaries
│   ├── notebooks               <- Jupyter notebooks for exploration and model testing
│   ├── requirements.txt        <- The requirements file for reproducing the analysis environment
│   ├── src                     <- Directory that holds all app application and modeling code
│   │   ├── app                 <- Directory that holds all `Flask` application logic and frontend
│   │   │   ├── static          <- Directory to hold static files for the `Flask` application
│   │   │   ├── templates       <- Directory to hold all .html templates for the `Flask` application
│   │   │   └── views.py        <- Script that contains all `Flask` application logic
│   │   ├── data                <- Scripts to download or generate data
│   │   ├── features            <- Scripts to turn raw data into features for modeling
│   │   ├── models              <- Scripts to train models and then use trained models to make predictions
│   │   └── visualization       <- Scripts to create exploratory and results oriented visualizations
│   ├── test_requests.py        <- Script to test the API using python's `requests` package
│   └── uwsgi.ini               <- uWSGI config file
├── nginx                       
│   ├── Dockerfile              <- Dockerfile for the `nginx` service
│   └── nginx.conf              <- Nginx configuration file
├── references                  <- Data dictionaries, manuals, and all other explanatory materials
└── reports                     <- Generated analysis as HTML, PDF, LaTeX, etc.
    └── figures                 <- Generated graphics and figures to be used in reporting
```
--------
