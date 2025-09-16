# 20252-progeficaz-projeto2-vicvaporubi

## Descrição do Projeto
Este projeto implementa uma API RESTful para uma empresa imobiliária usando o framework Flask. A API permite gerenciar uma base de dados de imóveis, seguindo os princípios de TDD (Test-Driven Development) e conectando-se a um banco de dados MySQL hospedado na plataforma Aiven.

## Requisitos e Tecnologias
- **Framework Web**: Flask
- **Banco de Dados**: MySQL (Aiven)
- **Bibliotecas Python**: As dependências do projeto estão listadas no arquivo `requirements.txt`. As principais são `Flask`, `mysql-connector-python` e `pytest`.

## Funcionalidades da API
A API foi projetada de acordo com o modelo de Maturidade de Richardson, atingindo o Nível 3 (HATEOAS). Isso significa que as respostas da API agora incluem links que permitem ao cliente descobrir e navegar pelos recursos e ações disponíveis, sem a necessidade de conhecimento prévio da estrutura de URLs.

### Rotas da API
A API agora oferece uma rota de entrada (root) para descoberta de endpoints, além das rotas para as operações CRUD:

| Método HTTP | Rota                          | Descrição                                 |
|-------------|-------------------------------|-------------------------------------------|
| `GET`       | `/`                           | Retorna uma página inicial com os comandos da API. |
| `GET`       | `/imoveis`                    | Lista todos os imóveis cadastrados. |
| `GET`       | `/imoveis/<int:id>`           | Detalha um imóvel específico pelo ID. |
| `GET`       | `/imoveis/tipo/<string:tipo>` | Filtra e lista imóveis por tipo. |
| `GET`       | `/imoveis/cidade/<string:cidade>`| Filtra e lista imóveis por cidade. |
| `POST`      | `/imoveis`                    | Cria um novo imóvel.         |
| `PUT`       | `/imoveis/<int:id>`           | Atualiza um imóvel existente. |
| `DELETE`    | `/imoveis/<int:id>`           | Remove um imóvel existente.  |

## Como Executar o Projeto

### Configuração do Ambiente
1.  **Variáveis de Ambiente**: Crie um arquivo `.env` na raiz do projeto para armazenar as credenciais do banco de dados MySQL. O arquivo `.gitignore` já está configurado para ignorá-lo.
    ```
    DB_HOST=seu_host_aiven.aivencloud.com
    DB_PORT=3306
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_NAME=seu_banco_de_dados
    ```
2.  **Instalar Dependências**: Instale as bibliotecas necessárias com o pip.
    ```bash
    pip install -r requirements.txt
    ```

### Inicialização do Banco de Dados
O projeto inclui um script para criar e popular o banco de dados. Use o seguinte comando para inicializar o banco de dados:
```bash
python main.py init_db
```

### Rodando o Servidor
Execute a aplicação em modo de desenvolvimento com o seguinte comando:
```bash
python main.py dev
```
O servidor estará disponível em http://0.0.0.0:5000

### Testes Automatizados
O projeto utiliza pytest para testes automatizados, seguindo os princípios de TDD. Para executar os testes, use os seguintes comandos:
- **Executar todos os testes:**
```bash 
python tests.py all
```
- **Executar testes de classes específicas:**
```bash 
python tests.py Database

python tests.py ImoveisAPI
```
- **Executar testes de rotas específicas:**
```bash
python tests.py ImoveisAPI get-all-imoveis

python tests.py ImoveisAPI get-imovel

python tests.py ImoveisAPI create-imovel

python tests.py ImoveisAPI update-imovel

python tests.py ImoveisAPI delete-imovel

python tests.py ImoveisAPI get-imoveis-by
```
### Deploy da API
A API está hospedada e acessível através do seguinte link: [54.227.62.155](http://54.227.62.155)

### Autores
- Maria Eduarda Oliveira Galdino
- Robson dos Santos França
