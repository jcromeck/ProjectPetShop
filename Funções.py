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

def listaProdutos1(tabela_produtos, idx, quant,n):
    my_list = []
    if n == 0:
        for index, rows in tabela_produtos.iterrows():
            my_list.append(rows.Produto+"-"+rows.Marca+"-"+rows.Método_Venda+"-"+str(quant)+"-"+str(float(rows.Valor_Venda))+"-"+str(float(rows.Valor_Venda)*float(quant)))
        y= my_list[int(idx)-1].split("-")
    if n == 1:
        for index, rows in tabela_produtos.iterrows():
            my_list.append(rows.Produto+"-"+rows.Marca+"-"+rows.Método_Venda+"-"+str(quant)+"-"+str(float(rows.Valor_Venda))+"-"+str(float(rows.Valor_Compra)))
        y = my_list[int(idx) - 1].split("-")
    return y

def numVenda(tabela_vendas):
    my_list=''
    for index, rows in tabela_vendas.iterrows():
        my_list = str(int(rows.NumVenda)+1)
    return my_list

def listaProdutosV1(tabela_vendas, tabela_compras, idx, quant, metodo_venda):
    my_list = []
    num = numVenda(tabela_vendas)
    for index, rows in tabela_compras.iterrows():
        my_list.append(rows.Produto+"-"+rows.Marca+"-"+str(quant)+"-"+str(float(rows.Valor_Venda))+"-"+str(float(quant)*float(rows.Valor_Venda))+'-'+str(metodo_venda)+'-'+str(num))
    y= my_list[int(idx)-1].split("-")
    return y

def listaMetodos(tabela_metodos):
    my_list = []
    for index, rows in tabela_metodos.iterrows():
        my_list.append(rows.Métodos)
    return my_list

def verificarSheet(num):
    if num == 0: #Problema em Estoque
        dC = {'Produto': ['Ração'], 'Marca': ['Pedigree'], 'Método': ['Pacote'], 'Quantidade': ['10'], 'Valor_Compra': ['8'], 'Valor_Venda':['10']}
        tabela_compras = pd.DataFrame.from_dict(dC)
    if num == 1: #Problema em Vendas
        dV = {'Produto': []}
        tabela_vendas = pd.DataFrame.from_dict(dV)
    if num == 2: #Problema em Produtos
        dP = {'Produto': [], 'Marca': [], 'Método de Venda': [], 'Valor_Método': [], 'Método_Compra': []}
        tabela_produtos = pd.DataFrame.from_dict(dP)
    if num == 3: #Problema em Métodos
        dM = {'Métodos':[]}
        tabela_metodos = pd.DataFrame.from_dict(dM)

def conferir(tabelas, path, num):
    try:
        sheet_nameS=['Estoque', 'Vendas', 'Produtos', 'Métodos']
        if num < 4:
            dict_df = pd.read_excel(path, sheet_name=sheet_nameS[num])
            tabelas[num]=dict_df.get(sheet_nameS)
        if num < 4:
            conferir(tabelas, path, num+1)
    except ValueError as ve1:
        verificarSheet(num)
        conferir(tabelas, path, num+1)