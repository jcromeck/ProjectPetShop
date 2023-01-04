from tkinter import messagebox
import PySimpleGUI as sg
import pandas as pd
from Funções import listaMetodos, listaProdutos, listaProdutos1, conferir, listaProdutosV, listaProdutosV1
from datetime import date
from Adicionar import mainA

def newRow(d, n, n1):
    if n == 10:
        for row in range(len(rowVendas)):
            tabela_vendas.append(rowVendas[row], ignore_index=True)
        with pd.ExcelWriter(path) as writer:
            tabela_produtos.to_excel(writer, sheet_name='Produtos', index=False)
            tabela_estoque.to_excel(writer, sheet_name='Estoque', index=False)
            tabela_vendas.to_excel(writer, sheet_name='Vendas', index=False)
            tabela_metodos.to_excel(writer, sheet_name='Métodos', index=False)
        rowVendas.clear()
    if n == 11:
        for row in range(len(rowEstoque)):
            tabela_estoque.append(rowEstoque[row], ignore_index=True)
        with pd.ExcelWriter(path) as writer:
            tabela_produtos.to_excel(writer, sheet_name='Produtos', index=False)
            tabela_estoque.to_excel(writer, sheet_name='Estoque', index=False)
            tabela_vendas.to_excel(writer, sheet_name='Vendas', index=False)
            tabela_metodos.to_excel(writer, sheet_name='Métodos', index=False)
        rowEstoque.clear()
    if n == 12:
        for row in range(len(rowProdutos)):
            tabela_produtos.append(rowProdutos[row], ignore_index=True)
        with pd.ExcelWriter(path) as writer:
            tabela_produtos.to_excel(writer, sheet_name='Produtos', index=False)
            tabela_estoque.to_excel(writer, sheet_name='Estoque', index=False)
            tabela_vendas.to_excel(writer, sheet_name='Vendas', index=False)
            tabela_metodos.to_excel(writer, sheet_name='Métodos', index=False)
        rowProdutos.clear()

def Dtto_Excel(tabelas, num):
    new_row = dict()
    #Vendas
    if num == 0:
        new_row = {'Produto': estoque[0],
                    'Marca': estoque[1],
                    'Quantidade': estoque[2],
                    'Valor_Unitário': estoque[3],
                    'Valor_Total': estoque[4],
                    'Método_Venda': estoque[5],
                    'NumVenda': estoque[6]}
        newRow(new_row, 0, None)
        print('Vendas NovaLinha')
    #Estoque
    if num == 1:
        quant = int(valores['quantidadeAdicionada'])
        provisorio = valores['comboProdutos'].split(". ")
        produtosProv = listaProdutos1(tabela_produtos, provisorio[0], quant, 1)
        new_row = {'Produto':      produtosProv[0],
                   'Marca':        produtosProv[1],
                   'Método':       produtosProv[2],
                   'Quantidade':   produtosProv[3],
                   'Valor_Venda':  produtosProv[4],
                   'Valor_Compra': produtosProv[5]}
        tabela_estoqueProv = tabelas[0].append(new_row, ignore_index=True)
        print('Estoque Prov Com nova linha')
    #Produtos
    if num == 2:
        new_row = {'Produto': valores["Produto"],
                   'Marca': valores["MarcaProduto"],
                   'Valor_Venda': valores['valorMVenda'],
                   'Valor_Compra': valores['valorMCompra'],
                   'Método_Venda': valores["metodoVenda"],
                   'Método_Compra': valores["metodoCompra"],
                   'ReporEstoquepProd': outroProduto}
        tabelas[2]= tabelas[2].append(new_row, ignore_index=True)
        with pd.ExcelWriter(path) as writer:
            tabelas[2].to_excel(writer, sheet_name='Produtos', index=False)
            tabelas[0].to_excel(writer, sheet_name='Estoque', index=False)
            tabelas[1].to_excel(writer, sheet_name='Vendas', index=False)
            tabelas[3].to_excel(writer, sheet_name='Métodos', index=False)
        print('Produtos Nova Linha')
        return tabelas
    #Métodos
    if num == 3:

        return tabelas

#CodigoPandas
path = "Arquivos/Compras.xlsx"
tabela_vendas = pd.DataFrame()
rowVendas = []
tabela_estoque = pd.DataFrame()
rowEstoque = []
tabela_produtos = pd.DataFrame()
rowProdutos = []
tabela_metodos = pd.DataFrame()
rowMetodos = []
tabelas = [tabela_estoque, tabela_vendas, tabela_produtos, tabela_metodos]

try:
    dict_df = pd.read_excel(path, sheet_name=['Produtos', 'Estoque', 'Vendas','Métodos'])
    tabela_vendas = dict_df.get('Vendas')
    tabela_produtos = dict_df.get('Produtos')
    tabela_estoque = dict_df.get('Estoque')
    tabela_metodos = dict_df.get('Métodos')
    print("Arquivo Encontrado\n\n")
    tabelas = [tabela_estoque, tabela_vendas, tabela_produtos, tabela_metodos]
    print("Estoque\n"+str(tabelas[0])+"\n\n\nVendas\n"+str(tabelas[1])+"\n\n\nProdutos\n"+str(tabelas[2])+"\n\n\nMétodos\n"+str(tabelas[3]))
except FileNotFoundError as fnfe:
    dV= {'Produto':[], 'Marca':[], 'Quantidade':[], 'Valor_Unitário':[], 'Valor_Total':[], 'Método_Venda':[], 'NumVenda':[]}
    dE= {'Produto':[], 'Marca':[], 'Quantidade':[], 'Valor_Venda':[], 'Valor_Compra':[],'Método':[]}
    dP= {'Produto':[], 'Marca':[], 'Método_Venda':[], 'Valor_Método':[], 'Método_Compra':[]}
    dM= {'Métodos':[]}
    tabela_vendas=pd.DataFrame(data=dV)
    tabela_estoque=pd.DataFrame(data=dE)
    tabela_produtos=pd.DataFrame(data=dP)
    tabela_metodos=pd.DataFrame(data=dM)
    print("Arquivo não lido, criando um dataframe substituto")
except ValueError as ve:
    print("Arquivo encontrado, porém sem todas sheets")
    tabelas = conferir(tabelas, path, 0)
    print(tabelas)
    tabela_estoque = tabelas[0]
    tabela_vendas = tabelas[1]
    tabela_produtos = tabelas[2]
    tabela_metodos = tabelas[3]

#Código
tabela_vendasProv = tabela_vendas
produtosAVender = []
valorTotalV = 0
produtosEstoque = listaProdutosV(tabela_estoque);
data_em_texto = date.today().strftime('%d/%m/%Y')

#Layout
def janelaInicial():
    sg.theme('Black')
    layout= [
        [sg.Image('Arquivos/Logo.png'), sg.Text(data_em_texto, font=(None, 20), justification='center', expand_x=True)],
        [sg.Button('Adicionar Produto', size=(25,1),button_color='#bee821',font=(None,20)),sg.Button('Vender Produto', size=(25,1),button_color='#bee821',font=(None,20))],
        [sg.Button('Histórico', size=(25,1),button_color='#bee821',font=(None,20)),sg.Button('Estatísticas', size=(25,1),button_color='#bee821',font=(None,20))],
        [sg.Button('Editar Produto', size=(25,1),button_color='#bee821',font=(None,20)),sg.Button('Estoque', size=(25,1),button_color='#bee821',font=(None,20))],
        [sg.Button('Sair', size=(25,1), font=(None,20), expand_x=True, button_color='#9853d1')]
    ]
    return sg.Window('LUME AGROPET', icon='Arquivos/icon.ico', layout=layout, finalize=True)

def janelaVender():
    sg.theme('DarkBlue')
    layout= [
        [sg.Text("Vender Produto")],
        [sg.Combo(produtosEstoque, key="tiposProdutos"), sg.Table(values=produtosAVender, headings=['Produto', 'Marca', 'Quant', 'ValorUn', 'ValorTotal'], size=(40, 15), key='tV_produtos')],
        [sg.Combo(metodosdeVenda,key="metodoVendacP")],
        [sg.InputText(key="QuantidadeItemVenda")],
        [sg.Text("Valor Total da Compra:", justification= 'right',expand_x=True)],
        [sg.Text(key='valorTotalV', justification='right',expand_x=True)],
        [sg.Button("+", key="ContinuarVenda"), sg.Button('Finalizar Venda',key="FinalizarVenda")]
    ]
    return sg.Window('Vender Produtos', layout=layout, finalize=True)

#Janela
janela1, janela2, janela3, janela4 = janelaInicial(), None, None, None

#Ler os eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    #Principal
    if janela == janela1:
        #Ir para janela Adicionar Produto
        if eventos == 'Adicionar Produto':
            tabelas = mainA(tabelas, path)
        # Ir para janela Vender Produto
        if eventos == 'Vender Produto':
            janela4 = janelaVender()
        # Fechar Programa
        if eventos == sg.WINDOW_CLOSED or eventos == 'Sair':
            break

    #Vender Produto
    if janela == janela4:
        #Vender
        if eventos == 'ContinuarVenda':
            current = valores['tiposProdutos']
            current2 = valores['metodoVendacP']
            if current in produtosEstoque:
                if current2 in metodosdeVenda:
                    try:
                        if int(valores['QuantidadeItemVenda']) >= 0:
                            quant = int(valores['QuantidadeItemVenda'])
                            provisorio = valores['tiposProdutos'].split(". ")
                            estoque = listaProdutosV1(tabela_vendas, tabela_estoque, provisorio[0], quant, valores['metodoVendacP'])
                            produtoAdicionado = [estoque[6], estoque[0], estoque[1], estoque[2]+' '+estoque[4], estoque[3] + " R$"]
                            produtosAVender.append(produtoAdicionado)
                            valorTotalV += float(estoque[4])
                            janela['tV_produtos'].Update(values=produtosAVender)
                            janela["valorTotalV"].Update(str(valorTotalV) + ' R$')
                            janela['QuantidadeItemVenda'].Update("")
                            janela['tiposProdutos'].Update("")
                            janela['metodoVendacP'].Update("")
                            tabela_vendas = Dtto_Excel(tabela_vendas,0)
                        else:
                            messagebox.showwarning("Erro ao Adicionar", 'Valor abaixo de 0 não é aceito')
                    except ValueError as ve:
                        messagebox.showwarning("Erro ao Adicionar", 'O campo Quantidade apenas aceita Números')
                else:
                    messagebox.showwarning("Erro ao Adicionar Produto", 'Não foi selecionado nenhum método de venda')
            else:
                messagebox.showwarning("Erro ao Adicionar Produto", 'Não foi selecionado nenhum produto a ser acrescentado')
        # Sair da janela Vender Produto e Voltar a Inicial
        if janela == janela4 and eventos == sg.WINDOW_CLOSED or eventos == 'FinalizarVenda':
            janela4.hide()

janela.close()