# Secure Login System
This project aims to build a secure and reliable Flask Authentication system.
The project makes use of the Flask-Login module for user session management and access control. It handles logging users in, logging users out and remembering user sessions. The Flask WTForms library is used in this project to handle form rendering and form validations. Bcrypt is used for salting and hashing passwords before they are passed to the database and also for matching attempted passwords against the stored hashes during log in attempts. Roles Based access-control is also employed here to prevent users without the required permissions from gaining access to certain pages. Flask-Mail is also employed for delivering timed email validation mails to new users. Views/pages are also restricted to unconfirmed users.

## Demo

https://user-images.githubusercontent.com/38054491/188340511-f3e6349d-2107-473a-b9f4-8b14040c9060.mp4


## Project structure
```
ROOT DIRECTORY

|--   config.py
|--   README.md
|--   requirements.txt
|--   run.py
|          
+---app
|   |---database.db
|   |---email.py
|   |---models.py
|   |---__init__.py
|   |   
|   +---main
|   |       |--   errors.py
|   |       |--   views.py
|   |       |--   __init__.py
|   |    
|   +---static
|   |       +---css
|   |       |    |-- styles.css
|   |       |    |-- styles.css  
|   |       |
|   |       +---images        
|   |            |-- CU.png
|   |            |-- rick.png
|   |
|   +---templates
|   |       +---auth
|   |           |-- login.html
|   |           |-- register.html
|   |           |-- unconfirmed.html
|   |
|   |       |--- base.html
|   |       |--- home.html
|   |       |--- admin_hub.html
|   |       |--- message.html
|   |       |--- navbar.html
|   |       |--- 500.html
|   |       |--- welcome.html
|   |       |--- info.html
|   |       |--- 403.html
|   |       |--- 404b.html
|
|           
+---venv
|
+---migrations
```
## Bringing up the application

- Setup and activate a new virtual environment `python -m venv env` activate `source env/Scripts/activate`
- Run `pip install -r requirements.txt` to download dependencies, N/B Application was built using Python 3.9.6
- Set environmental variables `export FLASK_APP=run.py` and `export FLASK_DEBUG=true`
- Run `flask run` to initialize and instance of the application.
- To avoid alembic error during migration use `migrate.init_app(app, db, render_as_batch=True)` to create fresh table and move data.
