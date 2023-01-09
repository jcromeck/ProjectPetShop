import PySimpleGUI as sg
from tkinter import messagebox
from Funções import listaProdutos1, writerE

def janelaAdicionar(produtosCadastrados, estoqueP, valorP, produtosAdicionados):
    sg.theme('Black')
    layout11 = [
        [sg.Text('Estoque: ')],
        [sg.Text(estoqueP,expand_x=True, justification='center',key='estoqueTModificado'),
         sg.Input(key='estoqueModificado', size=(8, 2), visible=False)]
    ]
    layout12 = [
        [sg.Text('Valor: ')],
        [sg.Text(valorP, expand_x=True, justification='center', key='valorPTModificado'),
         sg.InputText(key='valorProdutoModificado', visible=False, size=(8, 2))]
    ]
    layout1 = [
        [sg.Column(layout11), sg.Column(layout12)]
    ]
    layoutA = [
        [sg.Text("Produto")],
        [sg.Combo(produtosCadastrados, size=(24,2),key="comboProdutos", readonly=True, enable_events=True),
         sg.ReadFormButton('',key='editarEstoque', button_color='#bee821', image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2, border_width=1)],
        [sg.Text("Quantidade: "),sg.InputText(key="quantidadeAdicionada",size=(3,3),expand_x=True)],
        [sg.ReadFormButton('',key='continuarCompra', button_color='#bee821', image_filename='Arquivos/Carrinho.png', image_size=(50, 50), image_subsample=1, border_width=1),
         sg.Column(layout1, key='ColunaAM')],
        [sg.Button('CadastrarProduto', key='CadastroProduto', button_color='#bee821', font=(None,15),expand_x=True)]
    ]
    layoutB = [
        [sg.Text('',expand_x=True,justification='Right'),
         sg.ReadFormButton('', key='excluirTBEstoque', button_color='red', image_filename='Arquivos/Excluir.png', image_size=(30, 30), image_subsample=2, border_width=1)],
        [sg.Table(values=produtosAdicionados, select_mode=sg.SELECT_MODE_BROWSE, headings=['Produto', 'Marca', 'Método', 'Quant', 'ValorUn', 'ValorTotal'], size=(40, 15), key='-TB-')]
    ]
    layoutC = [
        [sg.Text("Valor Total da Compra:", justification='right', expand_x=True)],
        [sg.Text('',key='valorTotal', justification='right', expand_x=True,text_color='Red')]
    ]
    layoutP = [
        [sg.Column(layoutA),
         sg.Column(layoutB)],
        [sg.Button('Concluir', font=(None, 15), expand_x=True, button_color='#9853d1'),
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
# Selecionar Produto
def SePr(tabelas, v, janela):
    provisorio = v['comboProdutos'].split("-")
    condicao = (tabelas[1]['Produto'] == provisorio[0]) & (tabelas[1]['Marca'] == provisorio[1]) & (
            tabelas[1]['Método_Compra'] == provisorio[2])
    condicao2 = (tabelas[6]['Produto'] == provisorio[0]) & (tabelas[6]['Marca'] == provisorio[1]) & (
            tabelas[6]['Método_Compra'] == provisorio[2])
    somaV = tabelas[1].loc[condicao, :]
    somaV = somaV['Valor_Compra'].sum()
    try:
        somaE = tabelas[6].loc[condicao2, :]
        estoqueP = somaE['Quantidade'].sum()
    except IndexError as ie:
        estoqueP = '0'
    valorP = somaV/len(tabelas[1].loc[condicao, :])
    janela['estoqueTModificado'].Update(estoqueP)
    janela['valorPTModificado'].Update(valorP)
    janela['estoqueModificado'].Update(estoqueP)
    janela['valorProdutoModificado'].Update(valorP)
    return estoqueP, valorP

def popC(tabelas, tabela_estoqueProv, v, j):
    prov = v['comboPopup'].split("-")
    cond = (tabela_estoqueProv['Produto'] == prov[0]) & (
            tabela_estoqueProv['Marca'] == prov[1]) & (
            tabela_estoqueProv['Método'] == prov[2])
    indic = tabela_estoqueProv.loc[cond, :].index[0]
    tabela_estoqueProv.at[indic, 'Quantidade'] -= v['propRet']
    prov = v['comboProdutos'].split("-")
    cond = (tabela_estoqueProv['Produto'] == prov[0]) & (
            tabela_estoqueProv['Marca'] == prov[1]) & (
                   tabela_estoqueProv['Método'] == prov[2])
    indic = tabela_estoqueProv.loc[cond, :].index[0]
    tabela_estoqueProv.at[indic, 'Quantidade'] += v['propAdic']
    estoqueP = tabelas[0].loc[indic, 'Quantidade']
    j['estoqueTModificado'].Update(estoqueP, visible=True)
    j['estoqueModificado'].Update(estoqueP, visible=False)
    return estoqueP, tabela_estoqueProv
# Carrinho Adicionar
def CarAd(t, v, j, p_ComprasProv, produtosCadastrados, produtosAdicionados, valorTotal, id):
    atual = v['comboProdutos']
    if atual in produtosCadastrados:
        if not v['quantidadeAdicionada'] == "":
            try:
                if int(v['quantidadeAdicionada']) >= 0:
                    quant = int(v['quantidadeAdicionada'])
                    provisorio = v['comboProdutos'].split("-")
                    condicao = (t[1]['Produto'] == provisorio[0]) & (t[1]['Marca'] == provisorio[1]) & (
                            t[1]['Método_Compra'] == provisorio[2])
                    indice = t[1].loc[condicao, :].index[0]
                    produto = listaProdutos1(t[1], indice, quant, 0)
                    produtoAdicionado = [produto[0], produto[1], produto[2], produto[3],
                                         produto[4] + " R$", produto[5] + " R$"]
                    produtosAdicionados.append(produtoAdicionado)
                    j["-TB-"].Update(values=produtosAdicionados)
                    valorTotal += float(produto[5])
                    j["valorTotal"].Update('-' + str(valorTotal) + ' R$')
                    j["quantidadeAdicionada"].Update("")
                    j["comboProdutos"].Update("")
                    p_ComprasP = listaProdutos1(t[1], indice, quant, id, 1)
                    new_row = {'ID': p_ComprasP[0],
                               'Produto': p_ComprasP[1],
                               'Marca': p_ComprasP[2],
                               'Método': p_ComprasP[3],
                               'Quantidade': p_ComprasP[4],
                               'Valor_Un': p_ComprasP[5],
                               'Valor_Total': p_ComprasP[6]}
                    p_ComprasProv = p_ComprasProv.append(new_row, ignore_index=True)
                    return produtosAdicionados, valorTotal, p_ComprasProv
                else:
                    messagebox.showwarning("Erro ao Adicionar",
                                           'Valor abaixo de 0 não é aceito')
                    return None, None, None
            except ValueError as ve:
                messagebox.showwarning("Erro ao Adicionar",
                                       'O campo Quantidade apenas aceita Números')
                return None, None, None
        else:
            messagebox.showwarning("Erro ao Adicionar",
                                   'Valor inválido no campo "Quantidade"')
            return None, None, None
    else:
        messagebox.showwarning("Erro ao Adicionar",
                               'Selecione um produto para adicionar')
        return None, None, None
# Editar Estoque
def EditE(tabelas, path, j, v, visInput, valorP, estoqueP):
    if visInput == False:  # ABRINDO INPUT
        j['estoqueTModificado'].Update(estoqueP, visible=False)
        j['estoqueModificado'].Update(estoqueP, visible=True)
        j['valorPTModificado'].Update(valorP, visible=False)
        j['valorProdutoModificado'].Update(valorP, visible=True)
        visInput = True
    else:  # ABRINDO TEXT
        estoqueP = int(v['estoqueModificado'])
        valorP = int(v['valorProdutoModificado'])
        provisorio = v['comboProdutos'].split("-")
        condicao = (tabelas[1]['Produto'] == provisorio[0]) & (tabelas[1]['Marca'] == provisorio[1]) & (
                    tabelas[1]['Método_Compra'] == provisorio[2])
        condicao2 = (tabelas[6]['Produto'] == provisorio[0]) & (tabelas[6]['Marca'] == provisorio[1]) & (
                    tabelas[6]['Método_Compra'] == provisorio[2]) & (tabelas[6]['Método_Venda'] == provisorio[2])
        indice = tabelas[1].loc[condicao, :]
        tabelas[1].at[indice, 'Valor_Compra'] = valorP
        try:
            if estoqueP != '0':
                indice2 = tabelas[6].loc[condicao2, :].index[0]
                tabelas[6].at[indice2, 'Quantidade'] = estoqueP
        except IndexError as ie:
            messagebox.showwarning("Erro ao Editar Estoque",
                                   'Produto nunca antes adicionado.\nPrecisa adicionar uma vez antes de editar seu estoque')
            estoqueP = '0'
        writerE(tabelas, path)
        j['estoqueTModificado'].Update(estoqueP, visible=True)
        j['estoqueModificado'].Update(estoqueP, visible=False)
        j['valorPTModificado'].Update(valorP, visible=True)
        j['valorProdutoModificado'].Update(valorP, visible=False)
        visInput = False
    return visInput, tabelas, valorP, estoqueP
# Excluir Linha Table
def ExC(t, produtosAdicionados, j, v, valorTotal, p_ComprasProv):
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
                condicao = (t[4]['Produto'] == data_selected[0][0]) & (t[4]['Marca'] == data_selected[0][1]) & (
                            t[4]['Método'] == data_selected[0][2]) & (t[4]['Quantidade'] == data_selected[0][3]) & (
                            t[4]['Valor_Un'] == data_selected[0][4]) & (t[4]['Valor_Total'] == data_selected[0][5])
                indice = t[4].loc[condicao, :].index[0]
                p_ComprasProv.drop(indice)
                produtosAdicionados.pop(row)
        j['-TB-'].Update(values=produtosAdicionados)
        xProv = data_selected[0][5].split(" ")
        valorTotal -= float(xProv[0])
        j["valorTotal"].Update('-' + str(valorTotal) + ' R$')
    return valorTotal, p_ComprasProv, produtosAdicionados
# Finalizar
def FinalizarAd(p_ComprasProv, tabelas, path, id, data):
    tabelas[4] = p_ComprasProv
    condicao = (str(tabelas[4]['ID']) == str(id))
    quant = tabelas[4].loc[condicao, :].sum()
    vT = tabelas[4].loc[condicao, 'Valor_Total'].sum()
    new_row = {'ID': id,
               'QItens': quant,
               'Data': data,
               'Valor_Total': vT}
    tabelas[4] = tabelas[4].append(new_row, ignore_index=True)
    writerE(tabelas, path)
    return tabelas
