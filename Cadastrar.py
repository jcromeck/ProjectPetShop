import PySimpleGUI as sg
from tkinter import messagebox
from Funções import writerE
# Janela
def janelaCadastro(metodosdeVenda,metodosdeCompra):
    sg.theme('Black')
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
    layoutP = [
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
        [sg.Text("Insira um novo Método", key='TnM', expand_x=True, justification='right', visible=False)],
        [sg.InputText(key='novoMetodoVendaInput', visible=False),
         sg.Button("+", key="novoMetodoVenda", visible=False, button_color='#bee821')],
        [sg.Button("EfetuarCadastro", button_color='#9853d1')]
    ]
    return sg.Window('Cadastrar Produtos', layout=layoutP, finalize=True)
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
def NewM(tabelas, v, j, metodosdeVenda, path):
    metodosdeVenda.append(v['novoMetodoVendaInput'])
    metodosdeCompra = ['Outro produto do estoque'] + metodosdeVenda
    new_row = [{'Método': v["novoMetodoVendaInput"]}]
    tabelas[0] = tabelas[0].append(new_row, ignore_index=True)
    writerE(tabelas, path)
    j["TnM"].Update(visible=False)
    j["novoMetodoVendaInput"].Update(visible=False)
    j["novoMetodoVenda"].Update(visible=False)
    j['metodoVenda'].Update(values=metodosdeVenda)
    j['metodoCompra'].Update(values=metodosdeCompra)
    return metodosdeVenda, metodosdeCompra, tabelas
# Efetuar Cadastro
def EfCad(tabelas, v, j, path):
    current = v['metodoVenda']
    current2 = v['metodoCompra']
    if current != []:
        if current2 != []:
            if v["Prod"] == "" or v["valorMVenda"] == "" or v['MarcaProduto'] == "" or v["valorMCompra"] == "":
                messagebox.showwarning("Preencha Todos os campos",
                                       'Preencha os campos corretamente')
            else:
                try:
                    if v['metodoCompra'] == 'Outro produto do estoque':
                        outroProduto = 'Sim'
                    else:
                        outroProduto = 'Não'
                    a = float(v['valorMVenda'])
                    a = float(v['valorMCompra'])
                    new_row = {'Produto': v["Prod"],
                               'Marca': v["MarcaProduto"],
                               'Valor_Venda': v['valorMVenda'],
                               'Valor_Compra': v['valorMCompra'],
                               'Método_Venda': j['metodoVenda'].get()[0],
                               'Método_Compra': j["metodoCompra"].get()[0],
                               'ReporEstoquepProd': outroProduto}
                    tabelas[1] = tabelas[1].append(new_row, ignore_index=True)
                    writerE(tabelas, path)
                    return tabelas
                except ValueError as ve:
                    messagebox.showwarning("Erro ao Cadastrar",
                                           'O campo Valor do Produto apenas aceita Números')
        else:
            messagebox.showwarning("Preencha Todos os campos",
                                   'Preencha o campo de Método de Compra')
    else:
        messagebox.showwarning("Preencha Todos os campos",
                               'Preencha o campo de Método de Venda')