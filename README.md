# mercado-brasileiro

This is a for-school project for as single project group in CS 411 at UIUC for graduate level databases course in spring 2021.

## Development setup

1) Install Docker
The project is constructed on top of [docker](https://docs.docker.com/get-docker/) (to isolate all dependencies 
for the project) and [docker-compose](https://docs.docker.com/compose/install/)
(for establishing orchestration for the multiple containers involved.) You'll want to install both
of those before you continue.

2) Start app
`docker-compose run --rm web django-admin startproject mercado_brasileiro`