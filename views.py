from utils import get_data, get_imovel_by_id, save_data, get_connection

def get_imoveis():
    return get_data()

def get_imovel(id):
    imovel = get_imovel_by_id(id)
    if imovel:
        return imovel
    return {"error": "Imóvel não encontrado"}, 404

def create_imovel(imovel):
    save_data(imovel)
    return "Imóvel criado com sucesso", 201

def update_imovel(imovel):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE imoveis SET logradouro=?, tipo_logradouro=?, bairro=?, cidade=?, cep=?, tipo=?, valor=?, data_aquisicao=? WHERE id=?;",
        (
            imovel["logradouro"],
            imovel["tipo_logradouro"],
            imovel["bairro"],
            imovel["cidade"],
            imovel["cep"],
            imovel["tipo"],
            imovel["valor"],
            imovel["data_aquisicao"],
            imovel["id"]
        )
    )
    conn.commit()
    updated = cursor.rowcount
    cursor.close()
    conn.close()
    if updated:
        return "Imóvel atualizado com sucesso", 200
    return {"error": "Imóvel não encontrado"}, 404

def delete_imovel(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id=?;", id)
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    if deleted:
        return "Imóvel deletado com sucesso", 200
    return {"error": "Imóvel não encontrado"}, 404

def get_imoveis_by_tipo(tipo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT (*) FROM imoveis WHERE tipo=?;", tipo)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_imoveis_by_cidade(cidade):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT (*) FROM imoveis WHERE cidade=?;", cidade)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data