from tkinter import messagebox
import PySimpleGUI as sg
import pandas as pd

def listaProdutos():
    my_list=[]
    x=1
    for index, rows in tabela_produtos.iterrows():
        my_list.append(str(x)+". "+rows.Produto+rows.Marca + "-" + str(rows.Método_Compra))
        x += 1
    return my_list

def listaProdutos1(idx, quantidade):
    my_list = []
    for index, rows in tabela_produtos.iterrows():
        my_list.append(rows.Produto+"-"+rows.Marca+"-"+str(quant)+"-"+str(float(rows.Valor_Método))+"-"+str(float(quant)*float(rows.Valor_Método)))
    y= my_list[int(idx)-1].split("-")
    return y

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

def conferir(num):
    try:
        sheet_nameS=['Estoque','Vendas','Produtos']
        if num < 3:
            dict_df = pd.read_excel(path, sheet_name=sheet_nameS[num])
            tabelas[num]=dict_df.get(sheet_nameS)
        if num < 3:
            conferir(num+1)
    except ValueError as ve1:
        verificarSheet(num)
        conferir(num+1)

#CodigoPandas
path = "Arquivos/Compras.xlsx"
tabela_vendas= pd.DataFrame()
tabela_compras=pd.DataFrame()
tabela_produtos=pd.DataFrame()
tabelas=[tabela_compras,tabela_vendas,tabela_produtos]

try:
    dict_df = pd.read_excel(path, sheet_name=['Produtos', 'Estoque', 'Vendas'])
    tabela_vendas = dict_df.get('Vendas')
    tabela_produtos =dict_df.get('Produtos')
    tabela_compras = dict_df.get('Estoque')
    print("Arquivo Encontrado")
    tabelas = [tabela_compras, tabela_vendas, tabela_produtos]
    print(str(tabelas[0])+"\n"+str(tabelas[1])+"\n"+str(tabelas[2]))
except FileNotFoundError as fnfe:
    dV= {'Produto':[]}
    dC= {'Produto':[], 'Marca':[], 'Quantidade':[], 'Valor Total Gasto':[], 'Valor Total':[]}
    dP= {'Produto':[], 'Marca':[], 'Método de Venda':[], 'Valor_Método':[], 'Método_Compra':[]}
    tabela_vendas=pd.DataFrame(data=dV)
    tabela_compras=pd.DataFrame(data=dC)
    tabela_produtos=pd.DataFrame(data=dP)
    print("Arquivo não lido, criando um dataframe substituto")
except ValueError as ve:
    print("Arquivo encontrado, porém sem todas sheets")
    conferir(0)

#Código
metodosdeVenda = []
produtosAdicionados = []
valorTotal = 0
produtosCadastrados= listaProdutos()

#Layout
def janelaInicial():
    sg.theme('Dark2')
    layout= [
        [sg.Image(r'iconDog.png', size=(500, 500))],
        [sg.Button('Adicionar Produto', expand_x=True)],
        [sg.Button('Vender Produto', expand_x=True)],
        [sg.Button('Histórico', expand_x=True)],
        [sg.Button('Editar Produto', expand_x=True)],
        [sg.Button('Estoque', expand_x=True)],
        [sg.Button('Sair', expand_x=True)]
    ]
    return sg.Window('PetShop', layout=layout, finalize=True)

def janelaCadastro():
    sg.theme('Dark')
    layout=[
        [sg.Text("Cadastrar Produto")],
        [sg.InputText(key="Produto"),sg.InputText(key="MarcaProduto")],
        [sg.Text("Selecione o Método Principal de Compra"),sg.Combo(metodosdeVenda,key="metodoCompra",readonly=True,size=(15,100))],
        [sg.Combo(metodosdeVenda,key="metodoVenda",readonly=True,size=(15,100)),sg.InputText(key='valorProduto')],
        [sg.Button("Adicionar Novo Método de Venda/Compra",key='buttonMetodoVenda')],
        [sg.InputText(key='novoMetodoVendaInput',visible=False),sg.Button("+",key="novoMetodoVenda",visible=False)],
        [sg.Button("EfetuarCadastro")]
    ]
    return sg.Window('Cadastrar Produtos', layout= layout, finalize=True)

def janelaAdicionar():
    sg.theme('Dark2')
    layout= [
        [sg.Text("Adicionar Produtos")],
        [sg.Text("Produto a Adicionar"), sg.Combo(produtosCadastrados, size=(15,100),key="comboProdutos", readonly=True),sg.Button("+", key="CadastroProduto"),sg.Table(values=produtosAdicionados,headings=['Produto','Marca','Quant','ValorUn','ValorTotal'],size=(40,15), key='-TB-')],
        [sg.Text("Quantidade do Produto"), sg.InputText(key="quantidadeAdicionada"),sg.Text("Valor Total da Compra:", justification= 'right',expand_x=True)],
        [sg.Button('+', key='continuarCompra'), sg.Button("Finalizar"),sg.Text(key='valorTotal', justification='right',expand_x=True)]
    ]
    return sg.Window('Adicionar Produtos', layout= layout, finalize=True)

#Janela
janela1, janela2, janela3= janelaInicial(), None, None

#Ler os eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    #Adicionar Produto
    if janela == janela2 and eventos == 'continuarCompra':
        atual = valores['comboProdutos']
        if atual in produtosCadastrados:
            if not valores['quantidadeAdicionada'] =="":
                try:
                    if int(valores['quantidadeAdicionada']) >= 0:
                        quant = int(valores['quantidadeAdicionada'])
                        provisorio = valores['comboProdutos'].split(". ")
                        produto = listaProdutos1(provisorio[0], quant)
                        produtoAdicionado=[produto[0], produto[1], produto[2], produto[3]+" R$", produto[4]+" R$"]
                        produtosAdicionados.append(produtoAdicionado)
                        valorTotal += float(produto[4])
                        janela["-TB-"].Update(values=produtosAdicionados)
                        janela["valorTotal"].Update(str(valorTotal)+',00 R$')
                        janela["quantidadeAdicionada"].Update("")
                        janela["comboProdutos"].Update("")
                        new_rowC = {'Produto': produto[0],
                                    'Marca': produto[1],
                                    'Quantidade': produto[2],
                                    'Valor Total Gasto': produto[4]}
                        #tabela_compras["Valor Total"].ffill()
                        tabela_compras = tabela_compras.append(new_rowC, ignore_index=True)
                        with pd.ExcelWriter(path) as writer:
                            tabela_produtos.to_excel(writer, sheet_name='Produtos',index=False)
                            tabela_compras.to_excel(writer, sheet_name='Estoque',index=False)
                            tabela_vendas.to_excel(writer, sheet_name='Vendas',index=False)
                    else:
                        messagebox.showwarning("Erro ao Adicionar", 'Valor abaixo de 0 não é aceito')
                except ValueError as ve:
                    messagebox.showwarning("Erro ao Adicionar", 'O campo Quantidade apenas aceita Números')
            else:
                messagebox.showwarning("Erro ao Adicionar", 'Valor inválido no campo "Quantidade"')
        else:
            messagebox.showwarning("Erro ao Adicionar", 'Selecione um produto para adicionar')

    # Ir para janela Cadastrar Produto
    if janela == janela2 and eventos == 'CadastroProduto':
        janela3 = janelaCadastro()
        janela2.hide()

    # Adicionar Método de Venda
    if janela == janela3 and eventos == 'buttonMetodoVenda':
        janela["novoMetodoVendaInput"].Update(visible=True)
        janela["novoMetodoVenda"].Update(visible=True)

    # Confirmar novo Método de Venda
    if janela == janela3 and eventos == 'novoMetodoVenda' and not valores['novoMetodoVendaInput'] == '':
        metodosdeVenda.append(valores['novoMetodoVendaInput'])
        valores["novoMetodoVendaInput"] = ""
        janela["novoMetodoVendaInput"].Update(visible=False)
        janela["novoMetodoVenda"].Update(visible=False)
        janela['metodoVenda'].Update(values=metodosdeVenda)
        janela['metodoCompra'].Update(values=metodosdeVenda)

    # Confirmar novo Produto
    if janela == janela3 and eventos == 'EfetuarCadastro':
        current = valores['metodoVenda']
        current2= valores['metodoCompra']
        if current in metodosdeVenda:
            if current2 in metodosdeVenda:
                if valores["Produto"] == "" or valores["valorProduto"] == "" or valores['MarcaProduto'] == "":
                    messagebox.showwarning("Preencha Todos os campos", 'Preencha os campos corretamente')
                else:
                    try:
                        a = int(valores['valorProduto'])
                        new_rowP = {'Produto': valores["Produto"],
                                    'Marca': valores["MarcaProduto"],
                                    'Método_Venda': valores["metodoVenda"],
                                    'Método_Compra': valores["metodoCompra"],
                                    'Valor_Método': valores["valorProduto"]}
                        tabela_produtos = tabela_produtos.append(new_rowP, ignore_index=True)
                        with pd.ExcelWriter(path) as writer:
                            tabela_produtos.to_excel(writer, sheet_name='Produtos')
                            tabela_compras.to_excel(writer, sheet_name='Estoque')
                            tabela_vendas.to_excel(writer, sheet_name='Vendas')
                        janela3.hide()
                        produtosCadastrados = listaProdutos()
                        janela2['comboProdutos'].Update(values=produtosCadastrados)
                        janela2.un_hide()
                    except ValueError as ve:
                        messagebox.showwarning("Erro ao Cadastrar", 'O campo Valor do Produto apenas aceita Números '+str(ve))
            else:
                messagebox.showwarning("Preencha Todos os campos", 'Preencha o campo de Método de Compra')
        else:
            messagebox.showwarning("Preencha Todos os campos", 'Preencha o campo de Método de Venda')

    # Sair da janela Cadastrar Produto e Voltar para Adicionar Produto
    if janela == janela3 and eventos == sg.WINDOW_CLOSED:
        janela3.hide()
        janela2["-TB-"].Update(produtosAdicionados)
        janela2['valorTotal'].Update("")
        janela2.un_hide()

    #Ir para janela Adicionar Produto
    if janela == janela1 and eventos == 'Adicionar Produto':
        janela2 = janelaAdicionar()
        janela2['comboProdutos'].Update(values = produtosCadastrados)
        produtosAdicionados.clear()
        janela2["-TB-"].Update(produtosAdicionados)
        janela1.hide()

    #Sair da janela Adicionar Produto e Voltar a Inicial
    if janela == janela2 and eventos == sg.WINDOW_CLOSED:
        janela2.hide()
        janela1.un_hide()

    #Fechar Programa
    if janela == janela1 and eventos == sg.WINDOW_CLOSED or eventos == 'Sair':
        break
janela.close()