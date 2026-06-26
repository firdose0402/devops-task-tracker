from flask import Flask
from task import task_bp  # Importing the blueprint from task.py


def create_app():
    app = Flask(__name__)

    # Global Configurations (e.g., Database, JWT settings can go here)
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Register Blueprints
    # This prefixes all routes in task.py with /api (e.g., /api/tasks)
    app.register_blueprint(task_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return {"message": "API Server is running. Use /api/tasks for task endpoints."}, 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)