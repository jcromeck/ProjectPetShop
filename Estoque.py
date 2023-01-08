import PySimpleGUI as sg

def janelaEstoque(estoque):
    sg.theme('Black')
    layoutP = [
        [sg.Table(values=estoque, select_mode=sg.SELECT_MODE_BROWSE,
                  headings=['Produto', 'Marca', 'Método', 'Estoque'],
                  size=(40, 15), key='-TB-')]
    ]
    return sg.Window('Estoque', layout=layoutP, finalize=True)