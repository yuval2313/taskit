from flask import jsonify
from flask import current_app as app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from app.errors.http import CustomHTTPException


@app.errorhandler(HTTPException)
def handle_exception(ex: HTTPException):
    app.logger.warning(
        "Handling a default http exception - description: %s, code: %s", ex.description, ex.code)

    response = {
        "description": ex.description,
        "code": ex.code,
    }

    return jsonify(response), ex.code


@app.errorhandler(CustomHTTPException)
def handle_http_exception(ex: CustomHTTPException):
    app.logger.warning(
        "Handling a custom http exception - description: %s, code: %s", ex.description, ex.code)

    response = {
        'description': ex.description,
        'code': ex.code
    }

    if hasattr(ex, 'payload'):
        response['payload'] = ex.payload

    return jsonify(response), ex.code


@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(ex: SQLAlchemyError):
    app.logger.error("Handling an SQLAlchemy error", exc_info=ex)

    response = {
        'description': 'Internal Server Error',
        'code': 500
    }
    return jsonify(response), 500
