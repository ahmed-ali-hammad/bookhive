

<h3 align="center">Book API</h3>

<div align="center">
  <img src="https://img.shields.io/badge/status-active-success.svg" />
  <img src="https://img.shields.io/badge/python-3.13-blue" />
</div>

---

<p align="center">TODO: Short Description.
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
- [Built Using](#built-using)

## 🧐 About <a name = "about"></a>
TODO: Fill me in

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

 - [Docker](https://docs.docker.com/)
 - [Docker Compose](https://docs.docker.com/compose/)

### Installing

```bash
docker compose up
docker exec -it book_api/bin/bash 

pipenv shell  # spawns a shell within the virtualenv 
```


### ▶️ Running the webapp
TODO: Fill me in

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