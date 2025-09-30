''''
from flask import Flask, jsonify
from routes import register_routes

app = Flask(__name__)
register_routes(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
'''

from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.extensions import db, jwt
from backend.routes import register_routes
from backend import models



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Register blueprints (auth, tasks)
    register_routes(app)

    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    # Error handlers
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
        from backend import models
        db.create_all()  # Create tables in SQLite (for dev)
    app.run(host="127.0.0.1", port=5000, debug=True)
