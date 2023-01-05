import PySimpleGUI as sg
from tkinter import messagebox
from Funções import listaProdutosV, listaMetodos, listaProdutosV1

def janelaVender(produtosEstoque, produtosAVender, estoqueP, valorP):
    sg.theme('Black')
    layoutC1 = [
        [sg.Text('Estoque: ')],
        [sg.Text(estoqueP, expand_x=True, justification='center', key='estoqueTVModificado'),
         sg.Input(key='estoqueVModificado', size=(8, 2), visible=False)]
    ]
    layoutC2 = [
        [sg.Text('Valor: ')],
        [sg.Text(valorP, expand_x=True, justification='center', key='valorPTVModificado'),
         sg.InputText(key='valorProdutoVModificado', visible=False, size=(8, 2))]
    ]
    layoutC= [
        [sg.Column(layoutC1), sg.Column(layoutC2)]
    ]
    layout1= [
        [sg.Text("Produto")],
        [sg.Combo(produtosEstoque, key="tiposProdutos", enable_events=True)],
        [sg.Text("")],
        [sg.Text("Quantidade"), sg.InputText(key="quantidadeAdicionadaV", size=(3, 3), expand_x=True),
         sg.ReadFormButton('', key='editarEstoqueV', button_color='#bee821',
                           image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2,
                           border_width=1)],
        [sg.Text("")],
        [sg.ReadFormButton('', key='continuarVCompra', button_color='#bee821', image_filename='Arquivos/Carrinho.png',
                           image_size=(50, 50), image_subsample=1, border_width=1), sg.Column(layoutC)],
        [sg.Text("")],
        [sg.Button('Finalizar Venda', key="FinalizarVenda", font=(None,15), button_color='#9853d1')]
    ]
    layout2 = [
        [sg.Text('', expand_x=True, justification='Right'),
         sg.ReadFormButton('', key='editarTBEstoqueV', button_color='#bee821',
                          image_filename='Arquivos/EditEstoqueButton.png', image_size=(30, 30), image_subsample=2,
                          border_width=1),
        sg.ReadFormButton('', key='excluirTBEstoqueV', button_color='#9853d1', image_filename='Arquivos/Excluir.png',
                          image_size=(30, 30), image_subsample=2, border_width=1)],
        [sg.Table(values=produtosAVender, headings=['Produto', 'Marca', 'Quant', 'ValorUn', 'ValorTotal'],
                  size=(40, 15), key='tV_produtos')],
        [sg.Text("Valor Total da Compra:", justification='right', expand_x=True)],
        [sg.Text(key='valorTotalV', justification='right', expand_x=True)]
    ]
    layout = [
        [sg.Column(layout1), sg.Column(layout2)]
    ]
    return sg.Window('Vender Produtos', layout=layout, finalize=True)

def CarVenda(tabelas, v, j, produtosEstoque, produtosAVender, valorTotalV, tabela_estoqueP):
    current = v['tiposProdutos']
    if current in produtosEstoque:
        try:
            if int(v['QuantidadeItemVenda']) >= 0:
                quant = int(v['QuantidadeItemVenda'])
                provisorio = v['tiposProdutos'].split("-")
                condicao = (tabelas[1]['Produto'] == provisorio[0]) & (
                            tabelas[1]['Marca'] == provisorio[1]) & (
                            tabelas[1]['Método'] == provisorio[2])
                indice = tabelas[1].loc[condicao, :].index[0]
                produto = listaProdutosV1(tabelas[1], tabelas[0], indice, quant)
                produtoAdicionado = [produto[0], produto[1], produto[2], produto[3], produto[4], produto[5] + " R$", produto[6] + " R$"]
                produtosAVender.append(produtoAdicionado)
                valorTotalV += float(produto[6])
                j['tV_produtos'].Update(values=produtosAVender)
                j["valorTotalV"].Update(str(valorTotalV) + ' R$')
                j['QuantidadeItemVenda'].Update("")
                j['tiposProdutos'].Update("")
                j['metodoVendacP'].Update("")
                new_row = {'Produto': produto[0],
                           'Marca': produto[1],
                           'Método_Venda': produto[2],
                           'Método_Compra': produto[3],
                           'Quantidade': produto[4],
                           'Valor_Venda': produto[5],
                           'Valor_Total': produto[6]}

                #tabela_estoqueP = tabela_estoqueP.append(new_row, ignore_index=True)
            else:
                messagebox.showwarning("Erro ao Adicionar",
                                       'Valor abaixo de 0 não é aceito')
        except ValueError as ve:
            messagebox.showwarning("Erro ao Adicionar",
                                   'O campo Quantidade apenas aceita Números')
    else:
        messagebox.showwarning("Erro ao Adicionar Produto",
                               'Não foi selecionado nenhum produto a ser acrescentado')
