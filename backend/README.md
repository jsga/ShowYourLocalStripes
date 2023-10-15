# Backend ShowYourLocalStripes

Backend for [https://showyourlocalstripes.com/](https://showyourlocalstripes.com/).


## How to run locally


### Using docker compose

The easiest way to spawn a container with a local database and a backend instance:

```
docker compose -p climate -f docker-compose.dev.yml up -d --build 
```

The API should be accessible in [http://0.0.0.0:5001/docs](http://0.0.0.0:5001/docs)!

### Using a virtual environment

```
# Make sure to have poetry installed
curl -sSL https://install.python-poetry.org | python3 -

# Open a shell within the virtual environment
poetry shell

# Install packages
poetry install

# Run application
uvicorn api.main:app --port 5001 --reload
```

The Postgres database should be run locally as well.

## Migrations

Database migrations are defined in [alembic](https://alembic.sqlalchemy.org/en/latest/). 
After changes in the `api/models`, upgrade the database with:

```sh
alembic revision --autogenerate -m "init_commmit"
alembic upgrade head
```

## Secrets

Use [age](https://github.com/FiloSottile/age) to encrypt the secrets:

```
sops --input-type dotenv --output-type dotenv --age <age key> --encrypt  .prod.env > prod.env.encrypted
```
