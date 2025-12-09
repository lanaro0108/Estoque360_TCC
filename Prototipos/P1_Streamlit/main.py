import streamlit as st
import os
from produtos import salvar_produto, salvar_estoque, atualizar_estoque, pegar_id
from fornecedores import registrar_compra, registrar_fornecedor
from clientes import registrar_venda, registrar_cliente
from database import conectar, criar_tabelas
import base64
from dotenv import load_dotenv
import sqlite3
from openai import OpenAI

load_dotenv()
criar_tabelas()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #0a74da;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1a659e;
    }
    .css-1d391kg {
        background-color: #1a1d24;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.subheader("🤖 Assistente Estoque360")

if "mostrar_chat" not in st.session_state:
    st.session_state.mostrar_chat = False

if st.sidebar.button("Clique para falar com o Assistente", key="icone_chat"):
    st.session_state.mostrar_chat = not st.session_state.mostrar_chat

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

if st.session_state.mostrar_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
        "role": "system",
        "content": """
Você é o Assistente Oficial do Estoque360.
Seu trabalho é ajudar o usuário a utilizar o sistema de forma clara, direta e profissional.

IMPORTANTE — NUNCA FAÇA:
- Não invente menus, botões, telas, campos que o Estoque360 NÃO possui.
- Não fale “Adicionar Produto”, “Código do produto”, “Imagem do produto”, “Verificar produto”.
- Não explique funcionalidades que não existam.
- Não diga que você é uma IA.
- Não gere texto longo, repetitivo ou poluído.

O QUE EXISTE NO ESTOQUE360:

CADASTRO DE PRODUTOS  
Campos reais: categoria, tipo do produto, gênero, marca, cor, tamanho, preço de custo, preço de venda, quantidade.

CADASTRO DE CLIENTES  
Campos: CPF, nome, CEP, número, complemento, telefone, email.

CADASTRO DE FORNECEDORES  
Campos: CNPJ, nome, CEP, número, complemento, telefone, email.

REGISTRO DE COMPRA  
Campos: CNPJ do fornecedor, ID produto, quantidade, valor unitário. Produz entrada no estoque.

REGISTRO DE VENDA  
Campos: CPF cliente, ID produto, quantidade, valor unitário, forma de pagamento. Produz saída no estoque.

ESTOQUE  
Exibe: ID, tipo do produto, marca, cor, tamanho, quantidade atual.

COMPORTAMENTO DO ASSISTENTE:
- Responda de forma curta, clara e profissional.
- Se o usuário fizer algo errado (campo faltando, formato errado), explique o que está errado e como corrigir.
- Só fale com base no que existe de verdade no Estoque360.
- Se for dúvida vaga, peça para o usuário esclarecer.
"""
            }
        ]

    pergunta = st.sidebar.text_input("Digite sua pergunta:", key="pergunta_chat")

    if pergunta:
        st.session_state.messages.append({"role": "user", "content": pergunta})

        resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
        )

        texto = resposta.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": texto})
        st.sidebar.markdown(f"**Bot:** {texto}")

def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_image_base64("src/prototipos/assets/estoque360_master (1).png")

st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px;">
        <img src="data:image/png;base64,{logo_base64}" width="70">
        <h1 style="margin: 0;">Controle de Estoque</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

def fetch_options(table, column):
    db = conectar()
    cursor = db.cursor()
    cursor.execute(f"SELECT {column} FROM {table}")
    data = [row[0] for row in cursor.fetchall()]
    db.close()
    return data

def fetch_tipos_by_categoria(categoria):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("""
        SELECT tp.nome FROM tipo_produto tp
        JOIN categoria c ON tp.id_categoria = c.id
        WHERE c.nome = ?
    """, (categoria,))
    data = [row[0] for row in cursor.fetchall()]
    db.close()
    return data

pagina = st.sidebar.selectbox("Navegar para:",
                              ["Cadastro de Produtos", "Compras de Fornecedores", "Vendas a Clientes", "Estoque"])

if pagina == "Cadastro de Produtos":
    st.markdown("Cadastro de Produtos")
    categorias = fetch_options("categoria", "nome")
    generos = ["masculino", "feminino", "unissex"]

    with st.container(border=True):
        categoria = st.radio("Categoria", categorias)
        tipos = fetch_tipos_by_categoria(categoria)
        tipo_produto = st.selectbox("Tipo do produto", tipos)
        genero = st.selectbox("Gênero", generos)
        marca = st.text_input("Marca", placeholder="Digite a marca do produto...")
        cor = st.text_input("Cor", placeholder="Digite a cor do produto...")

        tamanho = ""

        if categoria == "calçados":
            tamanho = st.radio("Tamanho", [str(t) for t in range(33, 47)], horizontal=True)

        elif categoria == "vestuário":
            tamanhos_letras = ["PP","P","M","G","GG","XG","XXG","XXXG"]
            tamanhos_numericos = [str(t) for t in range(34, 61, 2)]
            tamanhos_infantil = [str(t) for t in range(2, 18, 2)]
            categorias_numericos = ["calças","shorts","saia"]
            categorias_letras = ["camisas","camisetas","blusa moletom","jaqueta","blazer","regata"]

            if tipo_produto in categorias_numericos:
                tamanho = st.radio("Tamanho", tamanhos_numericos, horizontal=True)
            elif tipo_produto in categorias_letras:
                tamanho = st.radio("Tamanho", tamanhos_letras, horizontal=True)
            elif tipo_produto == "vestidos":
                tamanho = st.radio("Tamanho", tamanhos_infantil + tamanhos_letras, horizontal=True)

        precocusto = st.number_input("Preço de custo", min_value=0.0)
        precovenda = st.number_input("Preço de venda", min_value=0.0)
        quantidade = st.number_input("Quantidade", min_value=1, step=1)

        if st.button("Cadastrar Produto"):
            if not marca or not cor:
                st.warning("Marca e Cor são obrigatórios.")
            else:
                produto_id = salvar_produto(categoria, tipo_produto, genero, marca, cor, tamanho, precocusto, precovenda)
                salvar_estoque(produto_id, quantidade)
                st.success("Produto cadastrado!")

elif pagina == "Compras de Fornecedores":
    st.markdown("Registrar Compra de Fornecedor")
    tab1, tab2 = st.tabs(["Nova Compra", "Cadastrar Fornecedor"])

    with tab2:
        with st.container(border=True):
            cnpj = st.text_input("CNPJ", placeholder="00.000.000/0000-00")
            nome = st.text_input("Nome", placeholder="Digite o nome do fornecedor...")
            cep = st.text_input("CEP", placeholder="00000-000")
            numero = st.text_input("Número", placeholder="Digite o número...")
            comp = st.text_input("Complemento", placeholder="Digite o complemento...")
            tel = st.text_input("Telefone", placeholder="(00) 00000-0000")
            email = st.text_input("Email", placeholder="Digite o email...")

            if st.button("Salvar Fornecedor"):
                if cnpj and nome and cep:
                    registrar_fornecedor(cnpj, nome, cep, numero, comp, tel, email)
                    st.success("Fornecedor cadastrado!")
                else:
                    st.warning("Preencha os campos obrigatórios.")

    with tab1:
        with st.container(border=True):
            cnpj_fornecedor = st.text_input("CNPJ do fornecedor", placeholder="00.000.000/0000-00")

            if "produtos_compra" not in st.session_state:
                st.session_state.produtos_compra = []

            nome_prod = st.text_input("Nome do Produto (por tipo)", key="compra_nome_prod", placeholder="Digite o nome do produto...")
            qtd = st.number_input("Quantidade", min_value=1)
            valor = st.number_input("Valor Unitário", min_value=0.0)

            if st.button("Adicionar Item"):
                db = conectar()
                cursor = db.cursor()
                cursor.execute(
                    "SELECT p.id FROM produtos p JOIN tipo_produto tp ON p.id_tipo_produto = tp.id WHERE tp.nome LIKE ?",
                    (f"%{nome_prod}%",)
                )
                res = cursor.fetchone()
                db.close()

                if res:
                    st.session_state.produtos_compra.append(
                        {"id_produto": res[0], "quantidade": qtd, "valor_unit": valor, "nome": nome_prod}
                    )
                    st.success("Produto adicionado!")
                else:
                    st.warning("Produto não encontrado.")

            if st.session_state.produtos_compra:
                for item in st.session_state.produtos_compra:
                    st.write(f"{item['nome']} — {item['quantidade']} x R$ {item['valor_unit']}")

            if st.button("Finalizar Compra"):
                if not st.session_state.produtos_compra:
                    st.warning("Lista vazia.")
                else:
                    try:
                        id_compra = registrar_compra(cnpj_fornecedor, st.session_state.produtos_compra)
                        st.success(f"Compra registrada! ID: {id_compra}")
                        st.session_state.produtos_compra = []
                    except Exception as e:
                        st.error(f"Erro: {e}")

elif pagina == "Vendas a Clientes":
    st.markdown("Registrar Venda a Cliente")
    tab1, tab2 = st.tabs(["Nova Venda", "Cadastrar Cliente"])

    with tab2:
        with st.container(border=True):
            cpf = st.text_input("CPF", placeholder="000.000.000-00")
            nome = st.text_input("Nome", placeholder="Digite o nome do cliente...")
            cep = st.text_input("CEP", placeholder="00000-000")
            numero = st.text_input("Número", placeholder="Digite o número...")
            comp = st.text_input("Complemento", placeholder="Digite o complemento...")
            tel = st.text_input("Telefone", placeholder="(00) 00000-0000")
            email = st.text_input("Email", placeholder="Digite o email...")

            if st.button("Salvar Cliente"):
                if cpf and nome and cep:
                    registrar_cliente(cpf, nome, cep, numero, comp, tel, email)
                    st.success("Cliente cadastrado!")
                else:
                    st.warning("Preencha os campos obrigatórios.")

    with tab1:
        with st.container(border=True):
            cpf_cliente = st.text_input("CPF do Cliente", placeholder="000.000.000-00")

            db = conectar()
            cursor = db.cursor()
            cursor.execute("SELECT id, formapgto FROM forma_pgto")
            formas = {row[1]: row[0] for row in cursor.fetchall()}
            db.close()

            forma = st.selectbox("Forma de pagamento", list(formas.keys()))
            id_forma = formas[forma]

            if "produtos_venda" not in st.session_state:
                st.session_state.produtos_venda = []

            nome_prod = st.text_input("Nome do produto (por tipo)", key="venda_nome_prod", placeholder="Digite o nome do produto...")
            qtd = st.number_input("Quantidade", min_value=1)
            valor = st.number_input("Valor Unitário", min_value=0.0)

            if st.button("Adicionar Item à Venda"):
                db = conectar()
                cursor = db.cursor()
                cursor.execute(
                    "SELECT p.id FROM produtos p JOIN tipo_produto tp ON p.id_tipo_produto = tp.id WHERE tp.nome LIKE ?",
                    (f"%{nome_prod}%",)
                )
                res = cursor.fetchone()
                db.close()

                if res:
                    st.session_state.produtos_venda.append(
                        {"id_produto": res[0], "quantidade": qtd, "valor_unit": valor, "nome": nome_prod}
                    )
                    st.success("Produto adicionado!")
                else:
                    st.warning("Produto não encontrado.")

            if st.session_state.produtos_venda:
                for item in st.session_state.produtos_venda:
                    st.write(f"{item['nome']} — {item['quantidade']} x R$ {item['valor_unit']}")

            if st.button("Finalizar Venda"):
                if not st.session_state.produtos_venda:
                    st.warning("Lista vazia.")
                else:
                    try:
                        id_venda = registrar_venda(cpf_cliente, id_forma, st.session_state.produtos_venda)
                        st.success(f"Venda registrada! ID: {id_venda}")
                        st.session_state.produtos_venda = []
                    except Exception as e:
                        st.error(f"Erro: {e}")

elif pagina == "Estoque":
    st.markdown("Estoque Atual")

    db = conectar()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.id, tp.nome as tipo_produto, m.nomemarca as marca, 
               c.nomecor as cor, t.tamanho, e.quantidade
        FROM produtos p
        JOIN tipo_produto tp ON p.id_tipo_produto = tp.id
        JOIN marcas m ON p.id_marca = m.id
        JOIN cores c ON p.id_cor = c.id
        JOIN tamanho t ON p.id_tamanho = t.id
        JOIN estoque_atual e ON p.id = e.produto_id
    """)
    data = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    db.close()

    st.table(data)

