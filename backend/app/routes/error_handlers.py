from flask import jsonify, json
from flask import current_app as app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from app.errors.http import CustomHTTPException


@app.errorhandler(HTTPException)
def handle_exception(ex: HTTPException):
    response = ex.get_response()
    response = {
        "description": ex.description,
        "code": ex.code,
    }

    return jsonify(response), ex.code


@app.errorhandler(CustomHTTPException)
def handle_http_exception(ex: CustomHTTPException):
    response = {
        'description': ex.description,
        'code': ex.code
    }

    if hasattr(ex, 'payload'):
        response['payload'] = ex.payload

    return jsonify(response), ex.code


@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(ex: SQLAlchemyError):

    response = {
        'description': 'Internal Server Error',
        'code': 500
    }
    return jsonify(response), 500
