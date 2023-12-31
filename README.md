# Task-it

Task-it is a simple task management / post-it application backed by a Flask backend which serves static files developed and built using React.

## Dependencies

**Requirements:**

- [**`Node.js 20`**](https://nodejs.org/en)
- [**`Pipenv`**](https://pipenv.pypa.io/en/latest/installation.html)

#### Backend

```sh
mkdir flask-backend/
pipenv install
```

#### Frontend

```sh
mkdir react-frontend/
npm install
```

## Development

In order to deploy the application in a development environment one may initialize the front and back ends as separate processes by following the following steps:

**1) Initialize Database**
Set up a PostgreSQL database and run migrations against it.
For convenience one may use the `docker-compose.yml` file in the root directory of the repository and simply run some of the services:

```sh
docker compose up db migrations
```

> Be sure to pass the relevant environment variables and expose the database port on your local machine.

**2) Deploy Flask Application**
Run the flask application and pass the corresponding environment variables for establishing a proper connection to the database.
You may reference the `flask-backend/.env.example` file and create a `.env` file of your own.

```sh
pipenv run start
```

**3) Deploy React Application**
Finally, deploy the react application using `npm`, be sure to pass in the `REACT_APP_API_URL` environment variable pointing to the backend application, see `react-backend/.env.example`.

```sh
npm run start
```

## Production

For production the frontend is meant to be served directly from the Flask application.
As such you must build the React application source code and place all the files within a single directory called `static/`, placing it within the `flask-backend/app/` directory.
Configure the `REACT_APP_API_URL` to be empty and then build the react application using `npm run build`.

For convenience you may use the custom `flask-build` script, and optionally pass in the location in which the `static/` directory should end up.
Be sure to set appropriate permissions to be able to run the custom script.

```sh
mkdir react-frontend/
chmod +x ./flask-build.sh
npm run flask-build ../flask-backend/app
```

After which one may simply run the flask application as before without requiring the frontend as a separate process.

## Docker

In order to deploy the application as a docker container one may simply initialize it using the `docker-compose.yml` at the root directory.
This will utilize the `Dockerfile` to build a container image ready to serve the application.
It will also front the application using an Nginx container as a reverse-proxy, and take care of initializing the database as well as running migrations against it.

```sh
docker compose up
```

> Be sure to set the appropriate environment variables for the application and migration containers to correspond to the credentials passed into the database container.

## Architecture

When deploying Task-it we get a 3 tier application structure:

![architecture.png](./docs/architecture.png "Application Architecture Diagram")

1. **db** - The database is initialized and configured, it persists its data on the host machine.
2. **migrations** - This is a container which executes database migrations for initializing the database tables and then exits (a job). It uses the same docker image as the application itself, though it executes a different process.
3. **app** - Here we have the Flask application itself, which manages API routes and can serve static files.
4. **nginx** - Finally, Nginx acts as a reverse-proxy and forwards requests to the backend while acting as a single point of entry to the application. It also holds some of the static files and can serve them directly without "troubling" the backend so to speak.
