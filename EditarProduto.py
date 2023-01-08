import PySimpleGUI as sg

def janelaEditProduto(produtosExistentes):
    sg.theme('Black')
    layoutP = [
        [sg.Table(values=produtosExistentes, select_mode=sg.SELECT_MODE_BROWSE,
                  headings=['Produto', 'Marca', 'Método de Venda', 'Método de Compra', 'Valor Venda', 'Valor Compra'],
                  size=(40, 15), key='-TB-')]
    ]
    return sg.Window('Editar Produto', layout=layoutP, finalize=True)