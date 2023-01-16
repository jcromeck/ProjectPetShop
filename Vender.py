import PySimpleGUI as sg
from tkinter import messagebox
from Funções import listaProdutosV, listaMetodos, listaProdutosV1, writerE

def janelaVender(produtosEstoque, produtosAVender, estoqueP, valorP):
    sg.theme('Black')
    colunaV = [
        [sg.ReadFormButton('', key='voltarV', image_filename='Arquivos/Retornar.png', border_width=0,
                           image_subsample=1,
                           image_size=(43, 43), button_color='black'), sg.Text('', expand_x=True)],
        [sg.Text('', size=(0, 18))]
    ]
    layoutC1 = [
        [sg.Text('Estoque: ')],
        [sg.Text(estoqueP, expand_x=True, justification='center', key='estoqueTVModificado'),
         sg.Input(key='estoqueVModificado', size=(8, 2), visible=False)]
    ]
    layoutC2 = [
        [sg.Text('Valor: ')],
        [sg.Text(valorP, expand_x=True, justification='center', key='valorPTVModificado'),
         sg.InputText(key='valorProdutoVModificado', visible=False, size=(8, 2))]
    ]
    layoutC = [
        [sg.Column(layoutC1), sg.Column(layoutC2)]
    ]
    layout1 = [
        [sg.Text("")],
        [sg.Text("Produto")],
        [sg.Combo(produtosEstoque, key="tiposProdutos", readonly=True, enable_events=True)],
        [sg.Text("")],
        [sg.Text("Quantidade"), sg.InputText(key="quantidadeAdicionadaV", size=(3, 3), expand_x=True)],
        [sg.Text("")],
        [sg.ReadFormButton('', key='continuarVCompra', button_color='#bee821', image_filename='Arquivos/Carrinho.png',
                           image_size=(50, 50), image_subsample=1, border_width=1), sg.Column(layoutC)],
        [sg.Text("")],
        [sg.Button('Finalizar Venda', key="FinalizarVenda", font=(None,15), button_color='#9853d1')]
    ]
    layout2 = [
        [sg.Text('', expand_x=True, justification='Right'),
        sg.ReadFormButton('', key='excluirTBEstoqueV', button_color='red', image_filename='Arquivos/Excluir.png',
                          image_size=(30, 30), image_subsample=2, border_width=1)],
        [sg.Table(values=produtosAVender, headings=['Produto', 'Marca', 'Método', 'Quant', 'ValorUn', 'ValorTotal'],
                  size=(40, 15), key='tV_produtos')],
        [sg.Text("Valor Total da Compra:", justification='right', expand_x=True)],
        [sg.Text(key='valorTotalV', text_color='green', justification='right', expand_x=True)],
    ]
    layout = [
        [sg.Column(colunaV), sg.Column(layout1), sg.Column(layout2)]
    ]
    return sg.Window('Vender Produtos', icon='Arquivos/icon.ico', layout=layout, finalize=True)

# Carrinho
def CarVenda(t, v, pE, j, pAV, vTV, tPVP, id, tEP):
    atual = v['tiposProdutos']
    if atual in pE:
        if not v['quantidadeAdicionadaV'] == "":
            try:
                if int(v['quantidadeAdicionadaV']) >= 0:
                    quant = int(v['quantidadeAdicionadaV'])
                    provisorio = v['tiposProdutos'].split("-")
                    condicao = (t[1]['Produto'] == provisorio[0]) & (t[1]['Marca'] == provisorio[1]) & (
                            t[1]['Método_Venda'] == provisorio[2])
                    indice = t[1].loc[condicao, :].index[0]
                    produto = listaProdutosV1(t[1], indice, quant, id)
                    produtoAdicionado = [produto[1], produto[2], produto[3], produto[4],
                                         produto[5] + " R$", produto[6] + " R$"]
                    pAV.append(produtoAdicionado)
                    j['tV_produtos'].Update(values=pAV)
                    vTV += float(produto[6])
                    j["valorTotalV"].Update('+' + str(vTV) + ' R$')
                    j["quantidadeAdicionadaV"].Update("")
                    j["tiposProdutos"].Update("")
                    produtosProv = produto
                    #P_Vendas
                    new_row = {'ID': produtosProv[0],
                               'Produto': produtosProv[1],
                               'Marca': produtosProv[2],
                               'Método': produtosProv[3],
                               'Quantidade': produtosProv[4],
                               'Valor_Un': produtosProv[5],
                               'Valor_Total': produtosProv[6]}
                    for index, rows in t[6].iterrows():
                        if produtosProv[1] == rows.Produto and produtosProv[2] == rows.Marca and produtosProv[
                            3] == rows.Método:
                            tepp = int(tEP.at[index, 'Quantidade']) - int(produtosProv[4])
                    tEP.at[index, 'Quantidade'] = tepp
                    tPVP = tPVP.append(new_row, ignore_index=True)
                    j['estoqueTVModificado'].Update('')
                    j['valorPTVModificado'].Update('')
                    return vTV, tPVP, pAV, tEP
                else:
                    messagebox.showwarning("Erro ao Adicionar",
                                           'Valor abaixo de 0 não é aceito')
                    return vTV, tPVP, pAV, tEP
            except ValueError as ve:
                messagebox.showwarning("Erro ao Adicionar",
                                       'O campo Quantidade apenas aceita Números')
                return vTV, tPVP, pAV, tEP
        else:
            messagebox.showwarning("Erro ao Adicionar",
                                   'Valor inválido no campo "Quantidade"')
            return vTV, tPVP, pAV, tEP
    else:
        messagebox.showwarning("Erro ao Adicionar",
                               'Selecione um produto para adicionar')
        return vTV, tPVP, pAV, tEP

# Selecionar Combo
def SePrV(tabelas, v, janela):
    provisorio = v['tiposProdutos'].split("-")
    condicao = (tabelas[1]['Produto'] == provisorio[0]) & (tabelas[1]['Marca'] == provisorio[1]) & (
            tabelas[1]['Método_Venda'] == provisorio[2])
    condicao2 = (tabelas[6]['Produto'] == provisorio[0]) & (tabelas[6]['Marca'] == provisorio[1]) & (
            tabelas[6]['Método'] == provisorio[2])
    somaV = tabelas[1].loc[condicao, :]
    somaV = somaV['Valor_Venda'].sum()
    try:
        somaE = tabelas[6].loc[condicao2, :]
        estoqueP = somaE['Quantidade'].sum()
    except IndexError as ie:
        estoqueP = '0'
    valorP = somaV/len(tabelas[1].loc[condicao, :])
    janela['estoqueTVModificado'].Update(estoqueP)
    janela['valorPTVModificado'].Update(valorP)
    janela['estoqueVModificado'].Update(estoqueP)
    janela['valorProdutoVModificado'].Update(valorP)
    return estoqueP, valorP

# Excluir Elemento Table
def ExcV(t, pAV, j, v, vTV, tPVP):
    data_selected = [pAV[row] for row in v['tV_produtos']]
    if data_selected == []:
        messagebox.showwarning("Impossível Deletar Dado",
                               'Precisa Selecionar o Dado na Tabela antes de Deletar')
    else:
        for row in range(len(pAV)):
            if pAV[row][0] == data_selected[0][0] and pAV[row][1] == data_selected[0][1] and \
               pAV[row][2] == data_selected[0][2] and pAV[row][3] == data_selected[0][3] and \
               pAV[row][4] == data_selected[0][4] and pAV[row][5] == data_selected[0][5]:
                condicao = (tPVP['Produto'] == data_selected[0][0]) & (tPVP['Marca'] == data_selected[0][1]) & (
                            tPVP['Método'] == data_selected[0][2]) & (tPVP['Quantidade'] == data_selected[0][3]) & (
                            tPVP['Valor_Un'] + str(' R$') == data_selected[0][4]) & (
                            tPVP['Valor_Total'] + str(' R$') == data_selected[0][5])
                condicao2 = (t[6]['Produto'] == data_selected[0][0]) & (t[6]['Marca'] == data_selected[0][1]) & (
                        t[6]['Método'] == data_selected[0][2])
                indice = tPVP.loc[condicao, :].index[-1]
                indice2 = t[6].loc[condicao2, :].index[0]
                quantAntes = t[6].at[indice2, 'Quantidade']
                quantAdd = data_selected[0][3]
                t[6].at[indice2, 'Quantidade'] = int(quantAntes) + int(quantAdd)
                tPVP = tPVP.drop(int(indice))
                pAV.pop(row)
                break
        j['tV_produtos'].Update(values=pAV)
        xProv = data_selected[0][5].split(" ")
        vTV -= float(xProv[0])
        j["valorTotalV"].Update('+' + str(vTV) + ' R$')
    return vTV, tPVP, pAV

def janelaVender2(valorTotalVenda):
    colunaV = [
        [sg.ReadFormButton('', key='voltarV2', image_filename='Arquivos/Retornar.png', border_width=0,
                           image_subsample=1,
                           image_size=(43, 43), button_color='black'), sg.Text('', expand_x=True)],
        [sg.Text('', size=(0, 12))]
    ]
    coluna1 = [
        [sg.Text('', size=(30, 1), justification='Right')],
        [sg.Text('Valor Total: '), sg.Text(valorTotalVenda, text_color='green', key='vTV')],
        [sg.Text('', expand_x=True, justification='Right')],
        [sg.Text('Desconto: '), sg.InputText(key='desconto', enable_events=True, size=(10, 1))],
        [sg.Checkbox('Frete', key='frete', enable_events=False)],
        [sg.Text('', expand_x=True, justification='Right')],
        [sg.Text('Valor Descontado: '), sg.Text(0.0, key='valorD', text_color='red')],
        [sg.Text('Valor Total com Desconto: '), sg.Text(valorTotalVenda, key='valorTcD', text_color='green')]
    ]
    coluna2 = [
        [sg.Text('Método de Pagamento: ')],
        [sg.Combo(['Pix', 'Cartão de Crédito', 'Cartão de Débito', 'Dinheiro'], key='comboPag', readonly=True)],
        [sg.Text('Comentários: ')],
        [sg.Multiline('', key='mT', no_scrollbar=True, size=(30, 7))]
    ]
    layoutP = [
        [sg.Column(colunaV), sg.Column(coluna1), sg.Column(coluna2)],
        [sg.Button('Concluir', key='concluirV', expand_x=True, button_color='#9853d1')]
    ]
    return sg.Window('Finalizar Venda', layout=layoutP, finalize=True)

def AtualizarDesconto(v, j, vTV):
    try:
        if v['desconto'] != '':
            desconto = int(v['desconto'])
        else:
            desconto = 0
        if desconto < 0:
            messagebox.showwarning("Erro no campo Desconto",
                               'Apenas é aceito números positivos')
            j['desconto'].Update('')
        j['valorD'].Update(desconto)
        vTD = float(vTV) - float(desconto)
        j['valorTcD'].Update(str(vTD))
        return vTD
    except (TypeError, ValueError) as te:
        messagebox.showwarning("Erro no campo Desconto",
                               'Apenas é aceito números no campo Desconto')
        j['desconto'].Update('')
        j['valorD'].Update('')
        j['valorTcD'].Update('')
        return vTV

def FinalizarVpt2(v, tPVP, tabelas, path, data, id, tEProv):
    Qtotal = 0
    total = 0
    # Atualizar P_Vendas
    tabelas[2] = tPVP
    # Atualizar Estoque
    tabelas[6] = tEProv
    condicao = (tabelas[2]['ID'] == str(id))
    quant = tabelas[2].loc[condicao, ['Valor_Total', 'Quantidade']]
    for n in range(len(quant)):
        Qtotal += int(quant['Quantidade'][n])
        total += float(quant['Valor_Total'][n])
    if v['frete'] == True:
        frete = 'Sim'
    else:
        frete = 'Não'
    if v['desconto'] == '':
        desconto = 0
    else:
        desconto = v['desconto']
    if int(desconto) <= total:
        total = total - int(desconto)
    #else:
        #Mensagem
    # Atualizar Vendas
    new_row = {'ID': id,
               'QItens': Qtotal,
               'Frete': frete,
               'Desconto': str(float(desconto)),
               'MétodoPagamento': v['comboPag'],
               'Comentários': v['mT'],
               'Data': data,
               'Valor_Total': total}
    tabelas[3] = tabelas[3].append(new_row, ignore_index=True)
    writerE(tabelas, path)
    return tabelas
