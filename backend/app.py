from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger

from backend.config import Config
from backend.extensions import db, jwt
from backend.routes import register_routes
from backend import models


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # -------------------------------------------------
    # Swagger / Flasgger configuration
    # -------------------------------------------------
    app.config["SWAGGER"] = {
        "title": "KaryaMate API",
        "uiversion": 3,
        # This makes Swagger UI available at /docs
        "specs_route": "/docs/",
    }

    swagger = Swagger(app)

    # -------------------------------------------------
    # Init extensions
    # -------------------------------------------------
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Register blueprints (auth, tasks, …)
    register_routes(app)

    # -------------------------------------------------
    # Routes WITH Swagger docstrings
    # -------------------------------------------------
    @app.route("/health", methods=["GET"])
    def health():
        """
        Health Check
        ---
        tags:
          - System
        responses:
          200:
            description: API is alive and reachable
            examples:
              application/json: { "status": "ok" }
        """
        return jsonify({"status": "ok"})

    @app.route("/", methods=["GET"])
    def home():
        """
        API Root
        ---
        tags:
          - System
        responses:
          200:
            description: Simple welcome message for KaryaMate API
            examples:
              application/json: { "message": "KaryaMate API is running" }
        """
        return jsonify({"message": "KaryaMate API is running"}), 200

    # -------------------------------------------------
    # Error handlers
    # -------------------------------------------------
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"message": "server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        from backend import models  # ensures models are registered
        db.create_all()             # SQLite tables for local dev
    app.run(host="127.0.0.1", port=5000, debug=True)
