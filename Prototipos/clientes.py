from database import conectar

def registrar_cliente(cpf, nome, cep, numero, complemento, telefone, email):
    db = conectar()
    cursor = db.cursor()
    
    cursor.execute("SELECT cep FROM cepnorm WHERE cep=?", (cep,))
    if not cursor.fetchone():
        cursor.execute("INSERT OR IGNORE INTO cepnorm (cep, id_estado, id_cidade, id_bairro, id_tipologradouro, id_logradouro) VALUES (?, 1, 1, 1, 1, 1)", (cep,))
    
    cursor.execute("INSERT INTO enderecos (cep, numero, complemento) VALUES (?,?,?)", (cep, numero, complemento))
    id_endereco = cursor.lastrowid
    
    cursor.execute("INSERT INTO telefones (numtelefone) VALUES (?)", (telefone,))
    id_telefone = cursor.lastrowid
    
    cursor.execute("INSERT INTO emails (email) VALUES (?)", (email,))
    id_email = cursor.lastrowid
    
    cursor.execute("INSERT INTO clientes (cpf, nome, id_endereco, id_telefone, id_email) VALUES (?,?,?,?,?)", 
                   (cpf, nome, id_endereco, id_telefone, id_email))
    db.commit()
    db.close()

def registrar_venda(cpf_cliente, id_formapgto, produtos):
    """
    produtos = lista de dicts: [{"id_produto":1,"quantidade":2,"valor_unit":25.50}, ...]
    """
    db = conectar()
    cursor = db.cursor()
    
    cursor.execute("SELECT cpf FROM clientes WHERE cpf=?", (cpf_cliente,))
    if not cursor.fetchone():

        raise ValueError("Cliente não encontrado. Cadastre o cliente primeiro.")

    cursor.execute("INSERT INTO vendas (id_cliente, id_formapgto) VALUES (?,?)", (cpf_cliente, id_formapgto))
    id_venda = cursor.lastrowid

    for p in produtos:
        #inserir item
        cursor.execute("""
            INSERT INTO vendas_itens (id_venda, id_produto, quantidade, valor_unit)
            VALUES (?,?,?,?)
        """, (id_venda, p["id_produto"], p["quantidade"], p["valor_unit"]))

        #atualizar estoque
        cursor.execute("SELECT quantidade FROM estoque_atual WHERE produto_id=?", (p["id_produto"],))
        resultado = cursor.fetchone()
        if resultado and resultado[0] >= p["quantidade"]:
            nova_qtd = resultado[0] - p["quantidade"]
            cursor.execute("UPDATE estoque_atual SET quantidade=? WHERE produto_id=?", (nova_qtd, p["id_produto"]))
        else:
            raise ValueError(f"Estoque insuficiente para produto {p['id_produto']}")
            
        cursor.execute("INSERT INTO balanco_financeiro (data_movimento, tipo, valor, referencia) VALUES (CURRENT_TIMESTAMP, 'entrada', ?, ?)", 
                       (p["quantidade"] * p["valor_unit"], f"Venda {id_venda} - Produto {p['id_produto']}"))

    db.commit()
    cursor.close()
    db.close()
    return id_venda
