import sys

from dotenv import load_dotenv
from flask import Flask, jsonify, request

import views
from utils import initialize_database

app = Flask(__name__)
# Loading environment variables from .env file if present
load_dotenv()


@app.route("/")
def home():
    return "<h1>API de Imóveis</h1><p>Bem-vindo à API de Imóveis!</p><h4>Commandos:</h4><p>/imoveis - GET: Lista todos os imóveis<br>/imoveis/&lt;id&gt; - GET: Detalha um imóvel pelo ID<br>/imoveis/tipo/&lt;tipo&gt; - GET: Filtra imóveis por tipo<br>/imoveis/cidade/&lt;cidade&gt; - GET: Filtra imóveis por cidade<br>/imoveis - POST: Cria um novo imóvel<br>/imoveis - PUT: Atualiza um imóvel existente<br>/imoveis/&lt;id&gt; - DELETE: Remove um imóvel pelo ID</p>"


@app.get("/imoveis")
def get_all_imoveis():
    json, status = views.get_all_imoveis()
    return jsonify(json), status


@app.get("/imoveis/<int:id>")
def get_imovel(id):
    json, status = views.get_imovel(id)
    return jsonify(json), status


@app.get("/imoveis/tipo/<string:tipo>")
def get_imoveis_by_tipo(tipo):
    json, status = views.get_imoveis_by_tipo(tipo)
    return jsonify(json), status


@app.get("/imoveis/cidade/<string:cidade>")
def get_imoveis_by_cidade(cidade):
    json, status = views.get_imoveis_by_cidade(cidade)
    return jsonify(json), status


@app.post("/imoveis")
def create_imovel():
    json, status = views.create_imovel(request.get_json())
    return jsonify(json), status


@app.put("/imoveis/<int:id>")
def update_imovel(id):
    json, status = views.update_imovel(request.get_json(), id)
    return jsonify(json), status


@app.delete("/imoveis/<int:id>")
def delete_imovel(id):
    json, status = views.delete_imovel(id)
    return jsonify(json), status


if __name__ == "__main__":
    # Loading environment variables from .env file if present
    load_dotenv()
    # Command line arguments handling
    command = ""
    if len(sys.argv) > 1:
        command = sys.argv[1]
    elif len(sys.argv) == 1:
        command = "dev"
    elif len(sys.argv) > 2:
        print("Uso: python main.py [init_db|dev]")
        sys.exit(1)

    if command == "init_db":
        initialize_database()
        sys.exit(0)

    # Run the app
    elif command == "dev":
        app.run(debug=True)
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        print("Uso: python main.py [init_db|dev]")
