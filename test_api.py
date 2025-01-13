import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import requests

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API
API_URL = "https://api-workshop-production.up.railway.app/produtos"

# Configuração do banco de dados PostgreSQL no Railway
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


def connect_to_db():
    """
    Função para conectar ao banco de dados PostgreSQL no Railway
    """
    try:
        engine = create_engine(
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        print("Conexão ao banco de dados bem-sucedida!")
        return engine
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None


def test_connection():
    """
    Testa a conexão ao banco e executa uma consulta simples.
    """
    engine = connect_to_db()
    if engine:
        try:
            with engine.connect() as conn:
                result = conn.execute("SELECT NOW();")
                for row in result:
                    print(f"Hora atual no servidor PostgreSQL: {row[0]}")
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")


def insert_product_api(titulo, preco, disponivel):
    """
    Função para enviar dados de um novo produto para a API remota.
    """
    payload = {
        "id": 0,  # O ID será gerado automaticamente pela API
        "titulo": titulo,  # Altere 'nome' para 'titulo'
        "descricao": None,  # Campo opcional
        "preco": preco,
        "disponivel": disponivel,
    }
    try:
        response = requests.post(f"{API_URL}/produtos", json=payload)
        if response.status_code == 200:
            print(f"Produto '{titulo}' inserido com sucesso!")
        else:
            print("Erro ao inserir produto:", response.json())
    except Exception as e:
        print("Erro ao conectar com a API:", e)



def list_products_api():
    """
    Lista os produtos cadastrados na API remota.
    """
    try:
        response = requests.get(f"{API_URL}/produtos")
        if response.status_code == 200:
            produtos = response.json()
            print("Produtos cadastrados:")
            for produto in produtos:
                print(
                    f"ID: {produto['id']}, Nome: {produto['nome']}, Preço: R${produto['preco']:.2f}, Disponível: {produto['disponivel']}"
                )
        else:
            print("Erro ao listar produtos:", response.json())
    except Exception as e:
        print("Erro ao conectar com a API:", e)


if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Testar conexão com o banco")
        print("2. Inserir novo produto via API")
        print("3. Listar produtos via API")
        print("4. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            test_connection()
        elif opcao == "2":
            titulo = input("Digite o título do produto: ")
            preco = float(input("Digite o preço do produto: "))
            disponivel_input = input("O produto está disponível? (s/n): ").strip().lower()
            disponivel = True if disponivel_input == "s" else False
            insert_product_api(titulo, preco, disponivel)
        elif opcao == "3":
            list_products_api()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
