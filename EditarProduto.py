import PySimpleGUI as sg
from Funções import writerE, listaMetodos

def janelaEditProduto(produtosExistentes):
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

def FinalizarEdit(tabelas, index, v, j, PCEP, path):
    prov = [str(v['Prod']), str(v['MarcaProduto']), str(j['metodoVenda'].get()[0]),
            str(v['valorMVenda']), str(j['metodoCompra'].get()[0]), str(v['valorMCompra'])]
    PCEP[index] = prov
    if str(j['metodoCompra'].get()[0]) == 'Outro produto do estoque':
        repEst = 'Sim'
    else:
        repEst = 'Não'
    prov = {'Produto': str(v['Prod']),
            'Marca': str(v['MarcaProduto']),
            'Método_Compra': str(j['metodoCompra'].get()[0]),
            'Método_Venda': str(j['metodoVenda'].get()[0]),
            'Valor_Compra': str(v['valorMCompra']),
            'Valor_Venda': str(v['valorMVenda']),
            'ReporEstoquepProd': repEst}
    tabelas[1].loc[index] = prov
    writerE(tabelas, path)
    return PCEP, tabelas