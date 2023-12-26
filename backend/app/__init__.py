from os import getenv
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    if getenv("FLASK_ENV") != "production":
        load_dotenv()
        app.config['DEBUG'] = True

    db_user = getenv('DB_USER')
    db_pass = getenv('DB_PASSWORD')
    db_name = getenv('DB_NAME')
    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')
    log_level = getenv('LOG_LEVEL', "INFO")

    try:
        app.logger.setLevel(log_level)
    except ValueError as ex:
        app.logger.error(
            "Log level \"%s\" is invalid! Logging may not work as expected!", log_level, exc_info=ex)

    db_uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.routes import error_handlers
        from app.routes import tasks

    return app
