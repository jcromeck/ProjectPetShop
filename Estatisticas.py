import PySimpleGUI as sg
import pandas as pd
from collections import Counter

def janelaEstatistica():
    sg.theme('Black')
    layout1 = [
        [sg.Text("Lucro(Vendas): ", expand_x=True, justification='center', font=('Any', 20, 'bold'))],
        [sg.Text('', key='lucroTotalT', expand_x=True, justification='center', font=('Any', 12))],
        [sg.Text('')],

        [sg.Text("Nº de Vendas do Dia:", expand_x=True, justification='center', font=('Any', 20, 'bold'))],
        [sg.Text('', key='nVendasDiaT', expand_x=True, justification='center', font=('Any', 12))],
        [sg.Text('')],

        [sg.Text("Lucro do Dia:", expand_x=True, justification='center', font=('Any', 20, 'bold'))],
        [sg.Text('', key='lucroDiaT', expand_x=True, justification='center', font=('Any', 12))],
        [sg.Text('')],

        [sg.Text("Nº de Entregas do Dia:", expand_x=True, justification='center', font=('Any', 20, 'bold'))],
        [sg.Text('', key='nEntregaDT', expand_x=True, justification='center', font=('Any', 12))],
        [sg.Text('')]
    ]
    layout2 = [
        [sg.Text("Vendas Efetuadas:", expand_x=True, justification='center', font=('Any', 20, 'bold'))],
        [sg.Text('', key='vendasEfetuadasT', expand_x=True, justification='center', font=('Any', 12))],
        [sg.Text('')],

        [sg.Text("Valor Gasto:", expand_x=True, justification='center', font=('Any', 20, 'bold'))],
        [sg.Text('', key='valorGastoT', expand_x=True, justification='center', font=('Any', 12))],
        [sg.Text('')],

        [sg.Text("Lucro Recebido:", expand_x=True, justification='center', font=('Any', 20, 'bold'))],
        [sg.Text('', key='lucroRecebidoT', expand_x=True, justification='center', font=('Any', 12))],
        [sg.Text('')],

        [sg.Text("Produto Mais Vendido:", expand_x=True, justification='center', font=('Any', 20, 'bold'))],
        [sg.Text('', key='produtoMVT', expand_x=True, justification='center', font=('Any', 12))],
        [sg.Text('')]
    ]
    layoutP = [
        [sg.Column(layout1), sg.VSep(), sg.Column(layout2)]
    ]
    return sg.Window('Estatistica', layout=layoutP, finalize=True)

def Estatisticas(tabelas, j, data):
    # Lucro(Vendas)
    lucro_vendas = tabelas[3].loc[:, 'Valor_Total'].sum()
    j["lucroTotalT"].Update(str(lucro_vendas))
    # N° Vendas do Dia
    n = 0
    for index, rows in tabelas[3].iterrows():
        if data == rows.Data:
            n +=1
    j['nVendasDiaT'].Update(str(n))
    # Lucro Dia(Vendas-Compras)
    data = data.split('/')
    data[0], data[2] = data[2], data[0]
    data = str(data[0])+"-"+str(data[1])+'-'+str(data[2])
    condicao = (tabelas[3]['Data'] == data)
    condicao1 = (tabelas[5]['Data'] == data)
    lucro_vendas = tabelas[3].loc[condicao, 'Valor_Total'].sum()
    prejuizo_compras = tabelas[5].loc[condicao1, 'Valor_Total'].sum()
    lucro_dia_vc = lucro_vendas - prejuizo_compras
    j['lucroDiaT'].Update(str(lucro_dia_vc))
    # N de entregas do dia(Vendas)
    count = tabelas[3].loc[(tabelas[3]['Frete'] == 'Sim') & condicao].shape[0]
    j['nEntregaDT'].Update(str(count))
    # Vendas Efetuadas 'vendasEfetuadasT'
    numVendas = tabelas[3].shape[0]
    j['vendasEfetuadasT'].Update(str(numVendas))
    # Valor Gasto(Compras) 'valorGastoT'
    prejuizo = tabelas[5].loc[:, 'Valor_Total'].sum()
    j['valorGastoT'].Update(str(prejuizo))
    # Lucro Recebido(Vendas-Compras) 'lucroRecebidoT'
    lucro_vendas = tabelas[3].loc[:, 'Valor_Total'].sum()
    prejuizo_compras = tabelas[5].loc[:, 'Valor_Total'].sum()
    lucro_vc = lucro_vendas - int(prejuizo_compras)
    j['lucroRecebidoT'].Update(str(lucro_vc))
    # Produto mais vendido 'produtoMVT'
    my_list = []
    for index, rows in tabelas[2].iterrows():
        my_list.append(str(rows.Produto)+'  ' + str(rows.Marca))
    counts = Counter(my_list)
    try:
        most_common_string = max(counts, key=counts.get)
    except ValueError as ve:
        most_common_string = 'Nenhum'
    j['produtoMVT'].Update(most_common_string)