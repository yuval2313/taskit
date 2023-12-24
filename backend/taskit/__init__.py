from os import getenv
from dotenv import load_dotenv
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    if getenv("FLASK_ENV") != "production":
        load_dotenv()
        app.config['DEBUG'] = True

    db_user = getenv('DB_USER')
    db_pass = getenv('DB_PASSWORD')
    db_name = getenv('DB_NAME')
    db_host = getenv('DB_HOST')

    # database uri
    db_uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:5431/{db_name}"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

    return app
