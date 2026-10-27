
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def inicio():
    return """
    <h1>Segurança Digital nas Comunidades</h1>
    <p>Servidor funcionando!</p>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "projeto": "Segurança Digital nas Comunidades"
    })


if __name__ == "__main__":
    app.run(debug=True)
