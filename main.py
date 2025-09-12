from flask import Flask, jsonify, request

import views

app = Flask(__name__)


@app.get("/imoveis")
def get_imoveis():
    return jsonify(views.get_imoveis()), 200

@app.get("/imoveis/<int:id>")
def get_imovel(id):
    result = views.get_imovel(id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200


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
    required_fields = [
        "logradouro", "tipo_logradouro", "bairro", "cidade", "cep",
        "tipo", "valor", "data_aquisicao"
    ]
    if not all(field in request_data and request_data[field] for field in required_fields):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    return jsonify(views.create_imovel(request_data)), 201

@app.put("/imoveis")
def update_imovel():
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Dados inválidos"}), 400
    required_fields = [
        "id", "logradouro", "tipo_logradouro", "bairro", "cidade", "cep",
        "tipo", "valor", "data_aquisicao"
    ]
    if not all(field in request_data and request_data[field] for field in required_fields):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    msg, status = views.update_imovel(request_data)
    return jsonify({"message": msg}), status


@app.delete("/imoveis/<int:id>")
def delete_imovel(id):
    msg, status = views.delete_imovel(id)
    return jsonify({"message": msg}), status


if __name__ == "__main__":
    app.run(debug=True)

