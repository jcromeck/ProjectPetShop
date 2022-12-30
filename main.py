from tkinter import messagebox
import PySimpleGUI as sg
import pandas as pd
from Funções import listaMetodos, listaProdutos, listaProdutos1, conferir, listaProdutosV, listaProdutosV1
from datetime import date

def newRow(d, n, n1):
    if n == 0:
        rowVendas.append(d)
    if n == 1:
        rowEstoque.append(d)
    if n == 2:
        rowProdutos.append(d)
    if n == 3:
        rowMetodos.append(d)
    if n == 11:
        for row in range(len(rowEstoque)):
            tabela_compras.append(rowEstoque[row], ignore_index=True)
        with pd.ExcelWriter(path) as writer:
            tabela_produtos.to_excel(writer, sheet_name='Produtos', index=False)
            tabela_compras.to_excel(writer, sheet_name='Estoque', index=False)
            tabela_vendas.to_excel(writer, sheet_name='Vendas', index=False)
            tabela_metodos.to_excel(writer, sheet_name='Métodos', index=False)
        rowEstoque.clear()
    if n == 20:
        for row in range(len(rowEstoque)):
            if n1[0][0] == rowEstoque[row].get('Produto') and n1[0][1] == rowEstoque[row].get('Marca') and n1[0][2] == rowEstoque[row].get('Quantidade') and n1[0][3] == str(rowEstoque[row].get('Valor Unitário'))+' R$':
                rowEstoque.pop(row)



def Dtto_Excel(tabela, num):
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
        new_row = {'Produto': produto[0],
                    'Marca': produto[1],
                    'Quantidade': produto[2],
                    'Valor Unitário': produto[3]}
        newRow(new_row, 1, None)
        print('Estoque NovaLinha')
    #Produtos
    if num == 2:
        new_row = {'Produto': valores["Produto"],
                    'Marca': valores["MarcaProduto"],
                    'Método_Venda': valores["metodoVenda"],
                    'Método_Compra': valores["metodoCompra"],
                    'Valor_Método': valores["valorProduto"]}
        newRow(new_row, 2, None)
        print('Produtos NovaLinha')
    #Métodos
    if num == 3:
        new_row = {'Métodos': valores["novoMetodoVendaInput"]}
        newRow(new_row,3,None)
        print('Métodos NovaLinha')


#CodigoPandas
path = "Arquivos/Compras.xlsx"
tabela_vendas= pd.DataFrame()
tabela_compras=pd.DataFrame()
tabela_produtos=pd.DataFrame()
tabela_metodos=pd.DataFrame()
tabelas=[tabela_compras,tabela_vendas,tabela_produtos,tabela_metodos]
rowEstoque=[]
rowMetodos=[]
rowProdutos=[]
rowVendas=[]

try:
    dict_df = pd.read_excel(path, sheet_name=['Produtos', 'Estoque', 'Vendas','Métodos'])
    tabela_vendas = dict_df.get('Vendas')
    tabela_produtos =dict_df.get('Produtos')
    tabela_compras = dict_df.get('Estoque')
    tabela_metodos = dict_df.get('Métodos')
    print("Arquivo Encontrado\n\n")
    tabelas = [tabela_compras, tabela_vendas, tabela_produtos, tabela_metodos]
    print("Estoque\n"+str(tabelas[0])+"\n\n\nVendas\n"+str(tabelas[1])+"\n\n\nProdutos\n"+str(tabelas[2])+"\n\n\nMétodos\n"+str(tabelas[3]))
except FileNotFoundError as fnfe:
    dV= {'Produto':[], 'Marca':[], 'Quantidade':[], 'Valor_Unitário':[], 'Valor_Total':[], 'Método_Venda':[], 'NumVenda':[]}
    dC= {'Produto':[], 'Marca':[], 'Quantidade':[], 'Valor_Venda':[], 'Valor_Compra':[],'Método':[]}
    dP= {'Produto':[], 'Marca':[], 'Método_Venda':[], 'Valor_Método':[], 'Método_Compra':[]}
    dM= {'Produto':[], 'Métodos':[]}
    tabela_vendas=pd.DataFrame(data=dV)
    tabela_compras=pd.DataFrame(data=dC)
    tabela_produtos=pd.DataFrame(data=dP)
    tabela_metodos=pd.DataFrame(data=dM)
    print("Arquivo não lido, criando um dataframe substituto")
except ValueError as ve:
    print("Arquivo encontrado, porém sem todas sheets")
    conferir(tabelas, path, 0)

#Código
metodosdeVenda = listaMetodos(tabela_metodos)
produtosAdicionados = []
produtosAVender = []
valorTotal = 0
valorTotalV = 0
produtosEstoque= listaProdutosV(tabela_compras)
produtosCadastrados= listaProdutos(tabela_produtos)
data_em_texto = date.today().strftime('%d/%m/%Y')
estoqueAdicionar = sg.Text('5',expand_x=True,justification='center',background_color='Black')
valorPAdicionar = sg.Text('1',expand_x=True,justification='center',background_color='Black')

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
    sg.theme('Black')
    layout1= [
        [sg.Text('Estoque: '),sg.Text('Valor: ')],
        [estoqueAdicionar, valorPAdicionar]
    ]
    layoutA= [
        [sg.Text("Produto")],
        [sg.Combo(produtosCadastrados, size=(15,100),key="comboProdutos", readonly=True),sg.ReadFormButton('',key='editarEstoque', button_color='#bee821', image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2, border_width=1)],
        [sg.Text("Quantidade: "),sg.InputText(key="quantidadeAdicionada",size=(3,3),expand_x=True)],
        [sg.ReadFormButton('',key='continuarCompra', button_color='#bee821', image_filename='Arquivos/Carrinho.png', image_size=(50, 50), image_subsample=1, border_width=1),
        sg.Column(layout1)],
        [sg.Button('CadastrarProduto', key='CadastroProduto', button_color='#bee821', font=(None,15),expand_x=True)]
    ]
    layoutB= [
        [sg.Text('',expand_x=True,justification='Right'),
         sg.ReadFormButton('',key='editarTBEstoque', button_color='#bee821', image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2, border_width=1),
         sg.ReadFormButton('',key='excluirTBEstoque', button_color='#9853d1', image_filename='Arquivos/Excluir.png', image_size=(30, 30), image_subsample=2, border_width=1)],
        [sg.Table(values=produtosAdicionados, select_mode= sg.TABLE_SELECT_MODE_BROWSE, headings=['Produto','Marca','Quant','ValorUn','ValorTotal'],size=(40,15), enable_events=True, key='-TB-')]
    ]
    layoutC= [
        [sg.Text("Valor Total da Compra:", justification='right', expand_x=True)],
        [sg.Text('',key='valorTotal', justification='right', expand_x=True,text_color='Red')]
    ]
    layoutP=[
        [sg.Column(layoutA),
         sg.Column(layoutB)],
        [sg.Button('Concluir', font=(None,15), expand_x=True, button_color='#9853d1'),
        sg.Column(layoutC)]
    ]
    return sg.Window('Adicionar Produtos', layout= layoutP, finalize=True)

def janelaVender():
    sg.theme('DarkBlue')
    layout= [
        [sg.Text("Vender Produto")],
        [sg.Combo(produtosEstoque, key="tiposProdutos"), sg.Table(values=produtosAVender, headings=['Produto', 'Marca', 'Quant', 'ValorUn', 'ValorTotal'], size=(40, 15), key=('tV_produtos'))],
        [sg.Combo(metodosdeVenda,key="metodoVendacP")],
        [sg.InputText(key="QuantidadeItemVenda")],
        [sg.Text("Valor Total da Compra:", justification= 'right',expand_x=True)],
        [sg.Text(key='valorTotalV', justification='right',expand_x=True)],
        [sg.Button("+", key="ContinuarVenda"), sg.Button('Finalizar Venda',key="FinalizarVenda")]
    ]
    return sg.Window('Vender Produtos', layout=layout, finalize=True)

#Janela
janela1, janela2, janela3, janela4= janelaInicial(), None, None, None

#Ler os eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    #Adicionar
    if janela == janela2:
        #Excluir Produto
        if eventos == 'excluirTBEstoque':
            data_selected = [produtosAdicionados[row] for row in valores['-TB-']]
            print(data_selected)
            newRow(None, 20, data_selected)
            for row in valores['-TB-']:
                produtosAdicionados.pop(row)
            janela['-TB-'].Update(values=produtosAdicionados)
        #Finalizar Compra
        newRow(None,11,None)
        #Comprar Produto
        if eventos == 'continuarCompra':
            atual = valores['comboProdutos']
            if atual in produtosCadastrados:
                if not valores['quantidadeAdicionada'] == "":
                    try:
                        if int(valores['quantidadeAdicionada']) >= 0:
                            quant = int(valores['quantidadeAdicionada'])
                            provisorio = valores['comboProdutos'].split(". ")
                            produto = listaProdutos1(tabela_produtos, provisorio[0], quant)
                            produtoAdicionado=[produto[0], produto[1], produto[2], produto[3]+" R$", produto[4]+" R$"]
                            produtosAdicionados.append(produtoAdicionado)
                            valorTotal += float(produto[4])
                            janela["-TB-"].Update(values=produtosAdicionados)
                            janela["valorTotal"].Update('-'+str(valorTotal)+' R$')
                            janela["quantidadeAdicionada"].Update("")
                            janela["comboProdutos"].Update("")
                            tabela_compras = Dtto_Excel(tabela_compras, 1)
                        else:
                            messagebox.showwarning("Erro ao Adicionar", 'Valor abaixo de 0 não é aceito')
                    except ValueError as ve:
                        messagebox.showwarning("Erro ao Adicionar", 'O campo Quantidade apenas aceita Números')
                else:
                    messagebox.showwarning("Erro ao Adicionar", 'Valor inválido no campo "Quantidade"')
            else:
                messagebox.showwarning("Erro ao Adicionar", 'Selecione um produto para adicionar')

    #Vender Produto
    if janela == janela4 and eventos == 'ContinuarVenda':
        current = valores['tiposProdutos']
        current2 = valores['metodoVendacP']
        if current in produtosEstoque:
            if current2 in metodosdeVenda:
                try:
                    if int(valores['QuantidadeItemVenda']) >= 0:
                        quant = int(valores['QuantidadeItemVenda'])
                        provisorio = valores['tiposProdutos'].split(". ")
                        estoque = listaProdutosV1(tabela_vendas, tabela_compras, provisorio[0], quant, valores['metodoVendacP'])
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

    # Ir para janela Cadastrar Produto
    if janela == janela2 and eventos == 'CadastroProduto':
        janela3 = janelaCadastro()
        janela2.hide()

    # Mudar Visibilidade Metodo Venda
    if janela == janela3 and eventos == 'buttonMetodoVenda':
        janela["novoMetodoVendaInput"].Update(visible=True)
        janela["novoMetodoVenda"].Update(visible=True)

    # Confirmar novo Método de Venda
    if janela == janela3 and eventos == 'novoMetodoVenda' and not valores['novoMetodoVendaInput'] == '':
        metodosdeVenda.append(valores['novoMetodoVendaInput'])
        tabela_metodos = Dtto_Excel(tabela_metodos, 3)
        valores["novoMetodoVendaInput"] = ""
        janela["novoMetodoVendaInput"].Update(visible=False)
        janela["novoMetodoVenda"].Update(visible=False)
        janela['metodoVenda'].Update(values=metodosdeVenda)
        janela['metodoCompra'].Update(values=metodosdeVenda)

    # Adicionar Produto Cadastro
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
                        tabela_produtos = Dtto_Excel(tabela_produtos, 2)
                        janela3.hide()
                        produtosCadastrados = listaProdutos(tabela_produtos)
                        janela2['comboProdutos'].Update(values=produtosCadastrados)
                        janela2.un_hide()
                    except ValueError as ve:
                        messagebox.showwarning("Erro ao Cadastrar", 'O campo Valor do Produto apenas aceita Números \n'+str(ve))
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
        if janela2 != None:
            janela2.un_hide()
        else:
            janela2 = janelaAdicionar()
        janela2['comboProdutos'].Update(values = produtosCadastrados)
        produtosAdicionados.clear()
        janela2["-TB-"].Update(produtosAdicionados)
        janela1.hide()

    #Ir para janela Vender Produto
    if janela == janela1 and eventos == 'Vender Produto':
        janela4 = janelaVender()
        janela1.hide()
        #janela4['tiposProdutos'].Update(values = )

    # Sair da janela Vender Produto e Voltar a Inicial
    if janela == janela4 and eventos == sg.WINDOW_CLOSED or eventos == 'FinalizarVenda':
            janela4.hide()
            janela1.un_hide()

    #Sair da janela Adicionar Produto e Voltar a Inicial
    if janela == janela2 and eventos == sg.WINDOW_CLOSED or eventos == 'Finalizar':
        janela2.hide()
        janela1.un_hide()

    #Fechar Programa
    if janela == janela1 and eventos == sg.WINDOW_CLOSED or eventos == 'Sair':

        break
janela.close()