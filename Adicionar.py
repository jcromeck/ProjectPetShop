import PySimpleGUI as sg
from tkinter import messagebox
from Funções import listaProdutos1, writerE, listaProdutos

def janelaAdicionar(tabelaP, produtosAdicionados):
    produtosCadastrados = listaProdutos(tabelaP, 0)
    estoqueP = ''
    valorP = ''
    sg.theme('Black')
    colunaV = [
        [sg.ReadFormButton('', key='voltarA', image_filename='Arquivos/Retornar.png', border_width=0,
                           image_subsample=1, image_size=(43, 43), button_color='black')],
        [sg.Text('', size=(0, 18))]
    ]
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
        [sg.Text('', size=(0,2))],
        [sg.Text("Produto")],
        [sg.Combo(produtosCadastrados, size=(40,2),key="comboProdutos", readonly=True, enable_events=True)],
        [sg.Text('')],
        [sg.Text("Quantidade: "),sg.InputText(key="quantidadeAdicionada",size=(3,3),expand_x=True)],
        [sg.Text('')],
        [sg.ReadFormButton('',key='continuarCompra', button_color='#bee821', image_filename='Arquivos/Carrinho.png', image_size=(35, 35), image_subsample=2, border_width=1),
         sg.Column(layout1, key='ColunaAM')],
        [sg.Text('')],
        [sg.Button('CadastrarProduto', key='CadastroProduto', button_color='#bee821', font=(None,15),expand_x=True)]
    ]
    layoutB = [
        [sg.Text('', size=(0,2))],
        [sg.Text('',expand_x=True,justification='Right'),
         sg.ReadFormButton('', key='excluirTBEstoque', button_color='red', image_filename='Arquivos/Excluir.png', image_size=(35, 35), image_subsample=2, border_width=1)],
        [sg.Table(values=produtosAdicionados, select_mode=sg.SELECT_MODE_BROWSE, headings=['Produto', 'Marca', 'Método', 'Quant', 'ValorUn', 'ValorTotal'], size=(40, 15), key='-TB-')]
    ]
    layoutC = [
        [sg.Text("Valor Total da Compra:", justification='right', expand_x=True)],
        [sg.Text('', key='valorTotal', justification='right', expand_x=True,text_color='Red')]
    ]
    layoutP = [
        [sg.Column(colunaV),
         sg.Column(layoutA),
         sg.Column(layoutB)],
        [sg.Button('Concluir', font=(None, 15), expand_x=True, button_color='#9853d1'),
         sg.Column(layoutC)]
    ]
    return sg.Window('Adicionar Produtos', icon='Arquivos/icon.ico', layout=layoutP, finalize=True)

# Selecionar Produto
def SePr(tabelas, v, janela):
    provisorio = v['comboProdutos'].split("-")
    condicao = (tabelas[1]['Produto'] == provisorio[0]) & (tabelas[1]['Marca'] == provisorio[1]) & (
            tabelas[1]['Método_Compra'] == provisorio[2])
    condicao2 = (tabelas[6]['Produto'] == provisorio[0]) & (tabelas[6]['Marca'] == provisorio[1]) & (
            tabelas[6]['Método'] == provisorio[2])
    somaV = tabelas[1].loc[condicao, :]
    somaV = somaV['Valor_Compra'].sum()
    try:
        somaE = tabelas[6].loc[condicao2, :]
        estoqueP = somaE['Quantidade'].sum()
    except IndexError as ie:
        estoqueP = '0'
    print(somaV)
    print(type(somaV))
    print(tabelas[1].loc[condicao, :])
    print(len(tabelas[1].loc[condicao, :]))
    valorP = int(somaV)/len(tabelas[1].loc[condicao, :])
    janela['estoqueTModificado'].Update(estoqueP)
    janela['valorPTModificado'].Update(valorP)
    janela['estoqueModificado'].Update(estoqueP)
    janela['valorProdutoModificado'].Update(valorP)

# Carrinho Adicionar
def CarAd(t, v, j, tP_CP, produtosAdicionados, valorTotal, id):
    tEP = t[6]
    tepp = 0
    n = 0
    quant = int(v['quantidadeAdicionada'])
    provisorio = v['comboProdutos'].split("-")
    condicao = (t[1]['Produto'] == provisorio[0]) & (t[1]['Marca'] == provisorio[1]) & \
               (t[1]['Método_Compra'] == provisorio[2])
    indice = t[1].loc[condicao, :].index[0]
    produto = listaProdutos1(t[1], indice, quant, None, 0)
    produtoAdicionado = [produto[0], produto[1], produto[2], produto[3], produto[4] + " R$", produto[5] + " R$"]
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
    for index, rows in t[6].iterrows():
        if p_ComprasP[1] == rows.Produto and p_ComprasP[2] == rows.Marca and p_ComprasP[3] == rows.Método:
            tepp = int(p_ComprasP[4]) + int(tEP.at[index, 'Quantidade'])
            n = index
            break
    tEP.at[n, 'Quantidade'] = tepp
    tP_CP = tP_CP.append(new_row, ignore_index=True)
    j['estoqueTModificado'].Update('')
    j['valorPTModificado'].Update('')
    return produtosAdicionados, valorTotal, tP_CP, tEP

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
                condicao = (p_ComprasProv['Produto'] == data_selected[0][0]) & (
                            p_ComprasProv['Marca'] == data_selected[0][1]) & (
                            p_ComprasProv['Método'] == data_selected[0][2]) & (
                            p_ComprasProv['Quantidade'] == data_selected[0][3]) & (
                            p_ComprasProv['Valor_Un']+str(' R$') == data_selected[0][4]) & (
                            p_ComprasProv['Valor_Total']+str(' R$') == data_selected[0][5])
                condicao2 = (t[6]['Produto'] == data_selected[0][0]) & (t[6]['Marca'] == data_selected[0][1]) & (
                            t[6]['Método'] == data_selected[0][2])
                indice = p_ComprasProv.loc[condicao, :].index[-1]
                indice2 = t[6].loc[condicao2, :].index[0]
                print(indice)
                quantAntes = t[6].at[indice2, 'Quantidade']
                print(quantAntes)
                quantSub = data_selected[0][3]
                t[6].at[indice2, 'Quantidade'] = int(quantAntes) - int(quantSub)
                p_ComprasProv = p_ComprasProv.drop(int(indice))
                produtosAdicionados.pop(row)
                break
        j['-TB-'].Update(values=produtosAdicionados)
        xProv = data_selected[0][5].split(" ")
        valorTotal -= float(xProv[0])
        j["valorTotal"].Update('-' + str(valorTotal) + ' R$')
    return valorTotal, p_ComprasProv, produtosAdicionados

# Finalizar
def FinalizarAd(tP_CP, tabelas, path, id, data, tEP):
    Qtotal = 0
    total = 0
    # Adicionar P_Compras
    tabelas[4] = tP_CP
    # Adicionar Estoque
    tabelas[6] = tEP
    condicao = tabelas[4]['ID'] == str(id)
    quant = tabelas[4].loc[condicao, 'Quantidade']
    for n in range(len(quant)):
        Qtotal += int(quant['Quantidade'][n])
        total += float(quant['Valor_Total'][n])
    # Adicionar Compras
    new_row = {'ID': id,
               'QItens': Qtotal,
               'Data': data,
               'Valor_Total': total}
    tabelas[5] = tabelas[5].append(new_row, ignore_index=True)
    writerE(tabelas, path)
    return tabelas
