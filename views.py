from utils import get_data, save_data


def get_imoveis():
    data = get_data()
    return data


def get_imovel(id):
    data = get_data()
    for imovel in data:
        if imovel["id"] == id:
            return imovel
    return {"error": "Imóvel não encontrado"}, 404


def create_imovel(imovel):
    data = get_data()
    new_id = max([item["id"] for item in data], default=0) + 1
    imovel["id"] = new_id
    data.append(imovel)
    save_data(data)
    return "Imóvel criado com sucesso", 201


def update_imovel(imovel):
    data = get_data()
    for index, item in enumerate(data):
        if item["id"] == imovel["id"]:
            data[index] = imovel
            save_data(data)
            return "Imóvel atualizado com sucesso", 200
    return {"error": "Imóvel não encontrado"}, 404


def delete_imovel(id):
    data = get_data()
    for index, item in enumerate(data):
        if item["id"] == id:
            del data[index]
            save_data(data)
            return "Imóvel deletado com sucesso", 200
    return {"error": "Imóvel não encontrado"}, 404


def get_imoveis_by_tipo(tipo):
    data = get_data()
    filtered_imoveis = [imovel for imovel in data if imovel["tipo"] == tipo]
    return filtered_imoveis


def get_imoveis_by_cidade(cidade):
    data = get_data()
    filtered_imoveis = [imovel for imovel in data if imovel["cidade"] == cidade]
    return filtered_imoveis
