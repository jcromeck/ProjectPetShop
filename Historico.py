import PySimpleGUI as sg

def janelaHistorico(vendasEfetuadasH,comprasEfetuadasH):
    sg.theme('Black')
    layout1 = [
        [sg.Text('', expand_x=True), sg.Text("Vendas:"), sg.Text('', expand_x=True)],
        [sg.Table(values=vendasEfetuadasH, select_mode=sg.SELECT_MODE_BROWSE,
                  headings=['ID', 'Data', 'NumProdutos', 'ValorTotal'], size=(40, 20), key='-TBHV-')]
    ]
    layout2 = [
        [sg.Text('', expand_x=True), sg.Text("Compras:"), sg.Text('', expand_x=True)],
        [sg.Table(values=comprasEfetuadasH, select_mode=sg.SELECT_MODE_BROWSE,
                  headings=['ID', 'Data', 'NumProdutos', 'ValorTotal'], size=(40, 20), key='-TBHV-')]
    ]
    layoutP = [
        [sg.CalendarButton('Selecione uma data',  format='%d/%m/%Y', key='-DATE-', button_color='#bee821'),
         sg.Text('', expand_x=True)],
        [sg.Column(layout1), sg.Column(layout2)]
    ]
    return sg.Window('Histórico', layout=layoutP, finalize=True).read()


def janelaHistorico2():
    layoutP = [
        [sg.Text('Nº '),
         sg.Text('',key='nHist', expand_x=True),
         sg.ReadFormButton('', key='editarH', button_color='#bee821',
                           image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2,
                           border_width=1),
        sg.ReadFormButton('', key='excluirH', button_color='red', image_filename='Arquivos/Excluir.png',
                          image_size=(30, 30), image_subsample=2, border_width=1)]
    ]
    return sg.Window('Histórico', layout=layoutP, finalize=True)