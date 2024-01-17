from flask import request, current_app as app


@app.after_request
def logging_interceptor(response):
    protocol = request.environ.get('SERVER_PROTOCOL')
    app.logger.info(
        f'"{request.method} {request.path} {protocol}" -- {response.status_code}')

    return response
