# Airavata Custos Portal

## How to use

Airavat custos portal is available as a python package to install and customise for tenants needs.
The forllowing instructions are for setting up a customised portal using all the features available
in the airavata custos portal.

## Development

The application consists of a Vue.js frontend and a Django based backend. 
The instructions below are for setting up the local setup for development.

### Change the configurations

Change the environment variables on `.env`

### Run Vue.js app

```
yarn install
yarn serve
```

### Lints and fixes files

```
yarn lint
```

## Running the Django server locally

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd airavata_custos_portal/
./manage.py migrate
./manage.py runserver
```

And then point to http://localhost:8000

## How to publish

1. Build the static files
```
yarn build
```

2. Build the python package

```
python -m pip install --upgrade build
python -m build
```

3. Publish the python package to pypi.org. Optionally can push to test.pypi.org. See https://packaging.python.org/tutorials/packaging-projects/ for more info.

```
python -m pip install --upgrade twine
python -m twine upload dist/*
```
