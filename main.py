import PySimpleGUI as sg
import pandas as pd
from Funções import listaProdutos, listarVC, listarBusca, listaEstoque
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
tabela_mtds = pd.DataFrame()      # 0
tabela_pdts = pd.DataFrame()      # 1
tabela_pVds = pd.DataFrame()      # 2
tabela_vendas = pd.DataFrame()    # 3
tabela_pCompras = pd.DataFrame()  # 4
tabela_compras = pd.DataFrame()   # 5
tabela_estoque = pd.DataFrame()   # 6

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
idV = 10000 #Listar Ultimo id de Vendas +1
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
janelaEP, janelaEst, janelaV2, janelaEPC = None, None, None, None

# Ler os eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    # Adicionar Produto
    if eventos == 'Adicionar Produto':
        eP, vP = '', ''
        tEP = tabelas[6]
        pC = listaProdutos(tabelas[1], 0)
        janelaA = janelaAdicionar(pC, eP, vP, pA)
        #Pronto

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
        janelaV["quantidadeAdicionadaV"].Update('')
        janelaV.close()

    # Histórico
    if eventos == 'Histórico':
        vEH = listarVC(tabelas[3])
        cEH = listarVC(tabelas[5])
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
        estatisticas(tabelas, janelaE, data_em_texto)
        # Jogar informações na tela

    # Fechar Estatistica
    if eventos == sg.WINDOW_CLOSED and janela == janelaE:
        janelaE.hide()
        #Só fecha mesmo

    # Fechar Editar Produto - Cadastro
    if eventos == sg.WINDOW_CLOSED and janela == janelaEPC:
        janelaEPC.hide()
        # Só fecha mesmo

    # Editar Produto
    if eventos == 'Editar Produto':
        pCEP = listaProdutos(tabelas[1], 2)
        janelaEP = janelaEditProduto(pCEP)

    #Selecionar Produto(Editar Produto)
    if eventos == '-TBEP-':
        janelaEPC = janelaCadastro(mdV, mdC)
        print(tabelas[0])
        selProd(tabelas[0], janelaEPC, pCEP[valores['-TBEP-'][0]])
        idxEdit = valores['-TBEP-'][0]
######################################## ARRUMAR VOLTAR DO SELECIONAR PRODUTO #########################################
    #Fechar Editar Produto
    if eventos == sg.WINDOW_CLOSED and janela == janelaEP:
        janelaEP.hide()
        # Limpar os inputs

    # Estoque
    if eventos == 'Estoque':
        estoque = listaEstoque(tabelas[6])
        janelaEst = janelaEstoque(estoque)
        # Enviar Produtos em estoque

    #Fechar Editar Produto
    if eventos == sg.WINDOW_CLOSED and janela == janelaEst:
        janelaEst.hide()
        # Só fecha

    # Fechar Programa
    if eventos == sg.WINDOW_CLOSED and janela == janelaP or eventos == 'Sair':
        break

    # Selecionar Produto(Adicionar)
    if eventos == 'comboProdutos':
        eP, vP = SePr(tabelas, valores, janela)
        #Feito

    # Carrinho(Adicionar)
    if eventos == 'continuarCompra':
        pA, vT, pCProv, tEP = CarAd(tabelas, valores, janela, pCProv, pC, pA, vT, idC, tEP)
        #Feito

    # Cadastro(Adicionar)
    if eventos == 'CadastroProduto':
        janelaC = janelaCadastro(mdV, mdC)
        #Feito

    # Excluir(Adicionar)
    if eventos == 'excluirTBEstoque':
        vT, pCProv, pA = ExC(tabelas, pA, janela, valores, vT, pCProv)
        #Confirmar funcionamento

    # Finalizar(Adicionar)
    if eventos == 'Concluir':
        tabelas = FinalizarAd(pCProv, tabelas, path, idC, data_em_texto, tEP)
        pA = []
        janelaA.close()

    # Mudar Visibilidade Metodo Venda(Cadastro)
    if eventos == 'buttonMetodoVenda':
        vBC = visCad(vBC, janela)
        #Feito

    # Confirmar novo Método de Venda(Cadastro)
    if eventos == 'novoMetodoVenda' and not valores['novoMetodoVendaInput'] == '':
        mdV, mdC, tabelas = NewM(tabelas, valores, janela, mdV, path)
        #Feito

    # Adicionar Produto Cadastro(Cadastro)
    if eventos == 'EfetuarCadastro' and janela == janelaC:
        tabelas = EfCad(tabelas, valores, janela, path)
        pC = listaProdutos(tabelas[1], 0)
        print(pC)
        janelaA['comboProdutos'].Update(values=pC)
        janelaC.hide()
        #Feito

    # Editar Produto(Cadastro)
    if eventos == 'EfetuarCadastro' and janela == janelaEPC:
        pCEP, tabelas =FinalizarEdit(tabelas, idxEdit, valores, janelaEPC, pCEP, path)
        janelaEPC.close()
        janelaEP.close()
        pCEP = listaProdutos(tabelas[1], 2)
        janelaEP = janelaEditProduto(pCEP)

    # Fechar Programa(Cadastro)
    if eventos == sg.WINDOW_CLOSED and janela == janelaC:
        janelaC.hide()
        #Feito

    # Selecionar Produto(Vender)
    if eventos == 'tiposProdutos':
        ePV, vPV = SePrV(tabelas, valores, janela)
        #Feito

    # Carrinho(Vender)
    if eventos == 'continuarVCompra':
        vTV, tPVP, pAV = CarVenda(tabelas, valores, pEV, janela, pAV, vTV, tPVP, nV)
        # Validar se tem no estoque

    # Editar(Vender)
    if eventos == 'editarEstoqueV':
        vIV, tabelas, vPV, ePV = EditEV(tabelas, path, janela, valores, vIV, vPV, ePV)
        # Feito

    #Excluir Elemento Table(Vender)
    if eventos == 'excluirTBEstoqueV':
        vTV, tPVP, pAV = ExcV(pAV, janela, valores, vTV, tPVP)
        #Conferir pra ver se ta certo

    # Finalizar(Venda)
    if eventos == "FinalizarVenda":
        if pAV != []:
            janelaV2 = janelaVender2(vTV)
        else:
            messagebox.showwarning("Erro ao Finalizar",
                                   "Não há produtos a vender para poder Finalizar")

    #Voltar(Adicionar)
    if eventos == 'voltarA':
        janelaA.hide()
        janelaP.un_hide()

    # Voltar(Vender)
    if eventos == 'voltarV':
        janelaV.hide()
        janelaP.un_hide()

    # Voltar(Vender2)
    if eventos == 'voltarV2':
        janelaV2.hide()
        janelaV.un_hide()

    # Voltar(Cadastro)
    if eventos == 'voltarC' and janela == janelaC:
        janelaC.hide()
        janelaA.un_hide()

    # Voltar(Cadastro- Editar Produto)
    if eventos == 'voltarC' and janela == janelaEPC:
        janelaEPC.hide()
        janelaEP.un_hide()

    # Voltar(Histórico)
    if eventos == 'voltarH':
        janelaH.hide()
        janelaP.un_hide()
    if eventos == 'voltarH2':
        janelaH.close()
        janelaH = janelaHistorico(vEH, cEH)

    #Finalizar Parte 2
    if eventos == 'concluirV':
        if valores['comboPag'] == []:
            tabelas = FinalizarVpt2(valores, tPVP, tabelas, path, data_em_texto, idV)
            idV += 1
            janelaV2.close()
            janelaV.close()
        else:
            messagebox.showwarning("Erro ao Finalizar",
                                   "Selecione o Método de venda")

    #Atualizar Desconto (Finalizar Pt2)
    if eventos == 'desconto':
        vTD = AtualizarDesconto(valores, janela, vTV)
        #Finalizado

    # Buscar (Histórico)
    if eventos == 'bPesquisar':
        listarBusca(tabelas, valores['inputIDH'], valores['inputQI'], valores['inputDT'], valores['inputVT'], janela)

    #Selecionar Table(Histórico)
    if eventos == '-TBHV-':
        janelaH.close()
        array = vEH
        idx = valores['-TBHV-']
        array = array[idx[0]]
        janelaH = janelaHistorico2(tabelas, 'Método de Venda', array[0])
        id_ExcluirV, id_ExcluirC = array[0], None
    if eventos == '-TBHC-':
        janelaH.close()
        array = cEH
        idx = valores['-TBHC-']
        array = array[idx[0]]
        janelaH = janelaHistorico2(tabelas, 'Método de Compra', array[0])
        id_ExcluirV, id_ExcluirC = None, array[0]

    # Excluir(Histórico)
    if eventos == 'excluirH2':
        if id_ExcluirV == None:
            ExcluirCompraVenda(tabelas, valores, 'mc', id_ExcluirC, janela, path)
        else:
            ExcluirCompraVenda(tabelas, valores, 'mv', id_ExcluirV, janela, path)
        janelaH.close()
        vEH = listarVC(tabelas[3])
        cEH = listarVC(tabelas[5])
        janelaH = janelaHistorico(vEH, cEH)














janela.close()