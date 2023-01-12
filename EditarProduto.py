import PySimpleGUI as sg
from Funções import writerE, listaMetodos

def janelaEditProduto(produtosExistentes):
    sg.theme('Black')
    layoutP = [
        [sg.Table(values=produtosExistentes, select_mode=sg.SELECT_MODE_BROWSE, enable_events=True,
                  headings=['Produto', 'Marca', 'Método de Venda', 'Método de Compra', 'Valor Venda', 'Valor Compra'],
                  size=(40, 15), key='-TBEP-')]
    ]
    return sg.Window('Editar Produto', layout=layoutP, finalize=True)

def selProd(tabelas, janelaEdP, PCEPcIdx):
    for index, rows in tabelas[0].iterrows():
        if rows.Método == PCEPcIdx[2]:
            m = index
    for index, rows in tabelas[0].iterrows():
        if rows.Método == PCEPcIdx[3]:
            n = index+1
        else:
            n = 0
    janelaEdP["Prod"].Update(PCEPcIdx[0])
    janelaEdP["MarcaProduto"].Update(PCEPcIdx[1])
    janelaEdP['metodoVenda'].Update(set_to_index=m, scroll_to_index=m)
    janelaEdP['metodoCompra'].Update(set_to_index=n, scroll_to_index=n)
    janelaEdP['valorMVenda'].Update(PCEPcIdx[4])
    janelaEdP['valorMCompra'].Update(PCEPcIdx[5])

def FinalizarEdit(tabelas, index, v, j, PCEP, path):
    prov = str(v['Prod']), str(v['MarcaProduto']), str(j['metodoCompra'].get()[0]), str(j['metodoVenda'].get()[0]), str(
        v['valorMCompra']), str(v['valorMVenda'])
    PCEP[index] = prov
    tabelas[1].loc[index] = prov
    writerE(tabelas, path)
    return PCEP, tabelas