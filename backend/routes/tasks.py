# backend/routes/tasks.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import Task
from backend.utils import (
    sanitize_string,
    parse_bool,
    parse_priority,
    parse_datetime,
)

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def task_to_dict(t: Task):
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "completed": bool(t.completed),
        "priority": t.priority,
        "due_date": t.due_date.isoformat() if t.due_date else None,
        "user_id": t.user_id,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "updated_at": t.updated_at.isoformat() if t.updated_at else None,
    }


@tasks_bp.get("")
@jwt_required()
def list_tasks():
    """
    List Tasks
    ---
    tags:
      - Tasks
    summary: List all tasks for the current user
    description: Returns all tasks belonging to the authenticated user.
    parameters:
      - in: query
        name: status
        type: string
        enum: [all, open, completed]
        required: false
        description: Optional filter by completion status.
    security:
      - BearerAuth: []
    responses:
      200:
        description: A list of tasks
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              completed:
                type: boolean
              priority:
                type: string
              due_date:
                type: string
                format: date-time
              user_id:
                type: integer
    """
    user_id = int(get_jwt_identity())
    status = (request.args.get("status") or "").lower()  # all|open|completed

    q = Task.query.filter_by(user_id=user_id)
    if status == "open":
        q = q.filter_by(completed=False)
    elif status == "completed":
        q = q.filter_by(completed=True)

    tasks = q.order_by(Task.created_at.desc()).all()
    return jsonify([task_to_dict(t) for t in tasks]), 200


@tasks_bp.post("")
@jwt_required()
def create_task():
    """
    Create Task
    ---
    tags:
      - Tasks
    summary: Create a new task
    description: Add a new task for the authenticated user.
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: Task payload
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              example: Finish Module 6 report
            description:
              type: string
              example: Write final reflection and upload PDF
            completed:
              type: boolean
              example: false
            priority:
              type: string
              enum: [Low, Medium, High]
              example: High
            due_date:
              type: string
              format: date-time
              example: "2025-11-30T10:00:00"
    responses:
      201:
        description: Task created successfully
      400:
        description: Title is missing or invalid
      401:
        description: Unauthorized or invalid token
    """
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    title = sanitize_string(data.get("title"))
    description = sanitize_string(data.get("description"))
    completed = parse_bool(data.get("completed"))
    priority = parse_priority(data.get("priority"))
    due_date = parse_datetime(data.get("due_date"))

    if not title:
        return jsonify({"message": "title is required"}), 400

    t = Task(
        title=title,
        description=description,
        completed=completed,
        priority=priority,
        due_date=due_date,
        user_id=user_id,
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(task_to_dict(t)), 201


@tasks_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id):
    """
    Get Single Task
    ---
    tags:
      - Tasks
    summary: Get a single task by ID
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: task_id
        required: true
        type: integer
        description: ID of the task
    responses:
      200:
        description: Task found
      404:
        description: Task not found
    """
    user_id = get_jwt_identity()
    t = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not t:
        return jsonify({"message": "task not found"}), 404
    return jsonify(task_to_dict(t)), 200


@tasks_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id):
    """
    Update Task
    ---
    tags:
      - Tasks
    summary: Update an existing task
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: path
        name: task_id
        required: true
        type: integer
        description: ID of the task to update
      - in: body
        name: body
        description: Fields to update (partial update allowed)
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Updated title
            description:
              type: string
              example: Updated description
            completed:
              type: boolean
              example: true
            priority:
              type: string
              enum: [Low, Medium, High]
              example: Low
            due_date:
              type: string
              format: date-time
              example: "2025-12-01T16:00:00"
    responses:
      200:
        description: Task updated successfully
      400:
        description: Invalid data (for example, empty title)
      404:
        description: Task not found
    """
    user_id = get_jwt_identity()
    t = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not t:
        return jsonify({"message": "task not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        new_title = sanitize_string(data.get("title"))
        if not new_title:
            return jsonify({"message": "title cannot be empty"}), 400
        t.title = new_title
    if "description" in data:
        t.description = sanitize_string(data.get("description"))
    if "completed" in data:
        t.completed = parse_bool(data.get("completed"))
    if "priority" in data:
        t.priority = parse_priority(data.get("priority"))
    if "due_date" in data:
        t.due_date = parse_datetime(data.get("due_date"))

    db.session.commit()
    return jsonify(task_to_dict(t)), 200


@tasks_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    """
    Delete Task
    ---
    tags:
      - Tasks
    summary: Delete a task by ID
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: task_id
        required: true
        type: integer
        description: ID of the task to delete
    responses:
      204:
        description: Task deleted successfully
      404:
        description: Task not found
    """
    user_id = get_jwt_identity()
    t = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not t:
        return jsonify({"message": "task not found"}), 404

    db.session.delete(t)
    db.session.commit()
    return "", 204
