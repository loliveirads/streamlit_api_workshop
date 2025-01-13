import streamlit as st
import requests
import pandas as pd

# URL da API
API_URL = "https://api-workshop-production.up.railway.app/produtos"

# Lista de categorias disponíveis
CATEGORIAS = ["Eletrônicos", "Informática", "Móveis", "Outros"]

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

def tab_inserir():
    st.subheader("Inserir Produto")
    with st.form(key="add_product_form"):
        titulo = st.text_input("Título do Produto", max_chars=100)
        descricao = st.text_area("Descrição do Produto", max_chars=500)
        preco = st.number_input("Preço do Produto", min_value=0.01, step=0.01)
        disponivel = st.checkbox("Disponível", value=True)
        categoria = st.selectbox("Categoria do Produto", CATEGORIAS)
        submit_button = st.form_submit_button(label="Adicionar Produto")

    if submit_button:
        if titulo and preco > 0:
            add_product(titulo, descricao, preco, disponivel, categoria)
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

def tab_alterar():
    st.subheader("Alterar Produto")
    products = get_products()
    if products:
        product_options = {f"{p['id']} - {p['titulo']}": p for p in products}
        selected_product = st.selectbox(
            "Pesquise ou selecione um Produto",
            options=list(product_options.keys()),
            help="Digite parte do título ou ID para buscar produtos"
        )
        product_data = product_options[selected_product]

        with st.form(key="update_product_form"):
            titulo = st.text_input("Título do Produto", value=product_data["titulo"])
            descricao = st.text_area("Descrição do Produto", value=product_data["descricao"])
            preco = st.number_input("Preço do Produto", min_value=0.01, step=0.01, value=product_data["preco"])
            disponivel = st.checkbox("Disponível", value=product_data["disponivel"])
            categoria_atual = product_data.get("categoria", "Outros")
            if categoria_atual not in CATEGORIAS:
                categoria_atual = "Outros"
            categoria = st.selectbox("Categoria do Produto", CATEGORIAS, index=CATEGORIAS.index(categoria_atual))
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
        df = pd.DataFrame(products)
        df['preco'] = df['preco'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df.rename(columns={
            'id': 'ID',
            'titulo': 'Título',
            'descricao': 'Descrição',
            'preco': 'Preço (R$)',
            'disponivel': 'Disponível',
            'categoria': 'Categoria'
        }, inplace=True)
        st.dataframe(df)
    else:
        st.warning("Nenhum produto encontrado.")

def delete_product(produto_id):
    try:
        response = requests.delete(f"{API_URL}/{produto_id}")
        if response.status_code == 200:
            st.success(f"Produto com ID {produto_id} deletado com sucesso!")
        elif response.status_code == 404:
            st.error("Produto não encontrado.")
        else:
            st.error(f"Erro ao deletar produto: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")

def tab_deletar():
    st.subheader("Deletar Produto")
    products = get_products()
    if products:
        product_options = {f"{p['id']} - {p['titulo']}": p for p in products}
        selected_product = st.selectbox("Pesquise ou selecione um Produto para deletar", options=list(product_options.keys()))
        product_data = product_options[selected_product]
        produto_id = product_data["id"]
        if st.button("Deletar Produto"):
            delete_product(produto_id)
    else:
        st.warning("Nenhum produto encontrado para deletar.")

def main():
    st.title("Gestão de Produtos")
    st.sidebar.title("Menu")
    menu = st.sidebar.radio(
        "Escolha uma opção:",
        ["Inserir Produtos", "Alterar Produtos", "Visualizar Produtos", "Deletar Produtos"]
    )
    if menu == "Inserir Produtos":
        tab_inserir()
    elif menu == "Alterar Produtos":
        tab_alterar()
    elif menu == "Visualizar Produtos":
        visualizar_produtos()
    elif menu == "Deletar Produtos":
        tab_deletar()

if __name__ == "__main__":
    main()
