# streamlit_api_workshop
# Streamlit API Workshop

## Descrição
Este projeto é uma aplicação frontend desenvolvida com **Streamlit** que consome a **API Workshop**. Ele permite a interação com a API para realizar operações de **CRUD** (Create, Read, Update, Delete) em produtos. O projeto é focado na facilidade de uso e na visualização dos dados, proporcionando uma interface amigável para gerenciar os produtos.

## Funcionalidades
- **Inserir Produtos**: Adicione novos produtos com título, descrição, preço, disponibilidade e categoria.
- **Alterar Produtos**: Atualize informações de produtos existentes.
- **Visualizar Produtos**: Consulte a lista de produtos com informações detalhadas.
- **Deletar Produtos**: Remova produtos do sistema.

## Links Importantes
- **Aplicação Streamlit**: [https://workshop-api.streamlit.app/](https://workshop-api.streamlit.app/)
- **Documentação da API**: [https://api-workshop-production.up.railway.app/docs](https://api-workshop-production.up.railway.app/docs)

## Requisitos
- **Python**: 3.12 ou superior
- **Poetry**: Gerenciador de dependências

## Configuração do Ambiente

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/loliveirads/streamlit_api_workshop.git
    ```

2. Clone o repositório:
   ```bash
   cd streamlit_api_wortkshop
    ```

3. Inicie o ambiente
   ```bash
   poetry init
    ```

4. Ative o ambiente
   ```bash
   poetry shell
    ```
5. Instale as dependencias
   ```bash
   poetry install
    ```
### Configuração

1. Crie um arquivo .env com as configurações necessárias:
   ```bash
    API_URL=https://api-workshop-production.up.railway.app/produtos
    ```

2. Certifique-se de que a API Workshop está rodando para consumir os endpoints.

### Executando a Aplicação

1. Inicie o servidor Streamlit:
   ```bash
    streamlit run main.py
    ```    
### Estrutura do Projeto
    ```bash
    streamlit_api_wortkshop/
    ├── .env                # Configuração de ambiente
    ├── main.py             # Código principal da aplicação Streamlit
    ├── pyproject.toml      # Configuração do Poetry
    ├── poetry.lock         # Dependências do projeto
    ├── README.md           # Documentação do projeto
    └── test_api.py         # Testes da aplicação
    ```    

### Contribuições

## Contato

Para dúvidas, sugestões ou feedbacks:

* **Luiz Fernando** - [luizfsoliveira.lm@gmail.com](mailto:luizfsoliveira.lm@gmail.com)