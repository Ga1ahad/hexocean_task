# Hexocean

## Technologies Used
- Django
- Django Rest Framework
- PostgreSQL 


## Available Urls
| URL  | HTTP Request Methods | HTTP Request | Description |
| ------------- | ------------- | ------------- | ------------- |
| api/token/  | POST | {     "username": "str",     "password": "str" } | Returns token |
| images  | GET | NA | Returns list of images |
| images/<int:img_id>  | GET | { "img_id": "int" }  | Returns image |
| images/upload  | POST | {     "image": ".png/.jpg" } | Creates images and thumbnails |
| images/<int:img_id>/expiring_img/<int:seconds>  | POST | { "seconds": "int" } | Creates expiring image |
| expiring_img/<int:img_id>/  | GET | { "img_id": "int" } | Returns image |


## Deployment 
- set up secrets
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate
