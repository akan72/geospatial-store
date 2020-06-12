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

Dashboard

From the index, we have also included a Dashboard where users can see the historical results of trained models. Every request to the API is logged within a SQLite database that stores the user_id of the requester, the time of the request, as well as the type of model and its result.

The dashboard may be filtered by user_id or by model_type, and users can view the original image submitted as well as new images outputted by models performing tasks like segmentation.

------------

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
│   ├── Dockerfile
│   ├── data
│   │   ├── raw             <- Directory of sample images for the various models
│   ├── main.py                 <- Entrypoint for the `Flask` application
│   ├── models                  <- Directory of Trained and serialized models used for making predictions
│   ├── notebooks               <- Directory of Jupyter notebooks for exploration and model testing
│   ├── requirements.txt        <- The requirements file for reproducing the analysis environment
│   ├── src
│   │   ├── app
│   │   │   ├── static
│   │   │   │   ├── uploads     <- Temporary location for all images uploaded to our application
│   │   │   ├── templates       <- Directory of templates for the `Flask` application
│   │   │   ├── models.py       <- Contains the schema for our API's prediction results
│   │   │   └── views.py        <- Backend logic for the `Flask` application
│   │   ├── models              <- Scripts to train and serialize models
│   │   └── visualization       <- Scripts to perform exploratory data analysis and visualization
│   ├── test_requests.py        <- Example of how to use our API using Python's `requests` package
|   ├── create_db.py            <- Script that initializes the SQLAlchemy database
│   └── uwsgi.ini               <- uWSGI config file
├── nginx
│   ├── Dockerfile
│   └── nginx.conf              <- `Nginx` configuration file
└── reports                     <- Generated analysis as HTML, PDF, LaTeX, etc.
    └── figures                 <- Generated graphics and figures to be used in reporting

```

------------

Future Work

- Upload the container to Docker Hub
- Add aggregate counts by date to the dashboard, show examples for computing aggregated statistics about different models
- Create pipeline to ingest Google Earth Engine Polygons for other GEE models
- Define spec and create example for others to submit additional models

------------
