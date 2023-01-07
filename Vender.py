import PySimpleGUI as sg
from tkinter import messagebox
from Funções import listaProdutosV, listaMetodos, listaProdutosV1, writerE

def janelaVender(produtosEstoque, produtosAVender, estoqueP, valorP):
    sg.theme('Black')
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
    layoutC= [
        [sg.Column(layoutC1), sg.Column(layoutC2)]
    ]
    layout1= [
        [sg.Text("Produto")],
        [sg.Combo(produtosEstoque, key="tiposProdutos", enable_events=True)],
        [sg.Text("")],
        [sg.Text("Quantidade"), sg.InputText(key="quantidadeAdicionadaV", size=(3, 3), expand_x=True),
         sg.ReadFormButton('', key='editarEstoqueV', button_color='#bee821',
                           image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2,
                           border_width=1)],
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
        [sg.Text(key='valorTotalV', text_color='green', justification='right', expand_x=True)]
    ]
    layout = [
        [sg.Column(layout1), sg.Column(layout2)]
    ]
    return sg.Window('Vender Produtos', layout=layout, finalize=True)

def CarVenda(t, v, pE, j, pAV, vTV, tPVP, nV):
    atual = v['tiposProdutos']
    if atual in pE:
        if not v['quantidadeAdicionadaV'] == "":
            try:
                if int(v['quantidadeAdicionadaV']) >= 0:
                    quant = int(v['quantidadeAdicionadaV'])
                    provisorio = v['tiposProdutos'].split("-")
                    condicao = (t[2]['Produto'] == provisorio[0]) & (t[2]['Marca'] == provisorio[1]) & (t[2]['Método_Venda'] == provisorio[2])
                    indice = t[2].loc[condicao, :].index[0]
                    produto = listaProdutosV1(t, indice, quant, 0)
                    produtoAdicionado = [produto[0], produto[1], produto[2], produto[3],
                                         produto[4] + " R$", produto[5] + " R$"]
                    pAV.append(produtoAdicionado)
                    j['tV_produtos'].Update(values=pAV)
                    vTV += float(produto[5])
                    j["valorTotalV"].Update('+' + str(vTV) + ' R$')
                    j["quantidadeAdicionadaV"].Update("")
                    j["tiposProdutos"].Update("")
                    produtosProv = listaProdutosV1(t, indice, quant, 0)
                    new_row = {'NVenda': nV,
                               'Produto': produtosProv[0],
                               'Marca': produtosProv[1],
                               'Valor': produtosProv[4],
                               'Método': produtosProv[2],
                               'Quantidade': produtosProv[3],
                               'Valor_Total': produtosProv[5]}
                    tPVP = tPVP.append(new_row, ignore_index=True)
                    return vTV, tPVP, pAV
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

def SePrV(tabelas, v, janela):
    provisorio = v['tiposProdutos'].split("-")
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
    valorP = tabelas[2].loc[indice, 'Valor_Venda']
    janela['estoqueTVModificado'].Update(estoqueP)
    janela['valorPTVModificado'].Update(valorP)
    janela['estoqueVModificado'].Update(estoqueP)
    janela['valorProdutoVModificado'].Update(valorP)
    return estoqueP, valorP

def ExcV(pAV, j, v, vTV, tPVP):
    data_selected = [pAV[row] for row in v['tV_produtos']]
    if data_selected == []:
        messagebox.showwarning("Impossível Deletar Dado",
                               'Precisa Selecionar o Dado na Tabela antes de Deletar')
        return vTV, tPVP, pAV
    else:
        for row in range(len(pAV)):
            if pAV[row][0] == data_selected[0][0] and \
                    pAV[row][1] == data_selected[0][1] and \
                    pAV[row][2] == data_selected[0][2] and \
                    pAV[row][3] == data_selected[0][3] and \
                    pAV[row][4] == data_selected[0][4] and \
                    pAV[row][5] == data_selected[0][5]:
                tPVP.drop(row)
                pAV.pop(row)
        j['tV_produtos'].Update(values=pAV)
        xProv = data_selected[0][5].split(" ")
        vTV -= float(xProv[0])
        j["valorTotalV"].Update('+' + str(vTV) + ' R$')
        return vTV, tPVP, pAV

def FinalizarV(tPVP, tabelas, path):
    tabelas[4] = tPVP
    writerE(tabelas, path)
    return tabelas
