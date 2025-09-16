from utils import get_connection


def get_all_imoveis():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if data:
        return data, 200
    else:
        return {"error": "Nenhum imóvel encontrado"}, 404


def get_imovel(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id=%s;", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if data:
        return data
    return {"error": f"Imóvel com id: {id} não encontrado"}, 404


def create_imovel(imovel):
    if not all(
        key in imovel
        for key in (
            "logradouro",
            "tipo_logradouro",
            "bairro",
            "cidade",
            "cep",
            "tipo",
            "valor",
            "data_aquisicao",
        )
    ):
        return {"error": "Todos os campos são obrigatórios"}, 415

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
        (
            imovel["logradouro"],
            imovel["tipo_logradouro"],
            imovel["bairro"],
            imovel["cidade"],
            imovel["cep"],
            imovel["tipo"],
            imovel["valor"],
            imovel["data_aquisicao"],
        ),
    )
    conn.commit()
    con = cursor.lastrowid
    cursor.close()
    conn.close()
    if not con:
        return {"error": "Erro ao criar o imóvel"}, 500
    return {"message": "Imóvel criado com sucesso"}, 201


def update_imovel(imovel, id):
    if not all(
        key in imovel
        for key in (
            "logradouro",
            "tipo_logradouro",
            "bairro",
            "cidade",
            "cep",
            "tipo",
            "valor",
            "data_aquisicao",
        )
    ):
        return {"error": "Todos os campos são obrigatórios"}, 415

    id = int(id) if int(id) > 0 else id
    if id is str or id < 0 or id is None:
        return {"error": "ID inválido"}, 415

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE imoveis SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s, cep=%s, tipo=%s, valor=%s, data_aquisicao=%s WHERE id=%s;",
        (
            imovel["logradouro"],
            imovel["tipo_logradouro"],
            imovel["bairro"],
            imovel["cidade"],
            imovel["cep"],
            imovel["tipo"],
            imovel["valor"],
            imovel["data_aquisicao"],
            id,
        ),
    )
    conn.commit()
    updated = cursor.rowcount
    cursor.close()
    conn.close()
    if updated:
        return {"message": "Imóvel atualizado com sucesso"}, 200
    return {"error": f"Imóvel com id {id} não encontrado"}, 404


def delete_imovel(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id=%s;", id)
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    if deleted:
        return {"message": "Imóvel deletado com sucesso"}, 200
    return {"error": f"Imóvel com id {id} não encontrado"}, 404


def get_imoveis_by_tipo(tipo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE tipo=%s;", tipo)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if not data:
        return {
            "error": f"Nenhum imóvel encontrado com o tipo {tipo} especificado"
        }, 404
    return data, 200


def get_imoveis_by_cidade(cidade):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade=%s;", cidade)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if not data:
        return {
            "error": f"Nenhum imóvel encontrado para a cidade {cidade} especificada"
        }, 404
    return data, 200
