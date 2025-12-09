from database import conectar

def pegar_id(table, coluna, valor):
    db = conectar()
    cursor = db.cursor()
    cursor.execute(f"SELECT id FROM {table} WHERE {coluna}=?", (valor,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()
    return resultado[0] if resultado else None

def salvar_produto(categoria, tipo_produto, genero, marca, cor, tamanho, precocusto, precovenda):
    # Helper to get or create ID
    def get_or_create(table, col, val):
        if not val: return None
        id_val = pegar_id(table, col, val)
        if id_val: return id_val
        
        db = conectar()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO {table} ({col}) VALUES (?)", (val,))
        db.commit()
        new_id = cursor.lastrowid
        cursor.close()
        db.close()
        return new_id

    id_categoria = get_or_create("categoria", "nome", categoria)
    id_tipo = get_or_create("tipo_produto", "nome", tipo_produto)
    id_genero = get_or_create("generos", "genero", genero)
    id_marca = get_or_create("marcas", "nomemarca", marca)
    id_cor = get_or_create("cores", "nomecor", cor)
    id_tamanho = get_or_create("tamanho", "tamanho", tamanho)

    # Note: In the new schema, tipo_produto has id_categoria. We should update it if needed or check consistency.
    # For simplicity, we assume the user selected compatible types.
    
    db = conectar()
    cursor = db.cursor()
    sql = """
        INSERT INTO produtos (id_categoria, id_tipo_produto, id_genero, id_marca, id_cor, id_tamanho, precocusto, precovenda)
        VALUES (?,?,?,?,?,?,?,?)
    """
    cursor.execute(sql, (id_categoria, id_tipo, id_genero, id_marca, id_cor, id_tamanho, precocusto, precovenda))
    db.commit()
    produto_id = cursor.lastrowid
    cursor.close()
    db.close()
    return produto_id

def salvar_estoque(produto_id, quantidade):
    db = conectar()
    cursor = db.cursor()
    sql = "INSERT INTO estoque_atual (produto_id, quantidade) VALUES (?, ?)"
    cursor.execute(sql, (produto_id, quantidade))
    db.commit()
    cursor.close()
    db.close()

def atualizar_estoque(produto_id, quantidade):
    db = conectar()
    cursor = db.cursor()
    cursor.execute("SELECT quantidade FROM estoque_atual WHERE produto_id=?", (produto_id,))
    resultado = cursor.fetchone()
    if resultado:
        nova_qtd = resultado[0] + quantidade
        cursor.execute("UPDATE estoque_atual SET quantidade=? WHERE produto_id=?", (nova_qtd, produto_id))
    else:
        cursor.execute("INSERT INTO estoque_atual (produto_id, quantidade) VALUES (?,?)", (produto_id, quantidade))
    db.commit()
    cursor.close()
    db.close()
