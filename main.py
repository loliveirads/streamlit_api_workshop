import streamlit as st
import requests

# URL da API
API_URL = "https://api-workshop-production.up.railway.app/produtos"

def add_product(titulo, descricao, preco, disponivel, categoria):
    payload = {
        "titulo": titulo,
        "descricao": descricao,
        "preco": preco,
        "disponivel": disponivel,
        "categoria": categoria
    }
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            st.success(f"Produto '{titulo}' adicionado com sucesso!")
        elif response.status_code == 400:
            st.error(response.json().get("detail", "Erro desconhecido"))
        else:
            st.error(f"Erro ao adicionar produto: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")

def get_products():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Erro ao obter produtos.")
            return []
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
        return []

def update_product(produto_id, titulo, descricao, preco, disponivel, categoria):
    payload = {
        "titulo": titulo,
        "descricao": descricao,
        "preco": preco,
        "disponivel": disponivel,
        "categoria": categoria
    }
    try:
        response = requests.put(f"{API_URL}/{produto_id}", json=payload)
        if response.status_code == 200:
            st.success(f"Produto '{titulo}' atualizado com sucesso!")
        elif response.status_code == 404:
            st.error("Produto não encontrado.")
        else:
            st.error(f"Erro ao atualizar produto: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")

# Funções para cada operação
def inserir_produto():
    st.subheader("Inserir Produto")
    with st.form(key="add_product_form"):
        titulo = st.text_input("Título do Produto", max_chars=100)
        descricao = st.text_area("Descrição do Produto", max_chars=500)
        preco = st.number_input("Preço do Produto", min_value=0.01, step=0.01)
        disponivel = st.checkbox("Disponível", value=True)
        categoria = st.text_input("Categoria do Produto")
        submit_button = st.form_submit_button(label="Adicionar Produto")

    if submit_button:
        if titulo and preco > 0:
            add_product(titulo, descricao, preco, disponivel, categoria)
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

def alterar_produto():
    st.subheader("Alterar Produto")
    products = get_products()
    if products:
        product_options = {f"{p['id']} - {p['titulo']}": p for p in products}
        selected_product = st.selectbox("Selecione um Produto", list(product_options.keys()))
        product_data = product_options[selected_product]

        with st.form(key="update_product_form"):
            titulo = st.text_input("Título do Produto", value=product_data["titulo"])
            descricao = st.text_area("Descrição do Produto", value=product_data["descricao"])
            preco = st.number_input("Preço do Produto", min_value=0.01, step=0.01, value=product_data["preco"])
            disponivel = st.checkbox("Disponível", value=product_data["disponivel"])
            categoria = st.text_input("Categoria do Produto", value=product_data.get("categoria", ""))
            submit_button = st.form_submit_button(label="Alterar Produto")

        if submit_button:
            if titulo and preco > 0:
                update_product(product_data["id"], titulo, descricao, preco, disponivel, categoria)
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")
    else:
        st.warning("Nenhum produto encontrado.")

def visualizar_produtos():
    st.subheader("Lista de Produtos")
    products = get_products()
    if products:
        df = st.dataframe(products)
    else:
        st.warning("Nenhum produto encontrado.")

# Main function
def main():
    st.title("Gestão de Produtos")

    # Criar menu lateral
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Escolha uma opção:", ["Inserir Produtos", "Alterar Produtos", "Visualizar Produtos"])

    if menu == "Inserir Produtos":
        inserir_produto()
    elif menu == "Alterar Produtos":
        alterar_produto()
    elif menu == "Visualizar Produtos":
        visualizar_produtos()

if __name__ == "__main__":
    main()
