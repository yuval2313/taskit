from flask import current_app as app


@app.route('/health')
def health_check():
    return "healthy"
