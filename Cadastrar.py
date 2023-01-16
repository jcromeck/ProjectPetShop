import PySimpleGUI as sg
from tkinter import messagebox
from Funções import writerE, listaProdutos, listaMetodos

# Janela
def janelaCadastro(tabelaM):
    metodosdeVenda = listaMetodos(tabelaM)
    metodosdeCompra = ['Outro produto do estoque'] + metodosdeVenda
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
def NewM(tabelas, v, j, metodosdeVenda, path):
    metodosdeVenda.append(v['novoMetodoVendaInput'])
    metodosdeCompra = ['Outro produto do estoque'] + metodosdeVenda
    new_row = {'Método': v["novoMetodoVendaInput"]}
    tabelas[0] = tabelas[0].append(new_row, ignore_index=True)
    writerE(tabelas, path)
    j["TnM"].Update(visible=False)
    j["novoMetodoVendaInput"].Update(visible=False)
    j["novoMetodoVenda"].Update(visible=False)
    j['metodoVenda'].Update(values=metodosdeVenda)
    j['metodoCompra'].Update(values=metodosdeCompra)
    return metodosdeVenda, metodosdeCompra, tabelas
# Efetuar Cadastro
def EfCad(tabelas, v, j, path, pC):
    current = v['metodoVenda']
    current2 = v['metodoCompra']
    if current != []:
        if current2 != []:
            if v["Prod"] == "" or v["valorMVenda"] == "" or v['MarcaProduto'] == "" or v["valorMCompra"] == "":
                messagebox.showwarning("Preencha Todos os campos",
                                       'Preencha os campos corretamente')
                return tabelas, pC, 0
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
                    new_row = {
                        'Produto': v['Prod'],
                        'Marca': v['MarcaProduto'],
                        'Método': j['metodoVenda'].get()[0],
                        'Quantidade': 0}
                    print(tabelas[1])
                    tabelas[6] = tabelas[6].append(new_row, ignore_index=True)
                    writerE(tabelas, path)
                    pC = listaProdutos(tabelas[1], 0)
                    return tabelas, pC, 1
                except ValueError as ve:
                    messagebox.showwarning("Erro ao Cadastrar",
                                           'O campo Valor do Produto apenas aceita Números')
                    return tabelas, pC, 0
        else:
            messagebox.showwarning("Preencha Todos os campos",
                                   'Preencha o campo de Método de Compra')
            return tabelas, pC, 0
    else:
        messagebox.showwarning("Preencha Todos os campos",
                               'Preencha o campo de Método de Venda')
        return tabelas, pC, 0
