import pandas as pd

def listaProdutos(tabela_produtos):
    my_list=[]
    for index, rows in tabela_produtos.iterrows():
        my_list.append(rows.Produto+"-"+rows.Marca + "-" + str(rows.Método_Compra))
    return my_list

def listaProdutosV(tabela_compras):
    my_list=[]
    for index, rows in tabela_compras.iterrows():
        my_list.append(rows.Produto+' - '+rows.Marca)
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

def verificarSheet(tabelas, num, path):
    if num == 0: #Problema em Estoque
        dC = {'Produto': ['Ração'], 'Marca': ['Pedigree'], 'Método': ['Pacote'], 'Quantidade': ['10'], 'Valor_Compra': ['8'], 'Valor_Venda':['10']}
        tabelas[0] = pd.DataFrame.from_dict(dC)
    if num == 1: #Problema em Vendas
        dV = {'Produto':[],
              'Marca':[],
              'Quantidade':[],
              'Valor_Unitário': [],
              'Valor_Total': [],
              'Método_Venda': [],
              'NumVenda': []}
        tabelas[1] = pd.DataFrame.from_dict(dV)
    if num == 2: #Problema em Produtos
        dP = {'Produto': [],
              'Marca': [],
              'Valor_Venda': [],
              'Valor_Compra': [],
              'Método_Venda': [],
              'Método_Compra': []}
        tabelas[2] = pd.DataFrame.from_dict(dP)
    if num == 3: #Problema em Métodos
        dM = {'Métodos':[]}
        tabelas[3] = pd.DataFrame.from_dict(dM)
    with pd.ExcelWriter(path) as writer:
        tabelas[2].to_excel(writer, sheet_name='Produtos', index=False)
        tabelas[0].to_excel(writer, sheet_name='Estoque', index=False)
        tabelas[1].to_excel(writer, sheet_name='Vendas', index=False)
        tabelas[3].to_excel(writer, sheet_name='Métodos', index=False)

def conferir(tabelas, path, num):
    try:
        sheet_nameS=['Estoque', 'Vendas', 'Produtos', 'Métodos']
        if num < 4:
            dict_df = pd.read_excel(path, sheet_name=sheet_nameS[num])
            tabelas[num]=dict_df.get(sheet_nameS)
        if num < 4:
            conferir(tabelas, path, num+1)
        else:
            print('Tabela do Conferir: \n')
            print(tabelas)
            return tabelas
    except ValueError as ve1:
        tabelas[num] = verificarSheet(tabelas, num, path)
        conferir(tabelas, path, num+1)

def valorEestoque(tabelas, idx, num):
    my_list1 = []
    my_list2 = []
    x = []
    x1 =[]
    count =0
    for index, rows in tabelas[0].iterrows():
        my_list1.append(rows.Produto + rows.Marca + rows.Método + '-' + str(rows.Quantidade))
    for index, rows in tabelas[2].iterrows():
        my_list2.append(rows.Produto + rows.Marca + rows.Método_Compra + '-' + str(rows.Valor_Compra))
    y = my_list2[int(idx-1)].split('-')
    z = y[0]
    z1 =y[1]
    for n in range(len(tabelas[0])):
        y = my_list1[n].split("-")
        x.append(y[0])
        x1.append(y[1])
        if x[n] == z:
            count=1
            if num == 0:  # QUANTIDADE
                return x1[n]
            if num == 1:  # VALOR
                return z1
    if count == 0:
        if num == 0:
            return 0
        if num == 1:
            return z1