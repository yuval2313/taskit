FROM python:3.10.12-alpine AS base

FROM base AS build

WORKDIR /app

# Install pipenv and compilation dependencies
RUN pip install pipenv

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
ENV PIPENV_VENV_IN_PROJECT=1 
RUN pipenv install --deploy

FROM base AS runtime

WORKDIR /app
# Copy virtual env from build stage
COPY --from=build /app/.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Install application into container
COPY . .
RUN chmod +x ./init.py

# Run the application
ENTRYPOINT ["python3"]
CMD ["init.py"]

