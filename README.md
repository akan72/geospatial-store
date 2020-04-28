COMP590
==============================

Final project for UNC COMP 590: Geospatial Store

We use the [uwsgi-nginx-flask](https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/) Docker image to deploy the application, along with Docker Compose to build and configure our services. We have one service for `Flask` and one service for `Nginx`.

Setup

------------
First, clone this repository to your local machine and `cd` into it:

```{shell}
git clone https://github.com/akan72/comp590
cd comp590
```

Next, we must set up the `Flask` development environment. This repository utilizes the `dotenv` package to manage app settings.
Starting off, we will use `development` mode and thus Flask requires us to define two environment variables.

```{shell}
echo "FLASK_APP=src/app/__init__.py" >> flask/.env
echo "FLASK_ENV=development" >> flask/.env
```

Run the script `create_db.py` to initialize the SQLAlchemy database on your local machine.

```{shell}
python flask/create_db.py
```

We use SQLAlchemy to create a light lightweight Object-Relational Mapping (ORM) to create a virtual Sqlite3 database for model
prediction results that lives in file. To view these results after running several models and creating the database,
you can run: 

```{shell}
sqlite3 flask/src/app/database.db
SELECT * FROM prediction;
```

Build and Test

------------
To build our services, we will now begin using `Docker Compose`. After starting up the Docker daemon on your machine, run:

```{shell}
docker-compose build
docker-compose up
```

The following achieves the same result:

```{shell}
docker-compose up --build
```

The app may now be viewed by visiting <http://127.0.0.1/> or <http://localhost/> in a web browser.
You must rebuild the image every time changes are made, but if you wish to restart the application without having made changes, only need to run:

```{shell}
docker-compose up
```

For rapid development and testing, the `Flask` application can be started without the webserver or container by running`flask run` within the `flask` directory and navigating to <http://127.0.0.1:5000/>.

Data Sources

------------
For sample satellite images one source is the [Planet Amazon Dataset](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space/data) from Kaggle. After logging in with a Kaggle account, the various .jpg datasets may be installed through the Kaggle CLI or directly downloaded to your machine in a compressed format.

Project Directory Organization

------------

```{markdown}
├── LICENSE
├── README.md
├── docker-compose.yml          <- Configuration file for Docker Compose
├── flask
│   ├── Dockerfile              <- Dockerfile for the `Flask` service
│   ├── data
│   │   ├── processed           <- The final, canonical data sets for modeling
│   │   ├── raw                 <- The original, immutable data dump
│   ├── main.py                 <- Entrypoint for the `Flask` application
│   ├── models                  <- Trained and serialized models, model predictions, or model summaries
│   ├── notebooks               <- Jupyter notebooks for exploration and model testing
│   ├── requirements.txt        <- The requirements file for reproducing the analysis environment
│   ├── src                     <- Directory that holds all application and modeling code
│   │   ├── app                 <- Directory that holds all `Flask` application logic and frontend
│   │   │   ├── static
            │   ├── uploads     <- Temporarily holds all images uploaded to the application
│   │   │   ├── templates       <- Directory to hold all .html templates for the `Flask` application
            ├── models.py       <- Script that contains the Schema for our API's prediction results
│   │   │   └── views.py        <- Script that contains all `Flask` application logic
│   │   ├── models              <- Scripts to train and serialize models, and then use to make predictions
│   │   └── visualization       <- Scripts to perform exploratory data analysis and visualization
│   ├── test_requests.py        <- Script to test the API using python's `requests` package
|   ├── create_db.py            <- Script to initialize the SQLAlchemy database
│   └── uwsgi.ini               <- uWSGI config file
├── nginx
│   ├── Dockerfile              <- Dockerfile for the `nginx` service
│   └── nginx.conf              <- Nginx configuration file
├── references                  <- Data dictionaries, manuals, and all other explanatory materials
└── reports                     <- Generated analysis as HTML, PDF, LaTeX, etc.
    └── figures                 <- Generated graphics and figures to be used in reporting
│   │   └── uploads<- Directory to store images uploaded to the application
```

------------
