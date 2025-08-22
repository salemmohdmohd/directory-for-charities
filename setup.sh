#!/bin/sh

pipenv install
pipenv run flask db migrate
pipenv run flask db upgrade
pipenv run start
