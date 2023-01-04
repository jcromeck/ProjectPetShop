import PySimpleGUI as sg
from tkinter import messagebox
from Funções import listaProdutos, listaProdutos1, writerE
from Cadastrar import mainC

def janelaAdicionar(produtosCadastrados, estoqueP, valorP, produtosAdicionados):
    sg.theme('Black')
    layout11 = [
        [sg.Text('Estoque: ')],
        [sg.Text(estoqueP,expand_x=True, justification='center',key='estoqueTModificado'),
         sg.Input(key='estoqueModificado', size=(8, 2), visible=False)]
    ]
    layout12 = [
        [sg.Text('Valor: ')],
        [sg.Text(valorP,expand_x=True, justification='center', key='valorPTModificado')
        ,sg.InputText(key='valorProdutoModificado', visible=False, size=(8,2))]
    ]
    layout1 = [
        [sg.Column(layout11),sg.Column(layout12)]
    ]
    layoutA = [
        [sg.Text("Produto")],
        [sg.Combo(produtosCadastrados, size=(24,2),key="comboProdutos", readonly=True, enable_events=True),sg.ReadFormButton('',key='editarEstoque', button_color='#bee821', image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2, border_width=1)],
        [sg.Text("Quantidade: "),sg.InputText(key="quantidadeAdicionada",size=(3,3),expand_x=True)],
        [sg.ReadFormButton('',key='continuarCompra', button_color='#bee821', image_filename='Arquivos/Carrinho.png', image_size=(50, 50), image_subsample=1, border_width=1),
        sg.Column(layout1, key='ColunaAM')],
        [sg.Button('CadastrarProduto', key='CadastroProduto', button_color='#bee821', font=(None,15),expand_x=True)]
    ]
    layoutB = [
        [sg.Text('',expand_x=True,justification='Right'),
         sg.ReadFormButton('',key='editarTBEstoque', button_color='#bee821', image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2, border_width=1),
         sg.ReadFormButton('',key='excluirTBEstoque', button_color='#9853d1', image_filename='Arquivos/Excluir.png', image_size=(30, 30), image_subsample=2, border_width=1)],
        [sg.Table(values=produtosAdicionados, select_mode=sg.SELECT_MODE_BROWSE, headings=['Produto', 'Marca', 'Método', 'Quant', 'ValorUn', 'ValorTotal'],size=(40,15), key='-TB-')]
    ]
    layoutC = [
        [sg.Text("Valor Total da Compra:", justification='right', expand_x=True)],
        [sg.Text('',key='valorTotal', justification='right', expand_x=True,text_color='Red')]
    ]
    layoutP = [
        [sg.Column(layoutA),
         sg.Column(layoutB)],
        [sg.Button('Concluir', font=(None,15), expand_x=True, button_color='#9853d1'),
        sg.Column(layoutC)]
    ]
    return sg.Window('Adicionar Produtos', layout=layoutP, finalize=True)

def popupRepor(produtosCadastrados):
    layout = [
        [sg.Text('Selecione o Item retirado')],
        [sg.Combo(produtosCadastrados, key='comboPopup', size=(20, 1))],
        [sg.Text('Agora Selecione a proporção')],
        [sg.Text('Selecione a quantidade retirada'), sg.Input(key='propRet')],
        [sg.Text('Selecione a quantidade adicionada'), sg.Input(key='propAdic')],
        [sg.Button('Ok', key='concluirPopup')]
    ]
    return sg.Window('Item com Reposição a partir de outro item', layout)

def mainA(tabelas, path):
    estoqueP = ''
    valorP = ''
    valorTotal = 0
    visInput = False
    produtosAdicionados = []
    produtosCadastrados = listaProdutos(tabelas[2])
    janela = janelaAdicionar(produtosCadastrados, estoqueP, valorP, produtosAdicionados)
    tabela_estoqueProv = tabelas[0]
    while True:
        j, e, v = janela.read()

        #Carrinho
        if e == 'continuarCompra':
            atual = v['comboProdutos']
            numProv = 0
            if atual in produtosCadastrados:
                if not v['quantidadeAdicionada'] == "":
                    try:
                        if int(v['quantidadeAdicionada']) >= 0:
                            quant = int(v['quantidadeAdicionada'])
                            provisorio = v['comboProdutos'].split("-")
                            condicao = (tabelas[1]['Produto'] == provisorio[0]) & (
                                    tabelas[1]['Marca'] == provisorio[1]) & (
                                               tabelas[1]['Método'] == provisorio[2])
                            indice = tabelas[1].loc[condicao, :].index[0]
                            if tabelas[1]['ReporEstoquepProd'][indice] == 'Sim':
                                janPop = popupRepor(produtosCadastrados)
                                while True:
                                    jan, event, val = janPop.read()
                                    if e == 'concluirPopup':
                                        prov = v['comboPopup'].split("-")
                                        cond = (tabela_estoqueProv['Produto'] == prov[0]) & (
                                                tabela_estoqueProv['Marca'] == prov[1]) & (
                                                tabela_estoqueProv['Método'] == prov[2])
                                        indic = tabela_estoqueProv.loc[cond, :].index[0]
                                        tabela_estoqueProv.at[indic, 'Quantidade'] -= v['propRet']
                                        prov = v['comboProdutos'].split("-")
                                        cond = (tabela_estoqueProv['Produto'] == provisorio[0]) & (
                                                tabela_estoqueProv['Marca'] == provisorio[1]) & (
                                                tabela_estoqueProv['Método'] == provisorio[2])
                                        indic = tabela_estoqueProv.loc[cond, :].index[0]
                                        tabela_estoqueProv.at[indic, 'Quantidade'] += v['propAdic']
                                        estoqueP = tabelas[0].loc[indic, 'Quantidade']
                                        j['estoqueTModificado'].Update(estoqueP, visible=True)
                                        j['estoqueModificado'].Update(estoqueP, visible=False)
                                        jan.close()
                                        break
                            produto = listaProdutos1(tabelas[2], provisorio[0], quant, 0)
                            produtoAdicionado = [produto[0], produto[1], produto[2], produto[3],
                                                 produto[4] + " R$", produto[5] + " R$"]
                            produtosAdicionados.append(produtoAdicionado)
                            j["-TB-"].Update(values=produtosAdicionados)
                            valorTotal += float(produto[5])
                            j["valorTotal"].Update('-' + str(valorTotal) + ' R$')
                            j["quantidadeAdicionada"].Update("")
                            j["comboProdutos"].Update("")
                            quant = int(v['quantidadeAdicionada'])
                            provisorio = v['comboProdutos'].split(". ")
                            produtosProv = listaProdutos1(tabelas[1], provisorio[0], quant, 1)
                            new_row = {'Produto': produtosProv[0],
                                       'Marca': produtosProv[1],
                                       'Método': produtosProv[2],
                                       'Quantidade': produtosProv[3],
                                       'Valor_Venda': produtosProv[4],
                                       'Valor_Compra': produtosProv[5]}
                            tabela_estoqueProv = tabelas[0].append(new_row, ignore_index=True)
                        else:
                            messagebox.showwarning("Erro ao Adicionar", 'Valor abaixo de 0 não é aceito')
                    except ValueError as ve:
                        messagebox.showwarning("Erro ao Adicionar", 'O campo Quantidade apenas aceita Números')
                else:
                    messagebox.showwarning("Erro ao Adicionar", 'Valor inválido no campo "Quantidade"')
            else:
                messagebox.showwarning("Erro ao Adicionar", 'Selecione um produto para adicionar')

        # Atualizar Estoque e Valor
        if e == 'comboProdutos':
            provisorio = v['comboProdutos'].split("-")
            condicao = (tabelas[2]['Produto'] == provisorio[0]) & (
                        tabelas[2]['Marca'] == provisorio[1])
            condicao2 = (tabelas[0]['Produto'] == provisorio[0]) & (
                        tabelas[0]['Marca'] == provisorio[1])
            indice = tabelas[2].loc[condicao, :].index[0]
            try:
                indice2 = tabelas[0].loc[condicao2, :].index[0]
                estoqueP = tabelas[0].loc[indice2, 'Quantidade']
            except IndexError as ie:
                estoqueP = '0'
            valorP = tabelas[2].loc[indice, 'Valor_Compra']
            janela['estoqueTModificado'].Update(estoqueP)
            janela['valorPTModificado'].Update(valorP)
            janela['estoqueModificado'].Update(estoqueP)
            janela['valorProdutoModificado'].Update(valorP)

        # Editar
        if e == 'editarEstoque':
            if visInput == False:  # ABRINDO INPUT
                janela['estoqueTModificado'].Update(estoqueP, visible=False)
                janela['estoqueModificado'].Update(estoqueP, visible=True)
                janela['valorPTModificado'].Update(valorP, visible=False)
                janela['valorProdutoModificado'].Update(valorP, visible=True)
                visInput = True
            else:  # ABRINDO TEXT
                estoqueP = v['estoqueModificado']
                provisorio = v['comboProdutos'].split("-")
                condicao = (tabelas[2]['Produto'] == provisorio[0]) & (
                            tabelas[2]['Marca'] == provisorio[1])
                condicao2 = (tabelas[0]['Produto'] == provisorio[0]) & (
                            tabelas[0]['Marca'] == provisorio[1])
                indice = tabelas[2].loc[condicao, :].index[0]
                tabelas[2].at[indice, 'Valor_Compra'] = v['valorProdutoModificado']
                try:
                    if estoqueP != '0':
                        indice2 = tabelas[0].loc[condicao2, :].index[0]
                        tabelas[0].at[indice2, 'Quantidade'] = v['valorProdutoModificado']
                except IndexError as ie:
                    messagebox.showwarning("Erro ao Editar Estoque",
                                           'Produto nunca antes adicionado, precisa adicionar uma vez antes de editar seu estoque')
                    estoqueP = '0'
                writerE(tabelas, path)
                valorP = v['valorProdutoModificado']
                janela['estoqueTModificado'].Update(estoqueP, visible=True)
                janela['estoqueModificado'].Update(estoqueP, visible=False)
                janela['valorPTModificado'].Update(valorP, visible=True)
                janela['valorProdutoModificado'].Update(valorP, visible=False)
                visInput = False

        #Cadastro
        if e == 'CadastroProduto':
            tabelas = mainC(tabelas, path)
            produtosCadastrados = listaProdutos(tabelas[2])
            j['comboProdutos'].Update(values=produtosCadastrados)

        # Excluir Produto
        if e == 'excluirTBEstoque':
            data_selected = [produtosAdicionados[row] for row in v['-TB-']]
            if data_selected == []:
                messagebox.showwarning("Impossível Deletar Dado",
                                       'Precisa Selecionar o Dado na Tabela antes de Deletar')
            else:
                for row in range(len(produtosAdicionados)):
                    if produtosAdicionados[row][0] == data_selected[0][0] and \
                       produtosAdicionados[row][1] == data_selected[0][1] and \
                       produtosAdicionados[row][2] == data_selected[0][2] and \
                       produtosAdicionados[row][3] == data_selected[0][3] and \
                       produtosAdicionados[row][4] == data_selected[0][4] and \
                       produtosAdicionados[row][5] == data_selected[0][5]:
                        tabela_estoqueProv.drop(row)
                        produtosAdicionados.pop(row)
                j['-TB-'].Update(values=produtosAdicionados)
                xProv = data_selected[0][5].split(" ")
                valorTotal -= float(xProv[0])
                j["valorTotal"].Update('-' + str(valorTotal) + ' R$')

        #Fechar Janela
        if e == sg.WINDOW_CLOSED:
            break
    janela.close()
    tabelas1 = tabelas
    return tabelas1
