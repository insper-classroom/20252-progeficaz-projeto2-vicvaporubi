from flask import Flask, jsonify, request

import views

app = Flask(__name__)


@app.get("/imoveis")
def get_imoveis():
    return jsonify(views.get_imoveis()), 200


@app.get("/imoveis/<int:id>")
def get_imovel(id):
    return jsonify(views.get_imovel(id)), 200


@app.get("/imoveis/tipo/<string:tipo>")
def get_imoveis_by_tipo(tipo):
    return jsonify(views.get_imoveis_by_tipo(tipo)), 200


@app.get("/imoveis/cidade/<string:cidade>")
def get_imoveis_by_cidade(cidade):
    return jsonify(views.get_imoveis_by_cidade(cidade)), 200


@app.post("/imoveis")
def create_imovel():
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Dados inválidos"}), 400
    imovel = {
        "nome": request_data.get("nome"),
        "tipo": request_data.get("tipo"),
        "cidade": request_data.get("cidade"),
        "preco": request_data.get("preco"),
    }
    if not all([imovel["nome"], imovel["preco"], imovel["tipo"], imovel["cidade"]]):
        return jsonify(
            {"error": "Todos os campos são obrigatórios (nome e preco)"}
        ), 400
    return jsonify(views.create_imovel(imovel)), 201


@app.put("/imoveis")
def update_imovel():
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Dados inválidos"}), 400
    imovel = {
        "id": request_data.get("id"),
        "nome": request_data.get("nome"),
        "preco": request_data.get("preco"),
    }
    if not all([imovel["nome"], imovel["preco"]]):
        return jsonify(
            {"error": "Todos os campos são obrigatórios (nome e preco)"}
        ), 400
    return jsonify(views.update_imovel(imovel)), 200


@app.delete("/imoveis/<int:id>")
def delete_imovel(id):
    return jsonify(views.delete_imovel(id)), 200


if __name__ == "__main__":
    app.run(debug=True)
