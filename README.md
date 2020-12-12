# TSL Full Stack Assignment

### Prerequisites

This project requires [Python](https://www.python.org/downloads/), [pip](https://pypi.org/project/pip/) and [VirtualEnv](https://pypi.org/project/virtualenv/) installed.

It's also needs a [gmail account](https://www.google.com/intl/pt/gmail/about/) with [less secure apps enabled](https://support.google.com/accounts/answer/6010255?hl=en) 

### Installing

Clone the repository

```
https://github.com/dokawa/tsl-django-rest-backend
```


Install the project dependencies

```
cd tsl-django-rest-backend
pip install -r requirements.txt
```

### Defining credentials

```
export EMAIL_HOST_USER = <your_username>
export EMAIL_HOST_PASSWORD = <your_password>
```

### Alternative method for credentials
Note: This step isn't necessary if the previous one was followed

Create a file

```
credentials/credentials
```

Following the example of [credentials_example](https://github.com/dokawa/tsl-django-rest-backend/blob/master/credentials/credentials_example)


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
needed to configure it to work with Django

### Future work

* More secure authentication method like OAuth 2.0
* Support for posting images, videos and urls
* Use another method to send emails, possibly a third-party service

 
