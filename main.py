import PySimpleGUI as sg
import pandas as pd
from Funções import listaProdutos, conferir, listaMetodos
from datetime import date
from Adicionar import *
from Cadastrar import *
from Vender import *

def newRow(d, n, n1):
    if n == 10:
        for row in range(len(rowVendas)):
            tabela_vendas.append(rowVendas[row], ignore_index=True)
        with pd.ExcelWriter(path) as writer:
            tabela_produtos.to_excel(writer, sheet_name='Produtos', index=False)
            tabela_estoque.to_excel(writer, sheet_name='Estoque', index=False)
            tabela_vendas.to_excel(writer, sheet_name='Vendas', index=False)
            tabela_metodos.to_excel(writer, sheet_name='Métodos', index=False)
        rowVendas.clear()
    if n == 11:
        for row in range(len(rowEstoque)):
            tabela_estoque.append(rowEstoque[row], ignore_index=True)
        with pd.ExcelWriter(path) as writer:
            tabela_produtos.to_excel(writer, sheet_name='Produtos', index=False)
            tabela_estoque.to_excel(writer, sheet_name='Estoque', index=False)
            tabela_vendas.to_excel(writer, sheet_name='Vendas', index=False)
            tabela_metodos.to_excel(writer, sheet_name='Métodos', index=False)
        rowEstoque.clear()
    if n == 12:
        for row in range(len(rowProdutos)):
            tabela_produtos.append(rowProdutos[row], ignore_index=True)
        with pd.ExcelWriter(path) as writer:
            tabela_produtos.to_excel(writer, sheet_name='Produtos', index=False)
            tabela_estoque.to_excel(writer, sheet_name='Estoque', index=False)
            tabela_vendas.to_excel(writer, sheet_name='Vendas', index=False)
            tabela_metodos.to_excel(writer, sheet_name='Métodos', index=False)
        rowProdutos.clear()

def Dtto_Excel(tabelas, num):
    #Estoque
    if num == 1:
        quant = int(valores['quantidadeAdicionada'])
        provisorio = valores['comboProdutos'].split(". ")
        produtosProv = listaProdutos1(tabela_produtos, provisorio[0], quant, 1)
        new_row = {'Produto':      produtosProv[0],
                   'Marca':        produtosProv[1],
                   'Método':       produtosProv[2],
                   'Quantidade':   produtosProv[3],
                   'Valor_Venda':  produtosProv[4],
                   'Valor_Compra': produtosProv[5]}
        tabela_estoqueProv = tabelas[0].append(new_row, ignore_index=True)
        print('Estoque Prov Com nova linha')
        return tabelas
    #Métodos
    if num == 3:

        return tabelas

#CodigoPandas
path = "Arquivos/Compras.xlsx"
pathBackup ="Arquivos/Compras_Backup.xlsx"
tabela_vendas = pd.DataFrame()
rowVendas = []
tabela_estoque = pd.DataFrame()
rowEstoque = []
tabela_produtos = pd.DataFrame()
rowProdutos = []
tabela_metodos = pd.DataFrame()
rowMetodos = []
tabelas = [tabela_estoque, tabela_vendas, tabela_produtos, tabela_metodos]

try:
    dict_df = pd.read_excel(path, sheet_name=['Produtos', 'Estoque', 'Vendas','Métodos'])
    tabela_vendas = dict_df.get('Vendas')
    tabela_produtos = dict_df.get('Produtos')
    tabela_estoque = dict_df.get('Estoque')
    tabela_metodos = dict_df.get('Métodos')
    print("Arquivo Encontrado\n\n")
    tabelas = [tabela_estoque, tabela_vendas, tabela_produtos, tabela_metodos]
    print("Estoque\n"+str(tabelas[0])+"\n\n\nVendas\n"+str(tabelas[1])+"\n\n\nProdutos\n"+str(tabelas[2])+"\n\n\nMétodos\n"+str(tabelas[3]))
except FileNotFoundError as fnfe:
    dV= {'Produto':[], 'Marca':[], 'Quantidade':[], 'Valor_Unitário':[], 'Valor_Total':[], 'Método_Venda':[], 'NumVenda':[]}
    dE= {'Produto':[], 'Marca':[], 'Quantidade':[], 'Valor_Venda':[], 'Valor_Compra':[],'Método':[]}
    dP= {'Produto':[], 'Marca':[], 'Método_Venda':[], 'Valor_Método':[], 'Método_Compra':[]}
    dM= {'Métodos':[]}
    tabela_vendas=pd.DataFrame(data=dV)
    tabela_estoque=pd.DataFrame(data=dE)
    tabela_produtos=pd.DataFrame(data=dP)
    tabela_metodos=pd.DataFrame(data=dM)
    print("Arquivo não lido, criando um dataframe substituto")
except ValueError as ve:
    print("Arquivo encontrado, porém sem todas sheets")
    tabelas = conferir(tabelas, path, 0)
    print(tabelas)
    tabela_estoque = tabelas[0]
    tabela_vendas = tabelas[1]
    tabela_produtos = tabelas[2]
    tabela_metodos = tabelas[3]

#Código
tabela_vendasProv = tabela_vendas
produtosAVender = []
data_em_texto = date.today().strftime('%d/%m/%Y')
pC = listaProdutos(tabelas[2]); eP = ''; vP = ''; pA = []; vT=0; vTV = 0
t0P = tabelas[0]; vI = False; vBC = False
mdV = listaMetodos(tabelas[3])
mdC = ['Outro produto do estoque'] + mdV
pE = listaProdutosV(tabelas[0], 0)
pAV = []

#Layout
def janelaInicial():
    sg.theme('Black')
    layout= [
        [sg.Image('Arquivos/Logo.png'), sg.Text(data_em_texto, font=(None, 20), justification='center', expand_x=True)],
        [sg.Button('Adicionar Produto', size=(25,1),button_color='#bee821',font=(None,20)),sg.Button('Vender Produto', size=(25,1),button_color='#bee821',font=(None,20))],
        [sg.Button('Histórico', size=(25,1),button_color='#bee821',font=(None,20)),sg.Button('Estatísticas', size=(25,1),button_color='#bee821',font=(None,20))],
        [sg.Button('Editar Produto', size=(25,1),button_color='#bee821',font=(None,20)),sg.Button('Estoque', size=(25,1),button_color='#bee821',font=(None,20))],
        [sg.Button('Sair', size=(25,1), font=(None,20), expand_x=True, button_color='#9853d1')]
    ]
    return sg.Window('LUME AGROPET', icon='Arquivos/icon.ico', layout=layout, finalize=True)

#Janela
janela1, janela2, janela3, janela4, janelaPop = janelaInicial(), None, None, None, None

#Ler os eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    #Adicionar Produto
    if eventos == 'Adicionar Produto':
        janela2 = janelaAdicionar(pC, eP, vP, pA)

    #Selecionar Produto(Adicionar)
    if eventos == 'comboProdutos':
        eP, vP = SePr(tabelas, valores, janela)

    # Carrinho(Adicionar)
    if eventos == 'continuarCompra':
        janelaPop, quant, idx = CarAd(tabelas, valores, janela, pC, eP)
        vT, t0P, pA = CardAdc(tabelas, valores, janela, idx, quant, vT, pA, t0P)

    # Editar(Adicionar)
    if eventos == 'editarEstoque':
        vI, tabelas = EditE(tabelas, path, janela, valores, vI, eP, vP)

    #Popup
    if eventos == 'concluirPopup':
        eP, t0P = popC(tabelas, t0P, valores, janela)
        vT, t0P, pA = CardAdc(tabelas, valores, janela, idx, quant, vT, pA, t0P)

    # Cadastro(Adicionar)
    if eventos == 'CadastroProduto':
        janela3 = janelaCadastro(mdV, mdC)
        janela2["comboProdutos"].Update(values=pC)

    #Excluir(Adicionar)
    if eventos == 'excluirTBEstoque':
        vT, t0P, pA = ExC(pA, janela, valores, vT, t0P)

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
        tabelas = EfCad(tabelas, valores, path)

    # Fechar Programa(Cadastro)
    if eventos == sg.WINDOW_CLOSED and janela == janela3:
        janela3.hide()

    # Vender Produto
    if eventos == 'Vender Produto':
        eP, vP = '', ''
        pEV = listaProdutos(tabelas[2],1)
        janela4 = janelaVender(pEV, pAV, eP, vP)

    #Carrinho(Vender)
    if eventos == 'ContinuarVenda':
        CarVenda(tabelas,valores, janela, pE, pAV, vTV, t0P)




    # Ir para janela Vender Produto
    # if eventos == 'Vender Produto':
    #     janela4 = janelaVender()

    # Fechar Programa
    if eventos == sg.WINDOW_CLOSED and janela == janela1 or eventos == 'Sair':
        break
janela.close()