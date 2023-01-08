import PySimpleGUI as sg

def janelaEstatistica():
    sg.theme('Black')
    layout1 = [
        [sg.Text("Lucro Total:"),
         sg.InputText(key="lucroTotalI", visible=False)],
        [sg.Text('', key='lucroTotalT')],

        [sg.Text("Nº Sorteios:"),
         sg.InputText(key="nSorteiosI", visible=False)],
        [sg.Text('', key='nSorteiosT')],

        [sg.Text("Nº de Vendas do Dia:"),
         sg.InputText(key="nVendasDiaI", visible=False)],
        [sg.Text('', key='nVendasDiaT')],

        [sg.Text("Lucro do Dia:"),
         sg.InputText(key="lucroDiaI", visible=False)],
        [sg.Text('', key='lucroDiaT')],

        [sg.Text("Nº de Entregas do Dia:"),
         sg.InputText(key="nEntregaDI", visible=False)],
        [sg.Text('', key='nEntregaDT')]
    ]
    layout2 = [
        [sg.Text("Vendas Efetuadas:"),
         sg.InputText(key="vendasEfetuadasI", visible=False)],
        [sg.Text('', key='vendasEfetuadasT')],

        [sg.Text("Valor Gasto:"),
         sg.InputText(key="valorGastoI", visible=False)],
        [sg.Text('', key='valorGastoT')],

        [sg.Text("Lucro Recebido:"),
         sg.InputText(key="lucroRecebidoI", visible=False)],
        [sg.Text('', key='lucroRecebidoT')],

        [sg.Text("Produto Mais Vendido:"),
         sg.InputText(key="produtoMVI", visible=False)],
        [sg.Text('', key='produtoMVT')],

        [sg.Text("Produto Menos Vendido:"),
         sg.InputText(key="produto_MVI", visible=False)],
        [sg.Text('', key='produto_MVT')],
    ]
    layoutP = [
        [sg.Column(layout1), sg.Column(layout2)]
    ]
    return sg.Window('Estatistica', layout=layoutP, finalize=True)