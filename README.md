### INF601 - Advanced Programming in Python
### Jamie Smith
### Mini Project 4
 
 
# Project FortiDragon
 
**Forged in education. Focused on technology.**

_**Project FortiDragon**_: Empowering cybersecurity learning through real-world IT issue tracking.
 
## Description
 
_**Project FortiDragon**_ is a Django-based ticketing system designed to model a realistic IT helpdesk workflow. When users browse to the site, they are immediately redirected to the login screen, where they can either register or sign in using Django’s built-in authentication. Regular staff users can log in and submit new tickets describing technical issues, including a title, description, priority level, and automatic timestamps. Admin and technician accounts (staff users with the appropriate permissions) can view a dashboard of all tickets, filter down to pending tickets, and then approve and assign them either to themselves or to another technician through a dedicated assignment view. Each ticket moves through a simple lifecycle (pending → approved → assigned → closed), and the interface uses Bootstrap styling along with a custom banner and logos to present a clean, helpdesk-style web application. Overall, the project demonstrates user authentication, role-based permissions, form handling, and CRUD operations in Django while simulating how an internal IT support team would manage and track support requests.
 
The name _**Project FortiDragon**_ represents a fusion of cybersecurity functionality and the lessons learned through a career at Hutchinson Community College and academic work at Fort Hays State University. The project reflects a practical approach to vulnerability management through a custom Django-based web application.

## Getting Started
 
### Dependencies
 
* Download the program from https://github.com/jamielsmith1118/miniproject4JamieSmith
* Please install the pip necessary packages to run the program.


```
pip install -r requirements.txt
```
 
 
### Executing program
* Navigate to the FortiDragon directory

```
cd .\FortiDragon\
```

* Create migration files. These are the plans for database changes.
```
python manage.py makemigrations
```

* Apply the migrations to the database. This creates and updates the tables and fields.

```
python manage.py migrate
```

* Create a superuser for administrative tasks.

```
python manage.py createsuperuser
```

* Run the server.

```
python.py runserver
```

Once the server is running, access Project FortiDragon by launching a web browser and navigating to http://127.0.0.1:8000/ which will redirect to the login page. If a user has not previously registered, they will need to register before they can log in. Users can register by clicking the link labeled "Register Here."

To register, users need to provide a username, password, and then confirm their password. After registering, the user is redirected to the login page, where they should log in with the account they just registered.

If you see an error like ```django.db.utils.OperationalError: no such table: auth_user```, it means the migrations have not been applied yet. Run the commands above and try again.

 
## Authors
 
Jamie Smith
 
https://github.com/jamielsmith1118
 
## Version History
 
* 0.1
    * Initial Release
 
 
## Acknowledgments
 
Inspiration, code snippets, etc.
* [Django Tutorial](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)
* chatGPT using the HutchCC business subscription - Chat available upon approved request