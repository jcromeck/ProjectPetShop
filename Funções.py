import pandas as pd

def listaProdutos(tabela_produtos, n):
    my_list = []
    for index, rows in tabela_produtos.iterrows():
        m_l = []
        if n == 0:
            k = 0
            m_l.append(rows.Produto+"-"+rows.Marca + "-" + rows.Método_Compra)
            for m in range(len(m_l)):
                for num in range(len(my_list)):
                    if m_l[m] == my_list[num]:
                        k = 1
            if k == 0:
                my_list.append(rows.Produto+"-"+rows.Marca + "-" + rows.Método_Compra)
        if n == 1:
            my_list.append(rows.Produto+"-"+rows.Marca + "-" + rows.Método_Venda)
        if n == 2:
            m_l.append(rows.Produto + '-' + rows.Marca + '-' + rows.Método_Venda + '-' + str(
                rows.Valor_Venda) + '-' + rows.Método_Compra + '-' + str(rows.Valor_Compra))
            m_l = m_l[0].split('-')
            my_list.append(m_l)
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

def listaProdutosV1(tabela_produtos, idx, quant, id):
    my_list = []
    y = []
    for index, rows in tabela_produtos.iterrows():
        my_list.append(str(id) + "-" + rows.Produto + "-" + rows.Marca + "-" + rows.Método_Venda + "-" + str(
            quant) + "-" + str(float(rows.Valor_Venda)) + "-" + str(float(rows.Valor_Venda) * float(quant)))
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
    for index, rows in tabela_vendas.iterrows():
        my_list.append(rows.ID)
        my_list.append(rows.Data)
        my_list.append(rows.QItens)
        my_list.append(rows.Valor_Total)
        y.append(my_list)
        my_list = []
    return y

def listarBusca(tabelas, id, quant, data, vT, janela):
    venda = []
    vendaP = []
    compra = []
    compraP = []
    if id == '' and quant == '' and data == '' and vT == '':
        for index, rows in tabelas[3].iterrows():
            venda = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
            vendaP.append(venda)
        for index, rows in tabelas[5].iterrows():
            compra = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
            compraP.append(compra)
            janela['-TBHV-'].Update(values=vendaP)
            janela['-TBHC-'].Update(values=compraP)
        return
    for index, rows in tabelas[3].iterrows():
        if str(id) == str(rows.ID):
            venda = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
        if str(quant) == str(rows.QItens):
            venda = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
        if str(data) == str(rows.Data):
            venda = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
        if str(vT) == str(rows.Valor_Total):
            venda = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
        if venda != []:
            vendaP.append(venda)
            venda = []
    for index, rows in tabelas[5].iterrows():
        if str(id) == str(rows.ID):
            compra = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
        if str(quant) == str(rows.QItens):
            compra = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
        if str(data) == str(rows.Data):
            compra = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
        if str(vT) == str(rows.Valor_Total):
            compra = [str(rows.ID), rows.Data, str(rows.QItens), str(rows.Valor_Total)]
        compraP.append(compra)
    janela['-TBHV-'].Update(values=vendaP)
    janela['-TBHC-'].Update(values=compraP)
    return

def listaEstoque(tabela_estoque):
    my_list = []
    y = []
    for index, rows in tabela_estoque.iterrows():
        my_list.append(rows.Produto+'-'+rows.Marca+'-'+rows.Método+'-'+str(rows.Quantidade))
        my_list = my_list[0].split('-')
        y.append(my_list)
        my_list= []
    return y

def listarID(tabelaID):
    n = 0
    for index, rows in tabelaID.iterrows():
        n = rows.ID
    n = int(n)+1
    return n