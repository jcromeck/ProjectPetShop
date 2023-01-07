import PySimpleGUI as sg
import pandas as pd
from Funções import listaProdutos
from datetime import date
from Adicionar import *
from Cadastrar import *
from Vender import *

#CodigoPandas
path = "Arquivos/Compras.xlsx"
pathBackup ="Arquivos/Compras_Backup.xlsx"
tabela_vendas = pd.DataFrame()
tabela_estoque = pd.DataFrame()
tabela_produtos = pd.DataFrame()
tabela_metodos = pd.DataFrame()
tabelas = [tabela_estoque, tabela_vendas, tabela_produtos, tabela_metodos]

try:
    dict_df = pd.read_excel(path, sheet_name=['Produtos', 'Estoque', 'Vendas', 'Métodos'])
    tabela_vendas = dict_df.get('Vendas')
    tabela_produtos = dict_df.get('Produtos')
    tabela_estoque = dict_df.get('Estoque')
    tabela_metodos = dict_df.get('Métodos')
    print("Arquivo Encontrado\n\n")
    tabelas = [tabela_estoque, tabela_vendas, tabela_produtos, tabela_metodos]
    print("Estoque\n"+str(tabelas[0])+"\n\n\nVendas\n"+str(tabelas[1])+"\n\n\nProdutos\n"+str(tabelas[2])+"\n\n\nMétodos\n"+str(tabelas[3]))
except FileNotFoundError as fnfe:
    dict_df = pd.read_excel(pathBackup, sheet_name=['Produtos', 'Estoque', 'Vendas', 'Métodos', 'P_Vendas'])
    tabela_prodvendas = dict_df.get('P_Vendas')
    tabela_vendas = dict_df.get('Vendas')
    tabela_produtos = dict_df.get('Produtos')
    tabela_estoque = dict_df.get('Estoque')
    tabela_metodos = dict_df.get('Métodos')
    print("Arquivo Não Encontrado, colocando backup\n\n")
    tabelas = [tabela_estoque, tabela_vendas, tabela_produtos, tabela_metodos, tabela_prodvendas]
    print("Estoque\n" + str(tabelas[0]) + "\n\n\nVendas\n" + str(tabelas[1]) + "\n\n\nProdutos\n" + str(
        tabelas[2]) + "\n\n\nMétodos\n" + str(tabelas[3]) + "\n\n\nProdutos Vendidos\n" + str(tabelas[4]))

# Código
tabela_vendasProv = tabela_vendas
produtosAVender = []
data_em_texto = date.today().strftime('%d/%m/%Y')
pC = listaProdutos(tabelas[2], 0); eP = ''; vP = ''; pA = []; vT=0; vTV = 0
t0P = tabelas[0]; vI = False; vBC = False
mdV = listaMetodos(tabelas[3])
mdC = ['Outro produto do estoque'] + mdV
pAV = []
editTBidx = 0
editTBn = 0
nV = 0
tPVP = tabelas[4]
# Layout
def janelaInicial():
    sg.theme('Black')
    layout = [
        [sg.Image('Arquivos/Logo.png'), sg.Text(data_em_texto, font=(None, 20), justification='center', expand_x=True)],
        [sg.Button('Adicionar Produto', size=(25, 1), button_color='#bee821', font=(None, 20)),
         sg.Button('Vender Produto', size=(25, 1), button_color='#bee821', font=(None, 20))],
        [sg.Button('Histórico', size=(25, 1), button_color='#bee821', font=(None, 20)),
         sg.Button('Estatísticas', size=(25, 1), button_color='#bee821', font=(None, 20))],
        [sg.Button('Editar Produto', size=(25, 1), button_color='#bee821', font=(None, 20)),
         sg.Button('Estoque', size=(25, 1), button_color='#bee821', font=(None, 20))],
        [sg.Button('Sair', size=(25, 1), font=(None, 20), expand_x=True, button_color='#9853d1')]
    ]
    return sg.Window('LUME AGROPET', icon='Arquivos/icon.ico', layout=layout, finalize=True)

# Janela
janela1, janela2, janela3, janela4, janelaPop = janelaInicial(), None, None, None, None

# Ler os eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    # Adicionar Produto
    if eventos == 'Adicionar Produto':
        janela2 = janelaAdicionar(pC, eP, vP, pA)

    # Selecionar Produto(Adicionar)
    if eventos == 'comboProdutos':
        eP, vP = SePr(tabelas, valores, janela)

    # Carrinho(Adicionar)
    if eventos == 'continuarCompra':
        janelaPop, quant, idx = CarAd(tabelas, valores, janela, pC, eP)
        if quant != None:
            vT, t0P, pA = CardAdc(tabelas, valores, janela, idx, quant, vT, pA, t0P)

    # Editar(Adicionar)
    if eventos == 'editarEstoque':
        vI, tabelas, vP, eP = EditE(tabelas, path, janela, valores, vI, vP, eP)

    # Popup
    if eventos == 'concluirPopup':
        eP, t0P = popC(tabelas, t0P, valores, janela)
        vT, t0P, pA = CardAdc(tabelas, valores, janela, idx, quant, vT, pA, t0P)

    # Cadastro(Adicionar)
    if eventos == 'CadastroProduto':
        janela3 = janelaCadastro(mdV, mdC)
        janela2["comboProdutos"].Update(values=pC)

    # Excluir(Adicionar)
    if eventos == 'excluirTBEstoque':
        vT, t0P, pA = ExC(pA, janela, valores, vT, t0P)

    # Finalizar(Adicionar)
    if eventos == 'Concluir':
        tabelas = FinalizarAd(t0P, tabelas, path)
        t0P = tabelas[0]
        pA = []
        janela2.close()

    # Fechar Programa(Adicionar)
    if eventos == sg.WINDOW_CLOSED and janela == janela2:
        janela2.hide()

    # Mudar Visibilidade Metodo Venda(Cadastro)
    if eventos == 'buttonMetodoVenda':
        vBC = visCad(vBC, janela)

    # Confirmar novo Método de Venda(Cadastro)
    if eventos == 'novoMetodoVenda' and not valores['novoMetodoVendaInput'] == '':
        mdV, mdC, tabelas = NewM(tabelas, valores, janela, mdV, path)

    # Adicionar Produto Cadastro(Cadastro)
    if eventos == 'EfetuarCadastro':
        tabelas = EfCad(tabelas, valores, janela, path)
        janela2['comboProdutos'].Update(pC)
        janela3.hide()

    # Fechar Programa(Cadastro)
    if eventos == sg.WINDOW_CLOSED and janela == janela3:
        janela3.hide()

    # Vender Produto
    if eventos == 'Vender Produto':
        eP, vP = '', ''
        pEV = listaProdutos(tabelas[2], 1)
        janela4 = janelaVender(pEV, pAV, eP, vP)

    # Carrinho(Vender)
    if eventos == 'continuarVCompra':
        vTV, tPVP, pAV = CarVenda(tabelas, valores, pEV, janela, pAV, vTV, tPVP, nV)

    #Excluir Elemento Table
    if eventos == 'excluirTBEstoqueV':
        vTV, tPVP, pAV = ExcV(pAV, janela, valores, vTV, tPVP)

    #Selecionar Produto(Vender)
    if eventos == 'tiposProdutos':
        SePrV(tabelas, valores, janela)

    # Finalizar(Adicionar)
    if eventos == "FinalizarVenda":
        tabelas = FinalizarV(tPVP, tabelas, path)
        tPVP = tabelas[4]
        nV += 1
        pAV = []
        janela4.close()

    # Fechar Programa(Cadastro)
    if eventos == sg.WINDOW_CLOSED and janela == janela4:
        janela4.close()




    # Ir para janela Vender Produto
    # if eventos == 'Vender Produto':
    #     janela4 = janelaVender()

    # Fechar Programa
    if eventos == sg.WINDOW_CLOSED and janela == janela1 or eventos == 'Sair':
        break
janela.close()