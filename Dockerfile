FROM python:3.10.12-alpine AS base

FROM base AS python-build

WORKDIR /flask-app

# Install pipenv and compilation dependencies
RUN pip install pipenv

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
ENV PIPENV_VENV_IN_PROJECT=1 
RUN pipenv install --deploy

### ----------------------------------- ###

FROM node:20-alpine as node-build

WORKDIR /react-app

# Install node dependencies
COPY react-frontend/package.json .
COPY react-frontend/package-lock.json .
RUN npm install

# Copy application code
COPY react-frontend/ .
RUN chmod +x ./flask-build.sh

# Compile production build for flask application
RUN npm run flask-build

### ----------------------------------- ###

FROM base AS runtime

WORKDIR /taskit
# Copy virtual env from python build stage
COPY --from=python-build /flask-app/.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Copy flask application into container
COPY . .
RUN chmod +x ./init.py

# Copy static files from node build stage
COPY --from=node-build /react-app/build/static ./app/static

# Remove react application source code
RUN rm -rf ./react-frontend/

# Run the application
ENTRYPOINT ["python3"]
CMD ["init.py"]

