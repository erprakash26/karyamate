from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import Task
from backend.utils import sanitize_string, parse_bool, parse_priority, parse_datetime



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
    user_id = int(get_jwt_identity())
    # Optional filters
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
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    title = sanitize_string(data.get("title"))
    description = sanitize_string(data.get("description"))
    completed = parse_bool(data.get("completed"))
    priority = parse_priority(data.get("priority"))
    due_date = parse_datetime(data.get("due_date"))

    # Validation
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
    user_id = get_jwt_identity()
    t = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not t:
        return jsonify({"message": "task not found"}), 404
    return jsonify(task_to_dict(t)), 200

@tasks_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id):
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
    user_id = get_jwt_identity()
    t = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not t:
        return jsonify({"message": "task not found"}), 404
    db.session.delete(t)
    db.session.commit()
    return "", 204
