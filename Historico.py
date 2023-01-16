import PySimpleGUI as sg
import numpy as np
from Funções import writerE, listarVC

def janelaHistorico(tabelaVP, tabelaCP):
    vendasEfetuadasH, comprasEfetuadasH = listarVC(tabelaVP), listarVC(tabelaCP)
    sg.theme('Black')
    colunaV = [
        [sg.ReadFormButton('', key='voltarH', image_filename='Arquivos/Retornar.png', border_width=0,
                           image_subsample=1, image_size=(43, 43), button_color='black')]

    ]
    layout1 = [
        [sg.Text('')],
        [sg.Text('Data: ')],
        [sg.Input(key='inputDT', size=(27, 1))],
        [sg.Text('Valor Total: ')],
        [sg.Input(key='inputVT', size=(27, 1))]
    ]
    layout2 = [
        [sg.Text('')],
        [sg.Text('ID: ')],
        [sg.Input(key='inputIDH', size=(27, 1))],
        [sg.Text('Quantidade : ')],
        [sg.Input(key='inputQI', size=(27, 1))]
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
        tabela = tabelas[4]
    if strMetodo == 'Método de Venda':
        tabela = tabelas[2]
    for index, rows in tabela.iterrows():
        if rows.ID == idX:
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
    int = 0
    if mvc == 'mv':
        int = 2
        #Venda
    if mvc == 'mc':
        int = 4
        # Compra

    condicao = (tabelas[int]['ID'] == np.int64(idX))
    indice = tabelas[int].loc[condicao, :].index[tab]
    print(type(indice))
    quantidade = tabelas[int].at[indice, 'Quantidade']
    vP = tabelas[int].at[indice, 'Valor_Total']
    tabelas[int] = tabelas[int].drop(indice)  # atualiza a tabela do produto

    condicao2 = (tabelas[int + 1]['ID'] == np.int64(idX))
    indice2 = tabelas[int + 1].loc[condicao2, :].index[0]
    atual = tabelas[int + 1].at[indice2, 'QItens']
    valorTotal = tabelas[int + 1].at[indice2, 'Valor_Total']

    conf1, conf2, conf3, conf4 = 0, 0, 0, 0
    print(vP)
    print(quantidade)
    print(atual)
    print(valorTotal)
    for n in range(10000):
        if str(quantidade) == str(n):
            quantidade = n
            conf1 = 1
        if str(vP) == str(n):
            vP = n
            conf2 = 1
        if conf1 == 1 and conf2 == 1:
            break
    for n in range(100000):
        if str(atual) == str(n):
            atual = n
            conf3 = 1
        if str(valorTotal) == str(n):
            valorTotal = n
            conf4 = 1
        if conf3 == 1 and conf4 == 1:
            break

    atual = atual - quantidade
    valorTotal = valorTotal - vP
    print(tabelas[int+1].at[indice2, 'QItens'])
    print(atual)
    tabelas[int+1].at[indice2, 'QItens'] = atual  # Mudando a quantidade de itens
    tabelas[int+1].at[indice2, 'Valor_Total'] = valorTotal  # Mudando o valorTotal de itens
    writerE(tabelas, path)
    j['Tabgroup'].remove(tab)  # Tirando a tab