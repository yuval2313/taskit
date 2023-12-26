from os import getenv
from app import create_app

flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=getenv("PORT", "5000"))
