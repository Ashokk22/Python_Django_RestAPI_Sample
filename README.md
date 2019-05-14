# IMDB celebrities search

A minimalistic Django project that demonstrates REST API production and consumption.

## Setup

The app needs some data seeding from IMDB data available [here](https://datasets.imdbws.com/ "IMDB datasets").
To download and seed data run: 
```bash
. createpyenv.sh
. loaddata.sh
``` 

*Note: For demonstration purpose the above setup only seeds data of 5000 celebrities.*


## Run app on local Django server

To run the app on Django server run the following command:

```bash
python manage.py runserver 0.0.0.0:8081
```

if everything goes well you should see something similar to..

```bash

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 14, 2019 - 13:15:17
Django version 2.2.1, using settings 'movies.settings'
Starting development server at http://0.0.0.0:8081/
Quit the server with CONTROL-C.
```

Access the home page at [http://localhost:8081/movies/home](http://localhost:8081/movies/home "Home").