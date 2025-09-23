from flask import Flask, jsonify
from routes import register_routes

app = Flask(__name__)
register_routes(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
