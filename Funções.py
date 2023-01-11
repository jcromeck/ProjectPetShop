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

def listarVC(tabela_vendas):
    my_list = []
    y = []
    x = []
    for index, rows in tabela_vendas.iterrows():
        x = str(rows.Data).split(" ")
        x = x[0].split("-")
        dataS = x[2] + "/" + x[1] + "/" + x[0]
        my_list.append(rows.ID)
        my_list.append(dataS)
        my_list.append(rows.QItens)
        my_list.append(rows.Valor_Total)
        y.append(my_list)
        my_list = []
    return y

def listarBusca(tabelas, id, quant, data, vT):
    venda = []
    vendaP = []
    compra = []
    compraP = []
    y = []
    for index, rows in tabelas[3].iterrows():
        y = str(rows.Data).split(" ")
        y = y[0].split("-")
        dataS = y[2]+"/"+y[1]+"/"+y[0]
        if str(id) == str(rows.ID):
            venda = [str(rows.ID), dataS, str(rows.QItens), str(rows.Valor_Total)]
        if str(quant) == str(rows.QItens):
            venda = [str(rows.ID), dataS, str(rows.QItens), str(rows.Valor_Total)]
        if str(data) == str(rows.Data):
            venda = [str(rows.ID), dataS, str(rows.QItens), str(rows.Valor_Total)]
        if str(vT) == str(rows.Valor_Total):
            venda = [str(rows.ID), dataS, str(rows.QItens), str(rows.Valor_Total)]
        vendaP.append(venda)
    for index, rows in tabelas[5].iterrows():
        y = str(rows.Data).split(" ")
        y = y[0].split("-")
        dataS = y[2] + "/" + y[1] + "/" + y[0]
        if str(id) == str(rows.ID):
            compra = [str(rows.ID), dataS, str(rows.QItens), str(rows.Valor_Total)]
        if str(quant) == str(rows.QItens):
            compra = [str(rows.ID), dataS, str(rows.QItens), str(rows.Valor_Total)]
        if str(data) == str(rows.Data):
            compra = [str(rows.ID), dataS, str(rows.QItens), str(rows.Valor_Total)]
        if str(vT) == str(rows.Valor_Total):
            compra = [str(rows.ID), dataS, str(rows.QItens), str(rows.Valor_Total)]
        compraP.append(compra)
    return vendaP, compraP

