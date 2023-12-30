# cp-skeleton

### Skeleton CherryPy web application based on
- Cherrypy (web framework)
- Jinja2 (templating engine)
- SQLAlchemy (ORM)
- Alembic (Database versioning)
- JQuery (Javascript framework)
- Bootstrap (CSS framework)
- Icons by Icons8 (icons8.com)

# Getting Started
First make a copy of the skeleton project. You then have the option to keep the skeleton git history or recreate a fresh git history.

### Initialize new git history w/o skelton history (optional)
```
cp -r cp-skeleton myproject
cd myproject
rm -rf .git
git init
git add {lots of things}
```

### Initialize new virtual env
Next setup the new python virutalenv environment and install requirements. It's optional to use system-site-packages or not.
```
python -m venv --system-site-packages venv
pip install -r requirements.txt
. venv/bin/activate
```


### Rename things from PROJECTNAME to your actual project name
```
git grep PROJECTNAME
```


### Install the conf file
```
cp {projectname}.conf.sample {projectname}.conf
```

### Create the database
```
venv/bin/alembic upgrade head
```

### Create directory for sessions
```
mkdir sessions
```

### Start the development server
```
python run.py [--host 127.0.0.1] [--port 9000]
```

# Development 

### Template feature examples
The index.html file shows a few features built into this skeleton
- base.html defines the header and footers and menu for all pages. This just an example, not a requirement
- head, title, help, and content are blocks defined in base and intended to be overridden in each template
- the java script function set_message takes a string or a dictionary with a message and  css class to display a notification on the page.

### Add Model Classes to enable database management
- db_test.py
- alembic/env.py

# Using alembic
Alembic is already initialized in this skeleton project. This initialization process consists of running:
```
alembic init alembic
```
This command creates the alembic directory and the alembic.ini file. Further updates are made to the alembic/env.py file to integrate with CherryPy.

General usage is to make changes to your SQLAlchemy model but not your database, then run __*alembic revision*__ to generate an alembic version file and apply that version to update the database using __*alembic update*__. If you add new model classes to your project, they will need to be added to the alembic/env.py file to be included in the version file.

```
alembic revision --autogenerate -m "revision message"
alembic upgrade head
```

If you have trouble running the alembic command you may need to install alembic into your virtual env and/or execute alembic directly from the virtualenv directory.
```
. venv/bin/activate
pip install --no-deps --force alembic
venv/bin/alembic revision --autogenerate -m 'Initial Database'
```


# Notes
- Not all CSS is bootstrap

# Future Topics for README
- Explain users / Notifications / Codes
- using tox to unit test
- installing production nginx/uwsgi deployment
- git hooks for prod deployment

# Code TODO
- Variableize PROJECTNAME so it's not in so many places