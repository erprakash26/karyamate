from backend.routes.auth import auth_bp
from backend.routes.tasks import tasks_bp

def register_routes(app):
    """Register all route blueprints with the Flask app."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
