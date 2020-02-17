COMP590
==============================

Final project for UNC COMP 590: Geospatial Store

Project Organization
------------

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
│   │   ├── app                 <- Directory that holds all flask application logic and frontend
│   │   │   ├── static          <- Directory to hold static files for the `Flask` application
│   │   │   ├── templates       <- Directory to hold all .html templates for the Flask application
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

--------
