import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

def get_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT (*) FROM imoveis;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_imovel_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT (*) FROM imoveis WHERE id=?;", id)
    imovel = cursor.fetchone()
    cursor.close()
    conn.close()
    return imovel

def save_data(imovel):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
        (
            imovel["logradouro"],
            imovel["tipo_logradouro"],
            imovel["bairro"],
            imovel["cidade"],
            imovel["cep"],
            imovel["tipo"],
            imovel["valor"],
            imovel["data_aquisicao"]
        )
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True
