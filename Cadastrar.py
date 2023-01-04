import PySimpleGUI as sg
from tkinter import messagebox
from Funções import writerE, listaMetodos

def janelaCadastro(tabelas,metodosdeVenda,metodosdeCompra):
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
        [sg.Text("Métodos", expand_x=True, justification='center', visible=False)],
        [sg.InputText(key='novoMetodoVendaInput', visible=False),
         sg.Button("+", key="novoMetodoVenda", visible=False, button_color='#bee821')],
        [sg.Button("EfetuarCadastro", button_color='#9853d1')]
    ]
    return sg.Window('Cadastrar Produtos', layout=layoutP, finalize=True)

def mainC(tabelas, path):
    metodosdeVenda = listaMetodos(tabelas[3])
    metodosdeCompra = ['Outro produto do estoque'] + metodosdeVenda
    janela = janelaCadastro(tabelas,metodosdeVenda,metodosdeCompra)
    visBCad = False
    while True:
        j, e, v = janela.read()

        # Mudar Visibilidade Metodo Venda
        if e == 'buttonMetodoVenda':
            if visBCad == False:
                j["novoMetodoVendaInput"].Update("")
                j["novoMetodoVendaInput"].Update(visible=True)
                j["novoMetodoVenda"].Update(visible=True)
                visBCad = True
            else:
                j["novoMetodoVendaInput"].Update(visible=False)
                j["novoMetodoVenda"].Update(visible=False)
                visBCad = False

        # Confirmar novo Método de Venda
        if e == 'novoMetodoVenda' and not v['novoMetodoVendaInput'] == '':
            metodosdeVenda.append(v['novoMetodoVendaInput'])
            new_row = [{'Métodos': v["novoMetodoVendaInput"]}]
            tabelas[3] = tabelas[3].append(new_row, ignore_index=True)
            writerE(tabelas, path)
            j["novoMetodoVendaInput"].Update(visible=False)
            j["novoMetodoVenda"].Update(visible=False)
            j['metodoVenda'].Update(values=metodosdeVenda)
            j['metodoCompra'].Update(values=metodosdeVenda)

        # Adicionar Produto Cadastro
        if e == 'EfetuarCadastro':
            current = v['metodoVenda']
            current2 = v['metodoCompra']
            if current != []:
                if current2 != []:
                    if v["Prod"] == "" or v["valorMVenda"] == "" or v['MarcaProduto'] == "" or v["valorMCompra"] == "":
                        messagebox.showwarning("Preencha Todos os campos", 'Preencha os campos corretamente')
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
                                       'Método_Venda': v["metodoVenda"],
                                       'Método_Compra': v["metodoCompra"],
                                       'ReporEstoquepProd': outroProduto}
                            tabelas[2] = tabelas[2].append(new_row, ignore_index=True)
                            writerE(tabelas, path)
                            break
                        except ValueError as ve:
                            messagebox.showwarning("Erro ao Cadastrar",
                                                   'O campo Valor do Produto apenas aceita Números')
                else:
                    messagebox.showwarning("Preencha Todos os campos",
                                           'Preencha o campo de Método de Compra')
            else:
                messagebox.showwarning("Preencha Todos os campos",
                                       'Preencha o campo de Método de Venda')

        # Sair da janela Cadastrar Produto e Voltar para Adicionar Produto
        if e == sg.WINDOW_CLOSED:
            break
    janela.close()
    tabelas1 = tabelas
    return tabelas1