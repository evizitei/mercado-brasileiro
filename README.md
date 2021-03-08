# mercado-brasileiro

This is a for-school project for as single project group in CS 411 at UIUC for graduate level databases course in spring 2021.

## Development setup

1) Install Docker
The project is constructed on top of [docker](https://docs.docker.com/get-docker/) (to isolate all dependencies
for the project) and [docker-compose](https://docs.docker.com/compose/install/)
(for establishing orchestration for the multiple containers involved.) You'll want to install both
of those before you continue.

2) Build your containers, which will download the images for the python container and the postgres container.
`docker-compose build`

3) bootstrap your env vars:PUT WHAT IS IN THE ".env_example"
file in "mercado_brasileiro" directory into a ".env" file in the same directory as "settings.py".

3) get your data archive from the olist dataset in place
for the db bootstrap in data/olist.zip.

4) run the database_init script, which will unzip
your data archive, create your db, apply migrations,
 import data, and create the root admin user:
`docker-compose run --rm web python scripts/database_init.py`

5) Start the app to make sure it works: `docker-compose up`


### Ongoing State Changes

Anytime you add a new dependency to requirements.txt,
don't forget you need to re-build the container to have it
installed.

```bash
docker-compose build web
```

Anytime you make a model change (models.py), you need to generate a new
migration for the change against the db, which
can be done from the root directory of the project:

```bash
python manage.py makemigrations mercado_brasileiro
```

And then you can run migrations to catch your curent

```bash
python manage.py migrate
```

## Operational Environment

This application is deployed on cpanel at http://mercadobrazil.web.illinois.edu/ .
The virtual machines there use passenger to act as the web server
to put python apps behind, and our application is configured to use
passenger_wsgi.py as the interface file along with "serve.py" as the file
it loads (for a hello-world configuration).

We've changed passenger_wsgi.py to point to do the same thing the generated
"wsgi.py" script does in the app directory, so it loads the django app
on boot now.

You probably want this in your ssh config if you want to ssh to the server:

```bash
Host cpanel
  HostName 18.220.149.166
  User mercadobrazil
  IdentityFile ~/.ssh/[your key you generated and authorized]
```

Settings are bootstrapped into the app via the settings.py file
but not all settings can be put in the repo
(things like passwords and keys should differ by environment
and should not be exposed to github).  We use a ".env" file
which is NOT committed to the repository.

there is a virtual environment on the server for python
and dependencies, make sure you're using it for anything
python related by running:

```bash
source /home/mercadobrazil/virtualenv/mercado-brasileiro/3.8/bin/activate
```

IF YOU ARE DEVELOPING LOCALLY, PUT WHAT IS IN THE ".env_example"
file into a ".env" file in the same directory as "settings.py"

In production, there is a .env file on the server that has
all the secrets in it which is not in the repo so it can have
it's own settings.

Using the information in that file, you can connect to the database
as the app user for example:

```bash
 psql -U mercadobrazil_app -d mercadobrazil_prod -h 127.0.0.1
```
(use the password specified in the .env file)

#### Deployment

since we're operating on a single server for this project, the deploy process is
pretty straightforward.


1) ssh to the server

```bash
ssh cpanel
```

2) pull the master branch to get the latest code
```bash
cd ~/mercado-brasileiro
git pull origin master
```

3) tell passenger to restart the application server
```bash
cd ~/mercado-brasileiro
touch tmp/restart.txt
```

A deploy script has been added to bin/deploy that does exactly this.

#### Database Bootstrapping

Whether locally or on the server, we're basing our application
on the dataset here
(https://www.kaggle.com/olistbr/brazilian-ecommerce).
This means we need to get that data into our database to do
anything.  Putting all the data in the repo would be
overkill, so there is a utility in "scripts/database_init.py"
that takes care of forcing all this data into tables
in the database.  Make sure to download the zip file for
the dataset and put it in "data/olist.zip". Then:

```bash
python scripts/database_init.py
```

from the root directory of this project (either in your local
docker container shell or on the server) and the script will
open the archive, create tables as necessary, import
data, and create your root admin user.

This process is idempotent, you can run it multiple
times and it will only do the work that it detects is not done.

postgres command line tools are installed in the 
docker container, so you can check on the db state
from the command line at any time using psql:

```bash
psql -d mercadobrazil_dev -h db -U postgres
```

(password is "sekret", as configured in docker-compose)

MongoDB is also installed in the docker container,
so you can talk to the mongo database container
by getting a shell in your "web" container and running:

```bash
mongo --host=mongo
```

### Auth and Admin
The Django app has an admin area built into it as part of the django
framework, with tables that are namespaced under "auth" in the schema.

The database init script will create one root user, but if you want
to have another admin user for yourself (which you should!) you can
create one from the shell with:

```bash
python manage.py createsuperuser
```
REMEMBER: ^ if you're on the production server you need
to have activated the python virtualenv in order to run
python commands with our dependencies successfully!

```bash
source /home/mercadobrazil/virtualenv/mercado-brasileiro/3.8/bin/activate
python manage.py createsuperuser
```

when your super user is created, you should be able to login
with your superuser username and password at the "/admin"
path on your server hostname.  This provides access
to administration for users and groups.
