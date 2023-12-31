import subprocess
from os import getenv
from app import create_app

flask_app = create_app()

if __name__ == "__main__":
    if getenv("FLASK_ENV") == "production":
        # Use Gunicorn for production
        gunicorn_cmd = [
            "python3",
            "-m",
            "gunicorn",
            "--bind", f"0.0.0.0:{getenv('PORT', '5000')}",
            "--workers", "4",  # Adjust the number of workers as needed
            "--log-level", "info",
            "init:flask_app"
        ]
        subprocess.run(gunicorn_cmd, check=True)
    else:
        # Use Flask's built-in development server for other environments
        flask_app.run(host="0.0.0.0", port=getenv("PORT", "5000"))
