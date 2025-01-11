

<h3 align="center">BookHive</h3>

<div align="center">
  <img src="https://img.shields.io/badge/status-active-success.svg" />
  <img src="https://img.shields.io/badge/python-3.13-blue" />
</div>

---

<p align="center">BookHive API
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
- [Built Using](#built-using)

## 🧐 About <a name = "about"></a>
BookHive is an API that enables users to store, query, update, and delete book records.

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

 - [Docker](https://docs.docker.com/)
 - [Docker Compose](https://docs.docker.com/compose/)

### Installing

```bash
docker compose up
docker exec -it bookhive-dev /bin/bash   # spawns a shell within the docker container
pipenv shell  # spawns a shell within the virtualenv 
```


### ▶️ Running the webapp
```bash
source ./config/.env.example    # add the environment variables to the running terminal
fastapi dev ./src/main.py --host 0.0.0.0    # run the server in dev mode
```

- API Docs [http://0.0.0.0:8000/docs]
- Healthcheck endpoints [http://0.0.0.0:8000/health]


### Database Migrations

```bash
alembic init -t async migrations  # init the migrations folder
alembic revision --autogenerate -m "message"  # create a new migration version
alembic upgrade head  # apply the new migrations
```

### 🧪 Running the tests <a name = "tests"></a>
[pytest](https://docs.pytest.org/) is used for testing.

```bash
$ pytest tests/             # run all tests
$ pytest tests/unit         # run only the unit tests
$ pytest tests/integration  # run only the integration tests
```

### Code Style & Linting

 - [ruff](https://docs.astral.sh/ruff/)

### Python Package Management
[pipenv](https://pipenv.pypa.io/en/latest/) is used to manage Python packages. 

```bash
$ pipenv shell  # spawns a shell within the virtualenv
$ pipenv install  # installs all packages from Pipfile
$ pipenv install --dev # installs all packages from Pipfile, including dev dependencies
$ pipenv install <package1> <package2>  # installs provided packages and adds them to Pipfile
$ pipenv update  # update package versions in Pipfile.lock, this should be run frequently to keep packages up to date
```

## ⛏️ Built Using <a name = "built_using"></a>
- [FastAPI](https://fastapi.tiangolo.com/) - Web Framework.
- [PostgreSQL](https://www.postgresql.org/) - Database.
- [SQLModel](https://sqlmodel.tiangolo.com/) - ORM.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Database Migration.