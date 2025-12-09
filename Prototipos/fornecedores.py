from database import conectar

def registrar_fornecedor(cnpj, nome, cep, numero, complemento, telefone, email):
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
    
    cursor.execute("INSERT INTO fornecedores (cnpj, nome, id_endereco, id_telefone, id_email) VALUES (?,?,?,?,?)", 
                   (cnpj, nome, id_endereco, id_telefone, id_email))
    db.commit()
    db.close()

def registrar_compra(cnpj_fornecedor, produtos): 
    """
    produtos = lista de dicts: [{"id_produto":1,"quantidade":5,"valor_unit":10.50}, ...]
    """
    db = conectar()
    cursor = db.cursor()
    
    cursor.execute("SELECT cnpj FROM fornecedores WHERE cnpj=?", (cnpj_fornecedor,))
    if not cursor.fetchone():
        pass

    cursor.execute("INSERT INTO compras_fornecedor (cnpj_fornecedor) VALUES (?)", (cnpj_fornecedor,))
    id_compra = cursor.lastrowid

    for p in produtos:
        cursor.execute("""
            INSERT INTO compras_fornecedor_itens (id_compra, id_produto, quantidade, valor_unit)
            VALUES (?,?,?,?)
        """, (id_compra, p["id_produto"], p["quantidade"], p["valor_unit"]))
        #atualizar estoque
        cursor.execute("SELECT quantidade FROM estoque_atual WHERE produto_id=?", (p["id_produto"],))
        resultado = cursor.fetchone()
        if resultado:
            nova_qtd = resultado[0] + p["quantidade"]
            cursor.execute("UPDATE estoque_atual SET quantidade=? WHERE produto_id=?", (nova_qtd, p["id_produto"]))
        else:
            cursor.execute("INSERT INTO estoque_atual (produto_id, quantidade) VALUES (?,?)", (p["id_produto"], p["quantidade"]))
            
        cursor.execute("INSERT INTO balanco_financeiro (data_movimento, tipo, valor, referencia) VALUES (CURRENT_TIMESTAMP, 'saida', ?, ?)", 
                       (p["quantidade"] * p["valor_unit"], f"Compra {id_compra} - Produto {p['id_produto']}"))
                       
    db.commit()
    cursor.close()
    db.close()
    return id_compra
