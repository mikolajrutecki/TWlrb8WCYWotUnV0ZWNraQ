# Fetcher

## Requirements

Make sure you have Python3 installed(tested on v3.6.7). 
Every library needed to run this project is listed in **requirements.txt**

To quickly install all these libraries(remember to create new virtualenv), simply run:

    pip install -r requirements.txt


Make sure you are in the project main category, then run:

    python manage.py makemigrations
    python manage.py migrate

This project is using **redis**, so you have to set it up. Docker will be nice for this.
After that, remember to change **/wp_project/settings.py** redis url
Example:

    CELERY_BROKER_URL = 'redis://localhost:32771'  
	CELERY_RESULT_BACKEND = 'redis://localhost:32771'

## How to run it
Run server and tell him to listen 8080 port:

    python manage.py runserver 8080

The API is available at:

    localhost:8080/api/fetcher


