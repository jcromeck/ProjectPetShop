import pandas as pd

def listaProdutos(tabela_produtos):
    my_list=[]
    x=1
    for index, rows in tabela_produtos.iterrows():
        my_list.append(str(x)+". "+rows.Produto+rows.Marca + "-" + str(rows.Método_Compra))
        x += 1
    return my_list

def listaProdutosV(tabela_compras):
    my_list=[]
    x=1
    for index, rows in tabela_compras.iterrows():
        my_list.append(str(x)+". "+rows.Produto+' - '+rows.Marca)
        x += 1
    return my_list

def listaProdutos1(tabela_produtos, idx, quant):
    my_list = []
    for index, rows in tabela_produtos.iterrows():
        my_list.append(rows.Produto+"-"+rows.Marca+"-"+str(quant)+"-"+str(float(rows.Valor_Método))+"-"+str(float(quant)*float(rows.Valor_Método)))
    y= my_list[int(idx)-1].split("-")
    return y

def listaProdutosV1(tabela_compras, idx, quant, metodo_venda, num_Venda):
    my_list = []
    for index, rows in tabela_compras.iterrows():
        my_list.append(rows.Produto+"-"+rows.Marca+"-"+str(quant)+"-"+str(float(rows.Valor_Unitário))+"-"+str(float(quant)*float(rows.Valor_Unitário))+'-'+str(metodo_venda))
    y= my_list[int(idx)-1].split("-")
    return y

def listaMetodos(tabela_metodos):
    my_list = []
    for index, rows in tabela_metodos.iterrows():
        my_list.append(rows.Métodos)
    return my_list

def verificarSheet(num):
    if num == 0: #Problema em Estoque
        dC = {'Produto': [], 'Marca': [], 'Quantidade': [], 'Valor Total Gasto': [], 'Valor Total': []}
        tabela_compras = pd.DataFrame.from_dict(dC)
        print('Estoque')
    if num == 1: #Problema em Vendas
        dV = {'Produto': []}
        tabela_vendas = pd.DataFrame.from_dict(dV)
        print('Vendas')
    if num == 2: #Problema em Produtos
        dP = {'Produto': [], 'Marca': [], 'Método de Venda': [], 'Valor_Método': [], 'Método_Compra': []}
        tabela_produtos = pd.DataFrame.from_dict(dP)
        print('Produtos')
    if num == 3: #Problema em Métodos
        dM = {'Métodos':[]}
        tabela_metodos = pd.DataFrame.from_dict(dM)
        print('Métodos')

def conferir(tabelas, path, num):
    try:
        sheet_nameS=['Estoque','Vendas','Produtos','Métodos']
        if num < 4:
            dict_df = pd.read_excel(path, sheet_name=sheet_nameS[num])
            tabelas[num]=dict_df.get(sheet_nameS)
        if num < 4:
            conferir(num+1)
    except ValueError as ve1:
        verificarSheet(num)
        conferir(num+1)