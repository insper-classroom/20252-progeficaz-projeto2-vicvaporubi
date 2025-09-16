from sys import argv
from unittest.mock import MagicMock, patch

import dotenv
import pytest

from main import app
from utils import get_connection


@pytest.fixture
def client():
    # Load env variables from .env file for testing
    dotenv.load_dotenv()

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestImoveisAPI:
    def setup_method(self):
        # Setting a common mock value for multiple tests
        self.mock_value = [
            {
                "logradouro": "Rua Teste1",
                "tipo_logradouro": "Rua",
                "bairro": "Centro",
                "cidade": "Cabideira",
                "cep": "12345-678",
                "tipo": "apartamento",
                "valor": 456.78,
                "data_aquisicao": "2024-01-01",
            },
            {
                "logradouro": "Rua Teste2",
                "tipo_logradouro": "Rua",
                "bairro": "Centro",
                "cidade": "Testelandia",
                "cep": "12345-678",
                "tipo": "apartamento",
                "valor": 123456.78,
                "data_aquisicao": "2024-01-01",
            },
            {
                "logradouro": "Avenida Teste3",
                "tipo_logradouro": "Avenida",
                "bairro": "Bairro Teste",
                "cidade": "Cabideira",
                "cep": "87654-321",
                "tipo": "casa",
                "valor": 789.01,
                "data_aquisicao": "2024-01-02",
            },
            {
                "logradouro": "Avenida Teste4",
                "tipo_logradouro": "Avenida",
                "bairro": "Bairro Teste",
                "cidade": "Testelandia",
                "cep": "87654-321",
                "tipo": "casa",
                "valor": 987654.32,
                "data_aquisicao": "2024-01-02",
            },
            {
                "logradouro": "Travessa Teste5",
                "tipo_logradouro": "Travessa",
                "bairro": "Bairro Teste",
                "cidade": "Cabideira",
                "cep": "11223-445",
                "tipo": "terreno",
                "valor": 321.65,
            },
        ]

        self.mock_imovel = {
            "id": 1,
            "logradouro": "Rua Teste1",
            "tipo_logradouro": "Rua",
            "bairro": "Centro",
            "cidade": "Cabideira",
            "cep": "12345-678",
            "tipo": "apartamento",
            "valor": 456.78,
            "data_aquisicao": "2024-01-01",
        }

        # Setting mocks
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = self.mock_value

        # Setup code before each test method
        patcher = patch("views.get_connection")
        self.mock_get_connection = patcher.start()
        self.mock_get_connection.return_value = self.mock_conn
        self.addCleanup = patcher.stop

    def teardown_method(self):
        # Teardown code after each test method
        self.mock_conn.close.assert_called_once()
        self.mock_cursor.close.assert_called()
        self.addCleanup()

    # Tests get all imoveis
    def test_get_all_imoveis(self, client):
        resp = client.get("/imoveis")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)
        assert resp.get_json() == self.mock_value

    def test_get_all_imoveis_empty(self, client):
        # Simulate no imoveis in database
        self.mock_cursor.fetchall.return_value = []

        resp = client.get("/imoveis")

        assert resp.status_code == 404
        assert resp.get_json() == {"error": "Nenhum imóvel encontrado"}

    # Test get imovel by id
    def test_create_imovel(self, client):
        novo_imovel = self.mock_imovel.copy()

        expected_sql = "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);".strip()
        data = (
            novo_imovel["logradouro"],
            novo_imovel["tipo_logradouro"],
            novo_imovel["bairro"],
            novo_imovel["cidade"],
            novo_imovel["cep"],
            novo_imovel["tipo"],
            novo_imovel["valor"],
            novo_imovel["data_aquisicao"],
        )

        # Create the imovel
        resp = client.post("/imoveis", json=novo_imovel)
        assert resp.status_code == 201
        assert resp.get_json() == {"message": "Imóvel criado com sucesso"}
        self.mock_cursor.execute.assert_called_once_with(expected_sql, data)

    def test_create_imovel_invalid_data(self, client):
        # Try to creqate imovel with invalid data
        resp = client.post("/imoveis", json={"logradouro": "Rua Incompleta"})
        assert resp.status_code == 415
        assert resp.get_json() == {"error": "Todos os campos são obrigatórios"}

    # Test Update imovel by id
    def test_update_imovel(self, client):
        # Get existing imovel and modify some fields
        imovel = self.mock_imovel.copy()

        resp = client.put(f"/imoveis/{imovel['id']}", json=imovel)
        assert resp.status_code == 200

        data = (
            imovel["logradouro"],
            imovel["tipo_logradouro"],
            imovel["bairro"],
            imovel["cidade"],
            imovel["cep"],
            imovel["tipo"],
            imovel["valor"],
            imovel["data_aquisicao"],
        )
        expected_sql = "UPDATE imoveis SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s, cep=%s, tipo=%s, valor=%s, data_aquisicao=%s WHERE id=%s;".strip()
        self.mock_cursor.execute.assert_called_once_with(expected_sql, data)

    def test_update_imovel_invalid_data(self, client):
        # Try to update imovel with invalid data
        resp = client.put("/imoveis", json={"logradouro": "Rua Incompleta"})
        assert resp.status_code == 415
        assert resp.get_json() == {"error": "Todos os campos são obrigatórios"}

    def test_update_imovel_not_found(self, client):
        # Simulate imovel not found during update
        self.mock_cursor.rowcount = 0
        imovel_not_found = self.mock_imovel.copy()
        imovel_not_found["id"] = 999  # Non-existent ID

        resp = client.put("/imoveis", json=imovel_not_found)
        assert resp.status_code == 404
        assert resp.get_json() == {
            "message": f"Imóvel com id {imovel_not_found['id']} não encontrado"
        }

    @pytest.mark.parametrize("invalid_id", [-1, 0, 3.5, "abc"])
    def test_update_imovel_invalid_id(self, invalid_id, client):
        # Try to update imovel with invalid id (non-integer)
        resp = client.put(f"/imoveis/{invalid_id}", json={"logradouro": "Rua Teste"})
        assert resp.status_code == 415
        assert resp.get_json() == {
            "error": "ID inválido. Deve ser um inteiro positivo."
        }

    # Test Delete imovel by id
    def test_delete_imovel(self, client):
        # Cria imóvel para deletar
        imovel = self.mock_imovel.copy()

        # Deleta o imóvel
        resp = client.delete(f"/imoveis/{imovel['id']}")
        assert resp.status_code == 200
        assert f"Imóvel deletado com id {imovel['id']} sucesso" in resp.get_json().get(
            "message", ""
        )
        expected_sql = "DELETE FROM imoveis WHERE id=%s;".strip()
        self.mock_cursor.execute.assert_called_once_with(expected_sql, (imovel["id"]))

    def test_delete_imovel_not_found(self, client):
        # Simulate imovel not found during delete
        self.mock_cursor.rowcount = 0
        non_existent_id = 999  # Non-existent ID

        resp = client.delete(f"/imoveis/{non_existent_id}")
        assert resp.status_code == 404
        assert resp.get_json() == {
            "message": f"Imóvel com id {non_existent_id} não encontrado"
        }

    @pytest.mark.parametrize("invalid_id", [-1, 0, 3.5, "abc"])
    def test_delete_imovel_invalid_id(self, invalid_id, client):
        # Try to delete imovel with invalid id (non-integer)
        resp = client.delete(f"/imoveis/{invalid_id}")
        assert resp.status_code == 415
        assert resp.get_json() == {
            "error": "ID inválido. Deve ser um inteiro positivo."
        }

    def test_get_imoveis_by_tipo(self, client):
        resp = client.get("/imoveis/tipo/apartamento")
        assert resp.status_code == 200
        assert resp.get_json() == self.mock_value
        expected_sql = "SELECT * FROM imoveis WHERE tipo=%s;".strip()
        self.mock_cursor.execute.assert_called_once_with(expected_sql, "apartamento")

    def test_get_imoveis_by_tipo_no_content(self, client):
        # Simulate no imoveis of given type in database
        self.mock_cursor.fetchall.return_value = []

        tipo = "apartamento"
        resp = client.get(f"/imoveis/tipo/{tipo}")
        assert resp.status_code == 404
        assert resp.get_json() == {
            "error": "Nenhum imóvel encontrado para o tipo apartamento especificado"
        }

    def test_get_imoveis_by_cidade(self, client):
        resp = client.get("/imoveis/cidade/Cabideira")
        assert resp.status_code == 200
        assert resp.get_json() == self.mock_value
        expected_sql = "SELECT * FROM imoveis WHERE cidade=%s;".strip()
        self.mock_cursor.execute.assert_called_once_with(expected_sql, "Cabideira")

    def test_get_imoveis_by_cidade_no_content(self, client):
        # Simulate no imoveis of given city in database
        self.mock_cursor.fetchall.return_value = []

        cidade = "Cabideira"
        resp = client.get(f"/imoveis/cidade/{cidade}")
        assert resp.status_code == 404
        assert resp.get_json() == {
            "error": f"Nenhum imóvel encontrado para a cidade {cidade} especificada"
        }


class TestDatabase:
    def setup_method(self):
        # Load env variables from .env file for testing
        dotenv.load_dotenv()

    def test_data_base_connection(self):
        conn = get_connection()
        assert conn.open
        conn.close()

    def test_cursor(self):
        conn = get_connection()
        cursor = conn.cursor()
        assert cursor is not None
        cursor.close()
        conn.close()

    def test_execute_query(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        assert result is not None
        cursor.close()
        conn.close()

    def test_close_connection(self):
        conn = get_connection()
        conn.close()
        assert not conn.open


if __name__ == "__main__":
    if argv and len(argv) > 1:
        if argv[1] == "all":
            pytest.main(["-v", __file__])
        elif argv[1] == "Database":
            pytest.main(["-v", __file__, "-k", "Database"])

        elif argv[1] == "ImoveisAPI":
            if len(argv) > 2:
                if argv[2] == "get-all-imoveis":
                    # Run all test starting with 'get_all_imoveis'
                    pytest.main(["-v", __file__, "-k", "get_all_imoveis"])
                elif argv[2] == "get-imoveis-by":
                    # Run all test starting with 'get_imoveis'
                    pytest.main(["-v", __file__, "-k", "get_imoveis_by"])
                elif argv[2] == "create-imovel":
                    # Run all test starting with 'create_imovel'
                    pytest.main(["-v", __file__, "-k", "create_imovel"])
                elif argv[2] == "update-imovel":
                    # Run all test starting with 'update_imovel'
                    pytest.main(["-v", __file__, "-k", "update_imovel"])
                elif argv[2] == "delete-imovel":
                    # Run all test starting with 'delete_imovel'
                    pytest.main(["-v", __file__, "-k", "delete_imovel"])
                else:
                    print(
                        "Invalid argument for ImoveisAPI. Use 'get-all-imoveis', 'get-imoveis', 'create-imovel', 'update-imovel', or 'delete-imovel'"
                    )
            else:
                pytest.main(["-v", __file__, "-k", "ImoveisAPI"])
        else:
            print("Invalid argument. Use 'all', 'Database', or 'ImoveisAPI'")
    else:
        print("Please provide an argument: 'all', 'Database', or 'ImoveisAPI'")
