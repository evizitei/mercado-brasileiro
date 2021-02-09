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

3) run the initial migrations to bootstrap your db:
`docker-compose run --rm web python manage.py migrate`

4) Start the app to make sure it works: `docker-compose up`

## Operational Environment

This applicaiton is deployed on cpanel at http://mercadobrazil.web.illinois.edu/ .
The virtual machines there use passenger to act as the web server
to put python apps behind, and our application is configured to use
passenger_wsgi.py as the interface file along with "serve.py" as the file
it loads (for a hello-world configuration).