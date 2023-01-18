import PySimpleGUI as sg
import numpy as np
from Funções import writerE

def janelaHistorico(vendasEfetuadasH, comprasEfetuadasH):

    sg.theme('Black')
    colunaV = [
        [sg.ReadFormButton('', key='voltarH', image_filename='Arquivos/Retornar.png', border_width=0,
                           image_subsample=1, image_size=(43, 43), button_color='black')]

    ]
    layout1 = [
        [sg.Text('')],
        [sg.Text('Data: ')],
        [sg.Input(key='inputDT', size=(27, 1))],
        [sg.Text('Quantidade : ')],
        [sg.Input(key='inputQI', size=(27, 1))]

    ]
    layout2 = [
        [sg.Text('')],
        [sg.Text('ID: ')],
        [sg.Input(key='inputIDH', size=(27, 1))],
        [sg.Text('Valor Total: ')],
        [sg.Input(key='inputVT', size=(27, 1))]
    ]
    l4 = [
        [sg.Text('')],
        [sg.Text("Vendas:", justification='center', expand_x=True)],
        [sg.Table(values=vendasEfetuadasH, select_mode=sg.SELECT_MODE_BROWSE, enable_events=True,
                  col_widths=[5, 8, 15, 10], auto_size_columns=False, expand_x=True,
                  headings=['  ID  ', '  Data  ', 'Quantidade Produtos', 'ValorTotal'], size=(40, 20), key='-TBHV-')]
    ]
    l5 = [
        [sg.Text('')],
        [sg.Text("Compras:", justification='center', expand_x=True)],
        [sg.Table(values=comprasEfetuadasH, select_mode=sg.SELECT_MODE_BROWSE, enable_events=True,
                  col_widths=[5, 8, 15, 10], auto_size_columns=False, expand_x=True,
                  headings=['  ID  ', '  Data  ', 'Quantidade Produtos', 'ValorTotal'], size=(10, 20), key='-TBHC-')]
    ]
    layoutP = [
        [sg.Column(colunaV)],
        [sg.Column(layout1), sg.Column(layout2)],
        [sg.Button('Buscar', key='bPesquisar', font=('Helvetica', 14), button_color='#bee821', size=(37, 1))],
        [sg.Column(l4), sg.Column(l5)]
    ]
    return sg.Window('Histórico', layout=layoutP, finalize=True)

def layoutsAba(produto, marca, metodo, quantidade, valor_un, valor_total, strMetodo, index):
    layout1 = [
        [sg.Text('Quantidade')],
        [sg.Text(quantidade)],
        [sg.Text('Valor Unitário')],
        [sg.Text(valor_un)],
        [sg.Text('Valor Total')],
        [sg.Text(valor_total)]
    ]
    layout2 = [
        [sg.Text('Produto')],
        [sg.Text(produto)],
        [sg.Text('Marca')],
        [sg.Text(marca)],
        [sg.Text(strMetodo)],
        [sg.Text(metodo)]
    ]
    layout = [
        [sg.Column(layout1), sg.Column(layout2)]
    ]
    return sg.Tab(f'Produto {index + 1}', layout, key=f'Tab {index}')

def janelaHistorico2(tabelas, strMetodo, idX):
    n = 0
    tabs_layout = []
    if strMetodo == 'Método de Compra':
        tabela = tabelas[4].copy()
    if strMetodo == 'Método de Venda':
        tabela = tabelas[2].copy()
    for index, rows in tabela.iterrows():
        if int(rows.ID) == idX:
            produto = rows.Produto
            marca = rows.Marca
            metodo = rows.Método
            quantidade = rows.Quantidade
            valor_un = rows.Valor_Un
            valor_total = rows.Valor_Total
            tabs_layout.append(layoutsAba(produto, marca, metodo, quantidade, valor_un, valor_total, strMetodo, n))
            n +=1
    colunaV = [
        [sg.ReadFormButton('', key='voltarH2', image_filename='Arquivos/Retornar.png', border_width=0,
                           image_subsample=1, image_size=(43, 43), button_color='black'),
         sg.Text('', size=(15, 1)),
         sg.ReadFormButton('', key='excluirH2', button_color='red', image_filename='Arquivos/Excluir.png',
                           image_size=(30, 30), image_subsample=2, border_width=1)]
    ]
    layoutP = [
        [sg.Column(colunaV)],
        [sg.Text('ID : '+str(idX), font=('',20), expand_x=True, justification='center')],
        [sg.TabGroup([tabs_layout], enable_events=True, key='Tabgroup')]
    ]
    return sg.Window('Histórico', layout=layoutP, finalize=True)

def ExcluirCompraVenda(tabelas, v, mvc, idX, j, path):
    tabP = v['Tabgroup']
    tabP = tabP.split(' ')
    for n in range(1000):
        if tabP[1] == str(n):
            tab = n
            break
    condicao = (tabelas[mvc]['ID'] == idX)
    indice = tabelas[mvc].loc[condicao, :].index[tab]
    quantidade = tabelas[mvc].at[indice, 'Quantidade']
    vP = tabelas[mvc].at[indice, 'Valor_Total']
    condicao2 = (tabelas[mvc + 1]['ID'] == np.int64(idX))
    indice2 = tabelas[mvc + 1].loc[condicao2, :].index[0]
    atual = tabelas[mvc + 1].at[indice2, 'QItens']
    valorTotal = tabelas[mvc + 1].at[indice2, 'Valor_Total']
    condicao3 = (tabelas[6]['Produto'] == tabelas[mvc].loc[indice, 'Produto']) & \
                (tabelas[6]['Marca'] == tabelas[mvc].loc[indice, 'Marca']) & \
                (tabelas[6]['Método'] == tabelas[mvc].loc[indice, 'Método'])
    indice3 = tabelas[6].loc[condicao3, :].index[0]
    valorAnteriorEstoque = tabelas[6].at[indice3, 'Quantidade']
    tabelas[mvc] = tabelas[mvc].drop(indice)  # atualiza a tabela do produto

    conf1, conf2, conf3, conf4 = 0, 0, 0, 0

    atual = int(atual) - int(quantidade)
    valorTotal = float(valorTotal) - float(vP)
    tabelas[mvc+1].at[indice2, 'QItens'] = str(atual)  # Mudando a quantidade de itens
    tabelas[mvc+1].at[indice2, 'Valor_Total'] = str(valorTotal)  # Mudando o valorTotal de itens

    if mvc == 2: # Venda
        tabelas[6].at[indice3, 'Quantidade'] = int(valorAnteriorEstoque) + int(quantidade)
        writerE(tabelas, path)
        return 'Método de Venda', tabelas
    else:
        tabelas[6].at[indice3, 'Quantidade'] = int(valorAnteriorEstoque) - int(quantidade)
        writerE(tabelas, path)
        return 'Método de Compra', tabelas
