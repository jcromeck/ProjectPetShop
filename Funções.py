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

def listaProdutos1(tabela_produtos, idx, quant, id, n):
    my_list = []
    y = []
    if n == 0:
        for index, rows in tabela_produtos.iterrows():
            my_list.append(rows.Produto + "-" + rows.Marca + "-" + rows.Método_Compra + "-" + str(quant) + "-" + str(
                float(rows.Valor_Compra)) + "-" + str(float(rows.Valor_Compra) * float(quant)))
        y = my_list[int(idx)].split("-")
    if n == 1:
        for index, rows in tabela_produtos.iterrows():
            my_list.append(str(id) + "-" + rows.Produto + "-" + rows.Marca + "-" + rows.Método_Compra + "-" + str(
                quant) + "-" + str(float(rows.Valor_Compra)) + "-" + str(float(rows.Valor_Compra) * float(quant)))
        y = my_list[int(idx)].split("-")
    return y

def numVenda(tabela_vendas):
    my_list = ''
    for index, rows in tabela_vendas.iterrows():
        my_list = str(int(rows.NumVenda)+1)
    return my_list

def listaProdutosV1(tabela_produtos, idx, quant):
    my_list = []
    y = []
    for index, rows in tabela_produtos.iterrows():
        my_list.append(rows.Produto + "-" + rows.Marca + "-" + rows.Método_Venda + "-" + str(quant) + "-" + str(
            float(rows.Valor_Venda)) + "-" + str(float(rows.Valor_Venda) * float(quant)))
    y = my_list[int(idx)].split("-")
    return y
# Perfeito
def writerE(tabelas, path):
    with pd.ExcelWriter(path) as writer:
        tabelas[0].to_excel(writer, sheet_name='Métodos', index=False)
        tabelas[1].to_excel(writer, sheet_name='Produtos', index=False)
        tabelas[2].to_excel(writer, sheet_name='P_Vendas', index=False)
        tabelas[3].to_excel(writer, sheet_name='Vendas', index=False)
        tabelas[4].to_excel(writer, sheet_name='P_Compras', index=False)
        tabelas[5].to_excel(writer, sheet_name='Compras', index=False)
        tabelas[6].to_excel(writer, sheet_name='Estoque', index=False)

def listaMetodos(tabela_metodos):
    my_list = []
    for index, rows in tabela_metodos.iterrows():
        my_list.append(rows.Método)
    return my_list

