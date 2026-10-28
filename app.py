
from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")
    


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "projeto": "Seguranca Digital nas Comunidades"
    })


if __name__ == "__main__":
    app.run(debug=True)
