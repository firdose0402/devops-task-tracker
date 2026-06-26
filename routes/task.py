from flask import Blueprint, jsonify, request
from api import db  # Import the db instance from api.py

task_bp = Blueprint('tasks', __name__)


# Define the Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Helper to convert database objects to JSON response format"""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed
        }


# 1. Get all tasks from the database
@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    return jsonify({"tasks": [task.to_dict() for task in all_tasks]}), 200


# 2. Get a single task by ID
@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify(task.to_dict()), 200
    return jsonify({"error": "Task not found"}), 404


# 3. Create and save a new task
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(
        title=data['title'],
        completed=data.get('completed', False)
    )

    db.session.add(new_task)  # Stage the new task
    db.session.commit()  # Permanently save it to the database file

    return jsonify(new_task.to_dict()), 201


# 4. Update an existing task in the database
@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.completed = data.get('completed', task.completed)

    db.session.commit()  # Save changes
    return jsonify(task.to_dict()), 200


# 5. Delete a task permanently
@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)  # Remove from database session
    db.session.commit()  # Apply changes to the database file

    return jsonify({"message": "Task deleted successfully from database"}), 200