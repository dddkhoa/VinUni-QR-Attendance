# Got It's Backend Training Final Project

## Requirements

- Python 3.7+
- MySQL 5.7+

## Installation

### Set up virtual environment

```shell
pip install virtualenv
virtualenv venv
source ./venv/bin/activate
```

### Install dependencies

```shell
pip install -r requirements-dev.txt
```

### Install `pre-commit` hooks

- Install `pre-commit`: https://pre-commit.com/
- Install `pre-commit` hooks:

  ```shell
  pre-commit install
  ```

## Running

### Running MySQL to initialize database 
#### Run these lines in mysql server
```shell
create database catalog;
use catalog;
```


### Setting up database with Flask Migration
```shell
flask db init
flask db migrate
flask db upgrade
```

Inside the virtual environment, run

```shell
python run.py
```

## Testing
```shell
ENVIRONMENT=test pytest
```

## Get Coverage Report
```shell
ENVIRONMENT=test coverage run -m pytest
coverage html
```
