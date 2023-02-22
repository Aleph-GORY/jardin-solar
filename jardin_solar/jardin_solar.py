from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(
        {"mensaje": "Jardin Solar API"}
    )

@app.route("/linea/<id>", methods=['GET'])
def estatus_linea(id=None):
    return jsonify(
        {"estatus": "Linea " + id + ", prendida"}
    )