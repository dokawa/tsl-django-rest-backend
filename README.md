# TSL Full Stack Assignment

### Prerequisites

This project requires [Python](https://www.python.org/downloads/), [pip](https://pypi.org/project/pip/) and [VirtualEnv](https://pypi.org/project/virtualenv/) installed

It's also needs a [gmail account](https://www.google.com/intl/pt/gmail/about/) with [less secure apps enabled](https://support.google.com/accounts/answer/6010255?hl=en) 

The project is also hosted on [Heroku](https://tsl-react-frontend.herokuapp.com/)

ATTENTION: the hosted version does not send e-mails due to restrictions on Gmail, (it could be corrected with a production e-mail service) the local version send it as requested in the assignment

### Installing

Clone the repository

```
https://github.com/dokawa/tsl-django-rest-backend
```

### Creating virtualenv

On Linux

```
cd tsl-django-rest-backend
python3 -m venv env
source env/bin/activate
```

On Windows

```
python3 -m venv env
cd env/Scripts
activate.bat
```

Install the project dependencies

```
pip3 install -r requirements.txt
```

### Defining e-mail server credentials

```
export EMAIL_HOST_USER = <your_gmail_username>
export EMAIL_HOST_PASSWORD = <your_gmail_password>
```

### Alternative method to define credentials
Note: This step isn't necessary if the previous one was followed

Create a file named '.env' in the project root directory with the following info

```
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=<your_gmail_username>
EMAIL_HOST_PASSWORD=<your_email_password>
```

### Running the application

```
python manage.py runserver
```

### Testing

```
python manage.py test
```

### This app was build with

[Django REST Framework](https://www.django-rest-framework.org/)

### Considerations

* Given the non critical nature of the assignment, the authentication method
is simple and overall effective, but not the most secure
* Still on the non criticality and security aspect, the SECRET_KEY of the application is included 
in the repository although clearly not recommended on production applications
* The Gmail e-mail account was chosen given it's popularity and little effort 
needed to configure it to work with Django, although not recommended to have your account in 
this configuration or use Gmail in production 
* The dbsqlite3 is included in the repository with pre-registered users and messages 
in favor of simplicity to run the assignment locally

### Future work

* More secure authentication method like OAuth 2.0
* Support for posting images, videos and urls
* Use another method to send emails, possibly a third-party service
* Use a html template for e-mails

 
