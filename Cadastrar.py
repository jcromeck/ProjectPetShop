import PySimpleGUI as sg
from Funções import writerE, listaProdutos

# Janela
def janelaCadastro(metodosdeVenda, metodosdeCompra):
    sg.theme('Black')
    colunaV = [
        [sg.ReadFormButton('', key='voltarC', image_filename='Arquivos/Retornar.png', border_width=0,
                           image_subsample=1, image_size=(43, 43), button_color='black')],
        [sg.Text('', size=(0, 25))]
    ]
    layout1 = [
        [sg.Text("Método de Venda:")],
        [sg.Listbox(metodosdeVenda, key='metodoVenda', size=(30, 6))],
        [sg.Text("Valor de Venda:")],
        [sg.InputText(key='valorMVenda', size=(32, 6))]
    ]
    layout2 = [
        [sg.Text("Método de Compra:")],
        [sg.Listbox(metodosdeCompra, key='metodoCompra', size=(30, 6))],
        [sg.Text("Valor de Compra:")],
        [sg.InputText(key='valorMCompra', size=(32, 6))]
    ]
    layout = [
        [sg.Text("Produto:")],
        [sg.InputText(key="Prod")],
        [sg.Text("Marca: ")],
        [sg.InputText(key="MarcaProduto")],
        [sg.Text(' ')],
        [sg.HSep()],
        [sg.Text("Métodos", expand_x=True, justification='center')],
        [sg.Column(layout1), sg.Column(layout2)],
        [sg.Text(' ')],
        [sg.HSep()],
        [sg.Text(' ')],
        [sg.Button("+", key='buttonMetodoVenda', expand_x=True, button_color='#bee821')],
        [sg.Text("Insira um novo Método", key='TnM', expand_x=True, justification='left', visible=False)],
        [sg.InputText(key='novoMetodoVendaInput', visible=False),
         sg.Button("+", key="novoMetodoVenda", visible=False, button_color='#bee821')],
        [sg.Button("EfetuarCadastro", button_color='#9853d1')]
    ]
    layoutP = [
        [sg.Column(colunaV), sg.Column(layout)]
    ]
    return sg.Window('Cadastrar Produtos', icon='Arquivos/icon.ico', layout=layoutP, finalize=True)
# Visualização Cadastrar Método
def visCad(visBCad, j):
    if visBCad == False:
        j["novoMetodoVendaInput"].Update("")
        j["TnM"].Update(visible=True)
        j["novoMetodoVendaInput"].Update(visible=True)
        j["novoMetodoVenda"].Update(visible=True)
        visBCad = True
    else:
        j["TnM"].Update(visible=False)
        j["novoMetodoVendaInput"].Update(visible=False)
        j["novoMetodoVenda"].Update(visible=False)
        visBCad = False
    return visBCad
# Cadastrar Método Novo
def NewM(tabelas, v, j, path, metodosdeVenda, metodosdeCompra):
    metodosdeVenda.append(v['novoMetodoVendaInput'])
    metodosdeCompra.append(v['novoMetodoVendaInput'])
    new_row = {'Método': v["novoMetodoVendaInput"]}
    tabelas[0] = tabelas[0].append(new_row, ignore_index=True)
    writerE(tabelas, path)
    j["TnM"].Update(visible=False)
    j["novoMetodoVendaInput"].Update(visible=False)
    j["novoMetodoVenda"].Update(visible=False)
    j['metodoVenda'].Update(values=metodosdeVenda)
    j['metodoVenda'].Update(set_to_index=len(metodosdeVenda)-1)
    j['metodoCompra'].Update(values=metodosdeCompra)
    j['metodoCompra'].Update(set_to_index=len(metodosdeCompra)-1)
    return metodosdeVenda, metodosdeCompra, tabelas
# Efetuar Cadastro
def EfCad(tabelas, v, j, path, tEP):
        a = float(v['valorMVenda'])
        a = float(v['valorMCompra'])
        new_row = {'Produto': v["Prod"],
                   'Marca': v["MarcaProduto"],
                   'Valor_Venda': v['valorMVenda'],
                   'Valor_Compra': v['valorMCompra'],
                   'Método_Venda': j['metodoVenda'].get()[0],
                   'Método_Compra': j["metodoCompra"].get()[0]}
        tabelas[1] = tabelas[1].append(new_row, ignore_index=True)
        new_row = {'Produto': v['Prod'],
                   'Marca': v['MarcaProduto'],
                   'Método': j['metodoVenda'].get()[0],
                   'Quantidade': 0}
        tabelas[6] = tabelas[6].append(new_row, ignore_index=True)
        tEP = tEP.append(new_row, ignore_index=True)
        writerE(tabelas, path)
        pC = listaProdutos(tabelas[1], 0)
        return tabelas, pC, tEP
