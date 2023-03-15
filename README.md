# Hexocean

## Technologies Used
- Django
- Django Rest Framework
- PostgreSQL 

## Baza danych:

### Messages
- id
- body (not null, CharField(160))
- views PositiveIntegerField(default=0)


### User
- id
- username (max_length=160)
- password(max_length=128, hash)


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
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

