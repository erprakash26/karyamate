from flask import jsonify

def register_routes(app):
    @app.route("/api/hello", methods=["GET"])
    def hello():
        return jsonify({"message": "Hello from KaryaMate backend!"})
