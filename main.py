import PySimpleGUI as sg
import pandas as pd
from Funções import listaProdutos
from datetime import date
from Adicionar import *
from Cadastrar import *
from Vender import *
from Historico import *
from Estatisticas import *
from EditarProduto import *
from Estoque import *

#CodigoPandas
path = "Arquivos/Compras.xlsx"
pathBackup ="Arquivos/Compras_Backup.xlsx"
tabela_mtds = pd.DataFrame()    #0
tabela_pdts = pd.DataFrame()    #1
tabela_pVds = pd.DataFrame()    #2
tabela_vendas = pd.DataFrame()  #3
tabela_pCompras = pd.DataFrame()#4
tabela_compras = pd.DataFrame() #5
tabela_estoque = pd.DataFrame() #6

try:
    dDf=pd.read_excel(path, sheet_name=['Métodos', 'Produtos', 'P_Vendas', 'Vendas', 'P_Compras', 'Compras', 'Estoque'])
    tabela_mtds = dDf.get('Métodos')
    tabela_pdts = dDf.get('Produtos')
    tabela_pVds = dDf.get('P_Vendas')
    tabela_vendas = dDf.get('Vendas')
    tabela_pCompras = dDf.get('P_Compras')
    tabela_compras = dDf.get('Compras')
    tabela_estoque = dDf.get('Estoque')
    print("Arquivo Encontrado\n\n")
    tabelas = [tabela_mtds, tabela_pdts, tabela_pVds, tabela_vendas, tabela_pCompras, tabela_compras, tabela_estoque]
    print("\n\nMétodos\n"+str(tabelas[0]))
    print("\n\nProdutos\n"+str(tabelas[1]))
    print("\n\nProduto_Vendas\n"+str(tabelas[2]))
    print("\n\nVendas\n"+str(tabelas[3]))
    print("\n\nProduto_Compras\n"+str(tabelas[4]))
    print("\n\nCompras\n"+str(tabelas[5]))
    print("\n\nEstoque\n"+str(tabelas[6]))
except FileNotFoundError as fnfe:
    dDf=pd.read_excel(pathBackup, sheet_name=['Métodos','Produtos','P_Vendas','Vendas','P_Compras','Compras','Estoque'])
    tabela_mtds = dDf.get('Métodos')
    tabela_pdts = dDf.get('Produtos')
    tabela_pVds = dDf.get('P_Vendas')
    tabela_vendas = dDf.get('Vendas')
    tabela_pCompras = dDf.get('P_Compras')
    tabela_compras = dDf.get('Compras')
    tabela_estoque = dDf.get('Estoque')
    print("Arquivo Não Encontrado, colocando backup\n\n")
    tabelas = [tabela_mtds, tabela_pdts, tabela_pVds, tabela_vendas, tabela_pCompras, tabela_compras, tabela_estoque]
    print("\n\nMétodos\n"+str(tabelas[0]))
    print("\n\nProdutos\n"+str(tabelas[1]))
    print("\n\nProduto_Vendas\n"+str(tabelas[2]))
    print("\n\nVendas\n"+str(tabelas[3]))
    print("\n\nProduto_Compras\n"+str(tabelas[4]))
    print("\n\nCompras\n"+str(tabelas[5]))
    print("\n\nEstoque\n"+str(tabelas[6]))

# Código
tabela_vendasProv = tabelas[3]
produtosAVender = []
data_em_texto = date.today().strftime('%d/%m/%Y')
# Adicionar
pA = [] # Perfeito
pCProv = tabelas[4]
idC = 1 # Listar Ultimo id de Compras +1
# Vender
pAV = []# Perfeito
# Histórico
vEH = [] # Listar ID, Data, Quantidades Produtos, ValorTotal
cEH = [] # Listar ID, Data, Quantidades Produtos, ValorTotal

vT=0 ; vTV = 0
t0P = tabelas[1]; vI = False; vBC = False
mdV = listaMetodos(tabelas[0])
mdC = ['Outro produto do estoque'] + mdV
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
janelaP, janelaA, janelaC, janelaV, janelaPop, janelaH, janelaE = janelaInicial(), None, None, None, None, None, None
janelaEP, janelaEst = None, None

# Ler os eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    # Adicionar Produto
    if eventos == 'Adicionar Produto':
        eP, vP = '', ''
        pC = listaProdutos(tabelas[1], 0)
        janelaA = janelaAdicionar(pC, eP, vP, pA)

    # Fechar Programa(Adicionar)
    if eventos == sg.WINDOW_CLOSED and janela == janelaA:
        janelaA['comboProdutos'].Update('')
        janelaA["quantidadeAdicionada"].Update('')
        janelaA.hide()

    # Vender Produto
    if eventos == 'Vender Produto':
        eP, vP = '', ''
        pEV = listaProdutos(tabelas[1], 1)
        janelaV = janelaVender(pEV, pAV, eP, vP)

    # Fechar Programa(Vender)
    if eventos == sg.WINDOW_CLOSED and janela == janelaV:
        janelaV['tiposProdutos'].Update('')
        janelaA["quantidadeAdicionadaV"].Update('')
        janelaV.close()

    # Histórico
    if eventos == 'Histórico':
        janelaH = janelaHistorico(vEH, cEH)
        # Fazer busca através de Data do calendário
        # Ao selecionar ir pra outra página com informações e 2 botões com funções

    #Fechar Histórico
    if eventos == sg.WINDOW_CLOSED and janela == janelaH:
        janelaH.hide()
        #Só fechar ta bom

    # Estatísticas
    if eventos == 'Estatísticas':
        janelaE = janelaEstatistica()
        # Jogar informações na tela

    # Fechar Estatistica
    if eventos == sg.WINDOW_CLOSED and janela == janelaE:
        janelaE.hide()
        #Só fecha mesmo

    # Editar Produto
    if eventos == 'Editar Produto':
        pC = listaProdutos(tabelas[1], 0)
        janelaEP = janelaEditProduto(pC)
        # Excluir Produto e Adicionar um novo com novas informações

    #Fechar Editar Produto
    if eventos == sg.WINDOW_CLOSED and janela == janelaEP:
        janelaEP.hide()
        # Limpar os inputs

    # Estoque
    if eventos == 'Estoque':
        janelaEst = janelaEstoque([])
        # Enviar Produtos em estoque

    #Fechar Editar Produto
    if eventos == sg.WINDOW_CLOSED and janela == janelaEst:
        janelaEst.hide()
        # Só fecha

    # Fechar Programa
    if eventos == sg.WINDOW_CLOSED and janela == janelaP or eventos == 'Sair':
        break

    ###################################################################################################################

    # Selecionar Produto(Adicionar)
    if eventos == 'comboProdutos':
        eP, vP = SePr(tabelas, valores, janela)
        #Feito

    # Carrinho(Adicionar)
    if eventos == 'continuarCompra':
        pA, vT, pCProv = CarAd(tabelas, valores, janela, pCProv, pC, pA, vT, idC)
        #Mudar só o Id

    # Editar(Adicionar)
    if eventos == 'editarEstoque':
        vI, tabelas, vP, eP = EditE(tabelas, path, janela, valores, vI, vP, eP)
        #Feito

    # Cadastro(Adicionar)
    if eventos == 'CadastroProduto':
        janelaC = janelaCadastro(mdV, mdC)
        #Feito

    # Excluir(Adicionar)
    if eventos == 'excluirTBEstoque':
        vT, pCProv, pA = ExC(tabelas, pA, janela, valores, vT, pCProv)
        #Feito

    # Finalizar(Adicionar)
    if eventos == 'Concluir':
        tabelas = FinalizarAd(pCProv, tabelas, path)
        pA = []
        janelaA.close()
############################################## A PARTIR DAQUI ##################################
    # Mudar Visibilidade Metodo Venda(Cadastro)
    if eventos == 'buttonMetodoVenda':
        vBC = visCad(vBC, janela)

    # Confirmar novo Método de Venda(Cadastro)
    if eventos == 'novoMetodoVenda' and not valores['novoMetodoVendaInput'] == '':
        mdV, mdC, tabelas = NewM(tabelas, valores, janela, mdV, path)

    # Adicionar Produto Cadastro(Cadastro)
    if eventos == 'EfetuarCadastro':
        tabelas = EfCad(tabelas, valores, janela, path)
        janelaA['comboProdutos'].Update(pC)
        janelaC.hide()

    # Fechar Programa(Cadastro)
    if eventos == sg.WINDOW_CLOSED and janela == janelaC:
        janelaC.hide()

    # Carrinho(Vender)
    if eventos == 'continuarVCompra':
        vTV, tPVP, pAV = CarVenda(tabelas, valores, pEV, janela, pAV, vTV, tPVP, nV)

    #Excluir Elemento Table
    if eventos == 'excluirTBEstoqueV':
        vTV, tPVP, pAV = ExcV(pAV, janela, valores, vTV, tPVP)

    #Selecionar Produto(Vender)
    if eventos == 'tiposProdutos':
        SePrV(tabelas, valores, janela)

    # Finalizar(Venda)
    if eventos == "FinalizarVenda":
        tabelas = FinalizarV(tPVP, tabelas, path)
        tPVP = tabelas[4]
        nV += 1
        pAV = []
        janelaV.hide()

janela.close()