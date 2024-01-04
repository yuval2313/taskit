from flask import current_app as app, send_from_directory


@app.route("/")
def serve_index():
    return send_from_directory('react-build/', 'index.html')
