import pytest
from main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("utils.get_connection")
def test_get_all_imoveis(mock_get_connection, client):
    mock_value = [
        {
            "logradouro": "Rua Teste1",
            "tipo_logradouro": "Rua",
            "bairro": "Centro",
            "cidade": "Cabideira",
            "cep": "12345-678",
            "tipo": "apartamento",
            "valor": 456.78,
            "data_aquisicao": "2024-01-01"
        },
        {
            "logradouro": "Rua Teste2",
            "tipo_logradouro": "Rua",
            "bairro": "Centro",
            "cidade": "Testelandia",
            "cep": "12345-678",
            "tipo": "apartamento",
            "valor": 123456.78,
            "data_aquisicao": "2024-01-01"
        }
    ]

    # Criando uma conexão Mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Chama o mock cursor quando executa conn.cursor
    mock_conn.cursor.return_value = mock_cursor

    # Simula o retorno do banco de dados
    mock_cursor.fetchall.return_value = mock_value

    # Substituir a conn
    mock_get_connection.return_value = mock_conn

    resp = client.get("/imoveis")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)
    assert resp.get_json() == mock_value

@patch("utils.get_connection")
def test_create_imovel(mock_get_connection, client):
    novo_imovel = {
        "logradouro": "Rua Teste",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "Testelandia",
        "cep": "12345-678",
        "tipo": "apartamento",
        "valor": 123456.78,
        "data_aquisicao": "2024-01-01"
    }

    # Criando uma conexão Mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Chama o mock cursor quando executa conn.cursor
    mock_conn.cursor.return_value = mock_cursor

    # Substituir a conn
    mock_get_connection.return_value = mock_conn
    
    expected_sql = "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (?, ?, ?, ?, ?, ?, ?, ?);".strip()
    data = (
    novo_imovel['logradouro'],
    novo_imovel['tipo_logradouro'],
    novo_imovel['bairro'],
    novo_imovel['cidade'],
    novo_imovel['cep'],
    novo_imovel['tipo'],
    novo_imovel['valor'],
    novo_imovel['data_aquisicao']
)


    # Cria imóvel
    resp = client.post("/imoveis", json=novo_imovel)
    assert resp.status_code == 201
    mock_cursor.execute.assert_called_once_with(expected_sql, data)

    
@patch("views.get_connection")
def test_update_imovel(mock_get_connection, client):
    # Cria imóvel para atualizar
    novo_imovel = {
        "logradouro": "Rua Atualiza",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "Atualizaville",
        "cep": "99999-999",
        "tipo": "casa",
        "valor": 555.55,
        "data_aquisicao": "2024-02-02",
        "id": 2
    }
    # Mock da conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    resp = client.put("/imoveis", json=novo_imovel)
    assert resp.status_code == 200

    data = (
    novo_imovel['logradouro'],
    novo_imovel['tipo_logradouro'],
    novo_imovel['bairro'],
    novo_imovel['cidade'],
    novo_imovel['cep'],
    novo_imovel['tipo'],
    novo_imovel['valor'],
    novo_imovel['data_aquisicao'],
    novo_imovel["id"]
    )
    expected_sql = "UPDATE imoveis SET logradouro=?,  tipo_logradouro=?, bairro=?, cidade=?, cep=?, tipo=?, valor=?, data_aquisicao=? WHERE id=?;".strip()
    mock_cursor.execute.assert_called_once_with(expected_sql, data)



@patch("views.get_connection")
def test_delete_imovel(mock_get_connection, client):
    # Cria imóvel para deletar
    imovel = {
        "logradouro": "Rua Deletar",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "Deletelandia",
        "cep": "00000-000",
        "tipo": "terreno",
        "valor": 1.23,
        "data_aquisicao": "2024-03-03",
        "id": 3
    }

    # Criando uma conexão Mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Chama o mock cursor quando executa conn.cursor
    mock_conn.cursor.return_value = mock_cursor

    # Substituir a conn
    mock_get_connection.return_value = mock_conn

    # Deleta o imóvel
    resp = client.delete(f"/imoveis/{imovel['id']}")
    assert resp.status_code == 200
    assert "Imóvel deletado com sucesso" in resp.get_json().get("message", "")
    expected_sql = "DELETE FROM imoveis WHERE id=?;".strip()
    mock_cursor.execute.assert_called_once_with(expected_sql, (imovel["id"]))

@patch("views.get_connection")
def test_get_imoveis_by_tipo(mock_get_connection, client):
    mock_value = [
        {
            "logradouro": "Rua Teste1",
            "tipo_logradouro": "Rua",
            "bairro": "Centro",
            "cidade": "Cabideira",
            "cep": "12345-678",
            "tipo": "apartamento",
            "valor": 456.78,
            "data_aquisicao": "2024-01-01"
        },
        {
            "logradouro": "Rua Teste2",
            "tipo_logradouro": "Rua",
            "bairro": "Centro",
            "cidade": "Testelandia",
            "cep": "12345-678",
            "tipo": "apartamento",
            "valor": 123456.78,
            "data_aquisicao": "2024-01-01"
        }
    ]

    # Criando uma conexão Mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Chama o mock cursor quando executa conn.cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = mock_value


    # Substituir a conn
    mock_get_connection.return_value = mock_conn

    resp = client.get("/imoveis/tipo/apartamento")
    assert resp.status_code == 200
    assert mock_value == resp.get_json()
    expected_sql = "SELECT (*) FROM imoveis WHERE tipo=?;".strip()
    mock_cursor.execute.assert_called_once_with(expected_sql, "apartamento")

@patch("views.get_connection")
def test_get_imoveis_by_cidade(mock_get_connection, client):
    mock_value = [
        {
            "logradouro": "Rua Teste1",
            "tipo_logradouro": "Rua",
            "bairro": "Centro",
            "cidade": "Cabideira",
            "cep": "12345-678",
            "tipo": "apartamento",
            "valor": 456.78,
            "data_aquisicao": "2024-01-01"
        },
        {
            "logradouro": "Rua Teste2",
            "tipo_logradouro": "Rua",
            "bairro": "Centro",
            "cidade": "Cabideira",
            "cep": "12345-678",
            "tipo": "apartamento",
            "valor": 123456.78,
            "data_aquisicao": "2024-01-01"
        }
    ]

    # Criando uma conexão Mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Chama o mock cursor quando executa conn.cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = mock_value


    # Substituir a conn
    mock_get_connection.return_value = mock_conn

    resp = client.get("/imoveis/cidade/Cabideira")
    assert resp.status_code == 200
    assert mock_value == resp.get_json()
    expected_sql = "SELECT (*) FROM imoveis WHERE cidade=?;".strip()
    mock_cursor.execute.assert_called_once_with(expected_sql, "Cabideira")
