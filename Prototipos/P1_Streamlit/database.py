import sqlite3

def conectar():
    return sqlite3.connect("estoque360.db")

def criar_tabelas():
    db = conectar()
    cursor = db.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Tabelas Básicas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS generos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genero ENUM NOT NULL CHECK(genero IN ('masculino', 'feminino', 'unissex'))
    )
    """)
    
    cursor.execute("INSERT OR IGNORE INTO generos (genero) VALUES ('Masculino')")
    cursor.execute("INSERT OR IGNORE INTO generos (genero) VALUES ('Feminino')")
    cursor.execute("INSERT OR IGNORE INTO generos (genero) VALUES ('Unissex')")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marcas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomemarca TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomecor TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)
    
    # Insert initial categories if not exist
    cursor.execute("INSERT OR IGNORE INTO categoria (nome) VALUES ('calçados'), ('vestuário')")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipo_produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        id_categoria INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id)
    )
    """)
    
    # Insert initial types (lowercase for consistency with app)
    initial_types = [
        ('tênis', 1),
        ('chuteira', 1),
        ('sapatênis', 1),
        ('sandália', 1),
        ('chinelo', 1),
        ('bota', 1),
        ('sapato social', 1),
        ('crocs', 1),

        ('calças', 2),
        ('camisas', 2),
        ('camisetas', 2),
        ('blusa moletom', 2),
        ('vestidos', 2),
        ('shorts', 2),
        ('saia', 2),
        ('jaqueta', 2),
        ('blazer', 2),
        ('regata', 2),
    ]

    for nome, cat_id in initial_types:
        cursor.execute("INSERT OR IGNORE INTO tipo_produto (nome, id_categoria) VALUES (?, ?)", (nome, cat_id))

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tamanho (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tamanho TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK(tipo IN ('calcado', 'letra', 'numerico', 'infantil'))
    )
    """)

    # Insert initial sizes
    sizes_calcado = [str(i) for i in range(33, 47)]
    for s in sizes_calcado:
        cursor.execute("INSERT OR IGNORE INTO tamanho (tamanho, tipo) VALUES (?, 'calcado')", (s,))
        
    sizes_letra = ['PP','P','M','G','GG','XG','XXG','XXXG']
    for s in sizes_letra:
        cursor.execute("INSERT OR IGNORE INTO tamanho (tamanho, tipo) VALUES (?, 'letra')", (s,))
        
    sizes_numerico = [str(i) for i in range(34, 61, 2)]
    for s in sizes_numerico:
        cursor.execute("INSERT OR IGNORE INTO tamanho (tamanho, tipo) VALUES (?, 'numerico')", (s,))
        
    sizes_infantil = [str(i) for i in range(2, 17, 2)]
    for s in sizes_infantil:
        cursor.execute("INSERT OR IGNORE INTO tamanho (tamanho, tipo) VALUES (?, 'infantil')", (s,))

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipo_produto_tamanho (
        id_tipo_produto INTEGER NOT NULL,
        id_tamanho INTEGER NOT NULL,
        PRIMARY KEY (id_tipo_produto, id_tamanho),
        FOREIGN KEY (id_tipo_produto) REFERENCES tipo_produto(id),
        FOREIGN KEY (id_tamanho) REFERENCES tamanho(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_categoria INTEGER NOT NULL,
        id_genero INTEGER NOT NULL,
        id_marca INTEGER NOT NULL,
        id_cor INTEGER NOT NULL,
        id_tipo_produto INTEGER NOT NULL,
        id_tamanho INTEGER NOT NULL,
        precocusto REAL NOT NULL,
        precovenda REAL NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id),
        FOREIGN KEY (id_genero) REFERENCES generos(id),
        FOREIGN KEY (id_marca) REFERENCES marcas(id),
        FOREIGN KEY (id_cor) REFERENCES cores(id),
        FOREIGN KEY (id_tipo_produto) REFERENCES tipo_produto(id),
        FOREIGN KEY (id_tamanho) REFERENCES tamanho(id)
    )
    """)

    # 2. Tabelas de Endereço
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sigla CHAR(2) NOT NULL,
        nomeestado TEXT NOT NULL
    )
    """)
    
    estates = [
        ('AC','Acre'),('AL','Alagoas'),('AM','Amazonas'),('AP','Amapá'),
        ('BA','Bahia'),('CE','Ceará'),('DF','Distrito Federal'),('ES','Espírito Santo'),
        ('GO','Goiás'),('MA','Maranhão'),('MG','Minas Gerais'),('MS','Mato Grosso do Sul'),
        ('MT','Mato Grosso'),('PA','Pará'),('PB','Paraíba'),('PE','Pernambuco'),
        ('PI','Piauí'),('PR','Paraná'),('RJ','Rio de Janeiro'),('RN','Rio Grande do Norte'),
        ('RO','Rondônia'),('RR','Roraima'),('RS','Rio Grande do Sul'),
        ('SC','Santa Catarina'),('SE','Sergipe'),('SP','São Paulo'),('TO','Tocantins')
    ]
    for sigla, nome in estates:
        cursor.execute("INSERT OR IGNORE INTO estados (sigla, nomeestado) VALUES (?, ?)", (sigla, nome))

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomecidade TEXT NOT NULL,
        id_estado INTEGER NOT NULL,
        FOREIGN KEY (id_estado) REFERENCES estados(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bairros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomebairro TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tiposlogradouro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipologradouro TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logradouros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        logradouro TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cepnorm (
        cep TEXT NOT NULL PRIMARY KEY,
        id_estado INTEGER NOT NULL,
        id_cidade INTEGER NOT NULL,
        id_bairro INTEGER NOT NULL,
        id_tipologradouro INTEGER NOT NULL,
        id_logradouro INTEGER NOT NULL,
        FOREIGN KEY (id_estado) REFERENCES estados(id),
        FOREIGN KEY (id_cidade) REFERENCES cidades(id),
        FOREIGN KEY (id_bairro) REFERENCES bairros(id),
        FOREIGN KEY (id_tipologradouro) REFERENCES tiposlogradouro(id),
        FOREIGN KEY (id_logradouro) REFERENCES logradouros(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enderecos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cep TEXT NOT NULL,
        numero TEXT NOT NULL,
        complemento TEXT,
        FOREIGN KEY (cep) REFERENCES cepnorm(cep)
    )
    """)

    # 3. Contatos e Pessoas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS telefones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numtelefone TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fornecedores (
        cnpj TEXT NOT NULL PRIMARY KEY,
        nome TEXT NOT NULL,
        id_endereco INTEGER NOT NULL,
        id_telefone INTEGER NOT NULL,
        id_email INTEGER NOT NULL,
        FOREIGN KEY (id_endereco) REFERENCES enderecos(id),
        FOREIGN KEY (id_telefone) REFERENCES telefones(id),
        FOREIGN KEY (id_email) REFERENCES emails(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        cpf TEXT NOT NULL PRIMARY KEY,
        nome TEXT NOT NULL,
        id_endereco INTEGER NOT NULL,
        id_telefone INTEGER NOT NULL,
        id_email INTEGER NOT NULL,
        FOREIGN KEY (id_endereco) REFERENCES enderecos(id),
        FOREIGN KEY (id_telefone) REFERENCES telefones(id),
        FOREIGN KEY (id_email) REFERENCES emails(id)
    )
    """)

    # 4. Vendas e Compras
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forma_pgto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        formapgto TEXT NOT NULL
    )
    """)
    cursor.execute("INSERT OR IGNORE INTO forma_pgto (formapgto) VALUES ('Dinheiro'), ('Cartão de Crédito'), ('Cartão de Débito'), ('Pix')")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente TEXT NOT NULL,
        id_formapgto INTEGER NOT NULL,
        data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_cliente) REFERENCES clientes(cpf),
        FOREIGN KEY (id_formapgto) REFERENCES forma_pgto(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unit REAL NOT NULL,
        FOREIGN KEY (id_venda) REFERENCES vendas(id),
        FOREIGN KEY (id_produto) REFERENCES produtos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compras_fornecedor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cnpj_fornecedor TEXT NOT NULL,
        data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        nota_fiscal TEXT,
        FOREIGN KEY (cnpj_fornecedor) REFERENCES fornecedores(cnpj)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compras_fornecedor_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_compra INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unit REAL NOT NULL,
        FOREIGN KEY (id_compra) REFERENCES compras_fornecedor(id),
        FOREIGN KEY (id_produto) REFERENCES produtos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estoque_atual (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS balanco_financeiro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_movimento TIMESTAMP NOT NULL,
        tipo TEXT NOT NULL CHECK(tipo IN ('entrada','saida')),
        valor REAL NOT NULL,
        referencia TEXT NOT NULL
    )
    """)

    db.commit()
    db.close()
