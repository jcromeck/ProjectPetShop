import PySimpleGUI as sg
from Funções import writerE, listaProdutos

def janelaEditProduto(tabelaP):
    produtosExistentes = listaProdutos(tabelaP, 2)
    sg.theme('Black')
    layoutP = [
        [sg.Table(values=produtosExistentes, select_mode=sg.SELECT_MODE_BROWSE, enable_events=True,
                  headings=['Produto', 'Marca', 'Método de Venda', 'Valor Venda', 'Método de Compra', 'Valor Compra'],
                  size=(40, 15), key='-TBEP-')]
    ]
    return sg.Window('Editar Produto', layout=layoutP, finalize=True)

def selProd(tabela_metodo, janelaEdP, PCEPcIdx):
    for index, rows in tabela_metodo.iterrows():
        print(rows.Método)
        print(PCEPcIdx[2])
        if rows.Método == PCEPcIdx[2]:
            m = index
    for index, rows in tabela_metodo.iterrows():
        if rows.Método == PCEPcIdx[4]:
            n = index+1
    if n > 0:
        n = n
    else:
        n = 0
    janelaEdP["Prod"].Update(PCEPcIdx[0])
    janelaEdP["MarcaProduto"].Update(PCEPcIdx[1])
    janelaEdP['metodoVenda'].Update(set_to_index=m, scroll_to_index=m)
    janelaEdP['metodoCompra'].Update(set_to_index=n, scroll_to_index=n)
    janelaEdP['valorMVenda'].Update(PCEPcIdx[3])
    janelaEdP['valorMCompra'].Update(PCEPcIdx[5])

def FinalizarEdit(tabelas, idx, v, j, path):
    difs = [0, 0, 0, 0]
    repEst = 'Não'
    if str(j['metodoCompra'].get()[0]) == 'Outro produto do estoque':
        repEst = 'Sim'
    if tabelas[1].loc[idx, 'Produto'] != v['Prod']:
        difs[0] = 1
    if tabelas[1].loc[idx, 'Marca'] != v['MarcaProduto']:
        difs[1] = 1
    if tabelas[1].loc[idx, 'Método_Venda'] != j['metodoVenda'].get()[0]:
        difs[2] = 1
    if tabelas[1].loc[idx, 'Método_Compra'] != j['metodoCompra'].get()[0]:
        difs[3] = 1
    for index, rows in tabelas[2].iterrows():
        if tabelas[1].loc[idx, 'Produto'] == rows.Produto and tabelas[1].loc[idx, 'Marca'] == rows.Marca and \
           tabelas[1].loc[idx, 'Método_Venda'] == rows.Método:
            if difs[0] == 1:
                tabelas[2].at[index, 'Produto'] = str(v['Prod'])
            if difs[1] == 1:
                tabelas[2].at[index, 'Marca'] = str(v['MarcaProduto'])
            if difs[2] == 1:
                tabelas[2].at[index, 'Método'] = str(j['metodoVenda'].get()[0])
    for index, rows in tabelas[4].iterrows():
        if tabelas[1].loc[idx, 'Produto'] == rows.Produto and tabelas[1].loc[idx, 'Marca'] == rows.Marca and \
           tabelas[1].loc[idx, 'Método_Compra'] == rows.Método:
            if difs[0] == 1:
                tabelas[4].at[index, 'Produto'] = str(v['Prod'])
            if difs[1] == 1:
                tabelas[4].at[index, 'Marca'] = str(v['MarcaProduto'])
            if difs[3] == 1:
                tabelas[4].at[index, 'Método'] = str(j['metodoCompra'].get()[0])
    for index, rows in tabelas[6].iterrows():
        if tabelas[1].loc[idx, 'Produto'] == rows.Produto and tabelas[1].loc[idx, 'Marca'] == rows.Marca and \
           tabelas[1].loc[idx, 'Método_Venda'] == rows.Método:
            if difs[0] == 1:
                tabelas[6].at[index, 'Produto'] = str(v['Prod'])
            if difs[1] == 1:
                tabelas[6].at[index, 'Marca'] = str(v['MarcaProduto'])
            if difs[2] == 1:
                tabelas[6].at[index, 'Método'] = str(j['metodoVenda'].get()[0])
            break
    prov = {'Produto': v['Prod'],
            'Marca': v['MarcaProduto'],
            'Método_Compra': j['metodoCompra'].get()[0],
            'Método_Venda': j['metodoVenda'].get()[0],
            'Valor_Compra': str(v['valorMCompra']),
            'Valor_Venda': str(v['valorMVenda']),
            'ReporEstoquepProd': repEst}
    tabelas[1].loc[idx] = prov
    writerE(tabelas, path)
    return tabelas
