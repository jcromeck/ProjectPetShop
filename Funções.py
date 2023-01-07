import pandas as pd

def listaProdutos(tabela_produtos, n):
    my_list = []
    for index, rows in tabela_produtos.iterrows():
        if n == 0:
            my_list.append(rows.Produto+"-"+rows.Marca + "-" + rows.Método_Compra)
        if n == 1:
            my_list.append(rows.Produto+"-"+rows.Marca + "-" + rows.Método_Venda)
    return my_list

def listaProdutosV(tabela_compras):
    my_list = []
    for index, rows in tabela_compras.iterrows():
        my_list.append(rows.Produto+'-'+rows.Marca + "-" + str(rows.Método))
    return my_list

def listaProdutos1(tabela_produtos, idx, quant,n):
    my_list = []
    y = []
    if n == 0:
        for index, rows in tabela_produtos.iterrows():
            my_list.append(rows.Produto + "-" + rows.Marca + "-" + rows.Método_Compra + "-" + str(quant) + "-" + str(
                float(rows.Valor_Compra)) + "-" + str(float(rows.Valor_Compra) * float(quant)))
        y = my_list[int(idx)].split("-")
    if n == 1:
        for index, rows in tabela_produtos.iterrows():
            my_list.append(rows.Produto + "-" + rows.Marca + "-" + rows.Método_Venda + "-" + str(quant) + "-" + str(
                float(rows.Valor_Venda)) + "-" + str(float(rows.Valor_Compra)))
        y = my_list[int(idx)].split("-")
    return y

def numVenda(tabela_vendas):
    my_list = ''
    for index, rows in tabela_vendas.iterrows():
        my_list = str(int(rows.NumVenda)+1)
    return my_list

def listaProdutosV1(tabelas, idx, quant, n):
    my_list = []
    y = []
    if n == 0:
        for index, rows in tabelas[2].iterrows():
            my_list.append(rows.Produto + "-" + rows.Marca + "-" + rows.Método_Compra + "-" + str(quant) + "-" + str(
                float(rows.Valor_Venda)) + "-" + str(float(rows.Valor_Venda) * float(quant)))
        y = my_list[int(idx)].split("-")
    if n == 1:
        for index, rows in tabelas[2].iterrows():
            my_list.append(rows.Produto + "-" + rows.Marca + "-" + rows.Método_Venda + "-" + str(quant) + "-" + str(
                float(rows.Valor_Venda)) + "-" + str(float(rows.Valor_Compra)))
        y = my_list[int(idx)].split("-")
    return y

def writerE(tabelas, path):
    with pd.ExcelWriter(path) as writer:
        tabelas[2].to_excel(writer, sheet_name='Produtos', index=False)
        tabelas[0].to_excel(writer, sheet_name='Estoque', index=False)
        tabelas[1].to_excel(writer, sheet_name='Vendas', index=False)
        tabelas[3].to_excel(writer, sheet_name='Métodos', index=False)
        tabelas[4].to_excel(writer, sheet_name='P_Vendas', index=False)

def listaMetodos(tabela_metodos):
    my_list = []
    for index, rows in tabela_metodos.iterrows():
        my_list.append(rows.Métodos)
    return my_list

