import PySimpleGUI as sg
from Funções import listaEstoque

def janelaEstoque(tabelaE):
    estoque = listaEstoque(tabelaE)
    sg.theme('Black')
    layoutP = [
        [sg.Table(values=estoque, select_mode=sg.SELECT_MODE_BROWSE,
                  headings=['Produto', 'Marca', 'Método', 'Estoque'],
                  size=(40, 15), key='-TB-')]
    ]
    return sg.Window('Estoque', layout=layoutP, finalize=True)