import PySimpleGUI as sg
import pandas as pd
from Funções import listaProdutos, listarVC, listarBusca, listaEstoque, listarID
from datetime import date
from Adicionar import *
from Cadastrar import *
from Vender import *
from Historico import *
from Estatisticas import *
from EditarProduto import *
from Estoque import *

# Pandas
path = "Arquivos/Compras.xlsx"
try:
    dDf=pd.read_excel(path, sheet_name=['Métodos', 'Produtos', 'P_Vendas', 'Vendas', 'P_Compras', 'Compras', 'Estoque'])
    tabelas = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),
               pd.DataFrame()]
    tabelas[0] = dDf.get('Métodos')
    tabelas[1] = dDf.get('Produtos')
    tabelas[2] = dDf.get('P_Vendas')
    tabelas[3] = dDf.get('Vendas')
    tabelas[4] = dDf.get('P_Compras')
    tabelas[5] = dDf.get('Compras')
    tabelas[6] = dDf.get('Estoque')
    print("Arquivo Encontrado\n\n")
    print("\n\nMétodos\n"+str(tabelas[0]))
    print("\n\nProdutos\n"+str(tabelas[1]))
    print("\n\nProduto_Vendas\n"+str(tabelas[2]))
    print("\n\nVendas\n"+str(tabelas[3]))
    print("\n\nProduto_Compras\n"+str(tabelas[4]))
    print("\n\nCompras\n"+str(tabelas[5]))
    print("\n\nEstoque\n"+str(tabelas[6]))
except FileNotFoundError as fnfe:
    dDf = pd.read_excel("Arquivos/Compras_Backup.xlsx",
                        sheet_name=['Métodos', 'Produtos', 'P_Vendas', 'Vendas', 'P_Compras', 'Compras', 'Estoque'])
    tabelas = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),
               pd.DataFrame()]
    tabelas[0] = dDf.get('Métodos')
    tabelas[1] = dDf.get('Produtos')
    tabelas[2] = dDf.get('P_Vendas')
    tabelas[3] = dDf.get('Vendas')
    tabelas[4] = dDf.get('P_Compras')
    tabelas[5] = dDf.get('Compras')
    tabelas[6] = dDf.get('Estoque')
    print("Arquivo Não Encontrado, colocando backup\n\n")
    print("\n\nMétodos\n"+str(tabelas[0]))
    print("\n\nProdutos\n"+str(tabelas[1]))
    print("\n\nProduto_Vendas\n"+str(tabelas[2]))
    print("\n\nVendas\n"+str(tabelas[3]))
    print("\n\nProduto_Compras\n"+str(tabelas[4]))
    print("\n\nCompras\n"+str(tabelas[5]))
    print("\n\nEstoque\n"+str(tabelas[6]))

# Data
data_em_texto = date.today().strftime('%d/%m/%Y')

# PySimpleGUI

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


janelaP = janelaInicial()
janelaEst, janelaA, janelaV, janelaH, janelaE, janelaEP = None, None, None, None, None, None
janelaC, janelaV2, janelaEPC, janelaRP = None, None, None, None

# Provisórios
tPP = tabelas[1].copy()
tP_VP = tabelas[2].copy()
tVP = tabelas[3].copy()
tP_CP = tabelas[4].copy()
tEP = tabelas[6].copy()

# Ids
iDc = listarID(tabelas[4])
if iDc == 1:
    iDc = 10000
iDv = listarID(tabelas[2])

# Métodos
mdV = listaMetodos(tabelas[0])
mdC = mdV.copy()

# Produtos adicionados em table
pA = []
pAV = []
pAHC = []
pAHV = []
pC = listaProdutos(tabelas[1], 0)
pV = listaProdutos(tabelas[1], 1)
cEH, vEH = listarVC(tabelas[5]), listarVC(tabelas[3])
pEd = []

# Valor Total
vT = 0
vTV = 0

eV = 0
vBC = False
editTBidx = 0
editTBn = 0


# Ler os eventos
while True:
    janela, eventos, valores = sg.read_all_windows()

    # PRINCIPAL
    if janela == janelaP:
        # Adicionar Produto
        if eventos == 'Adicionar Produto':
            janelaA = janelaAdicionar(tabelas[1], pA)

        # Vender Produto
        if eventos == 'Vender Produto':
            janelaV = janelaVender(pAV, tabelas[1])

        # Histórico
        if eventos == 'Histórico':
            cEH, vEH = listarVC(tabelas[5]), listarVC(tabelas[3])
            janelaH = janelaHistorico(vEH, cEH)

        # Estatísticas
        if eventos == 'Estatísticas':
            janelaE = janelaEstatistica()
            Estatisticas(tabelas, janelaE, data_em_texto)

        # Editar Produto
        if eventos == 'Editar Produto':
            pEd = listaProdutos(tabelas[1], 2)
            janelaEP = janelaEditProduto(pEd)

        # Estoque
        if eventos == 'Estoque':
            janelaEst = janelaEstoque(tabelas[6])

        # Fechar Programa
        if janela == janelaP and eventos == sg.WINDOW_CLOSED or eventos == 'Sair':
            break

    # ADICIONAR
    if janela == janelaA:

        # Fechar Programa(Adicionar)
        if eventos == sg.WINDOW_CLOSED and janela == janelaA:
            janelaA['comboProdutos'].Update('')
            janelaA["quantidadeAdicionada"].Update('')
            janelaA.close()

        # Selecionar Produto(Adicionar)
        if eventos == 'comboProdutos':
            SePr(tabelas, valores, janela, tEP)

        # Carrinho(Adicionar)
        if eventos == 'continuarCompra':
            if valores['comboProdutos'] not in pC:
                messagebox.showwarning("Erro ao Adicionar",
                                       'Selecione um produto para adicionar')
            else:
                if valores['quantidadeAdicionada'] == "":
                    messagebox.showwarning("Erro ao Adicionar",
                                           'Adicione um número no campo Quantidade')
                else:
                    try:
                        if not int(valores['quantidadeAdicionada']) >= 0:
                            messagebox.showwarning("Erro ao Adicionar",
                                                   'Valor abaixo de 0 em campo Quantidade')
                        else:
                            pA, vT, tP_CP, tEP = CarAd(tabelas, valores, janela, tP_CP, pA, vT, iDc, tEP)
                    except ValueError as ve:
                        messagebox.showwarning("Erro ao Adicionar",
                                               'O campo Quantidade apenas aceita Números')
            # Feito

        # Cadastro(Adicionar)
        if eventos == 'CadastroProduto':
            janelaC = janelaCadastro(mdV, mdC)

        # Excluir(Adicionar)
        if eventos == 'excluirTBEstoque':
            data_selected = [pA[row] for row in valores['-TB-']]
            if data_selected == []:
                messagebox.showwarning("Erro ao Excluir",
                                       'É preciso selecionar um produto na tabela antes de Excluir')
            else:
                vT, tP_CP, pA, tEP = ExC(tabelas, pA, janela, valores, vT, tP_CP, tEP, data_selected)

        # Finalizar(Adicionar)
        if eventos == 'Concluir':
            if pA != []:
                tabelas = FinalizarAd(tP_CP, tabelas, path, iDc, data_em_texto, tEP)
                iDc += 1
                vT = 0
                pA = []
                janelaA.close()
                janelaP.un_hide()
            else:
                messagebox.showwarning("Erro ao Finalizar Compra",
                                       "Selecione ao menos um produto")

        # Voltar(Adicionar)
        if eventos == 'voltarA':
            vT = 0
            pA = []
            tEP = tabelas[6].copy()
            tP_CP = tabelas[4].copy()
            janelaA.close()
            janelaP.un_hide()

    # VENDER
    if janela == janelaV:

        # Fechar Programa(Vender)
        if eventos == sg.WINDOW_CLOSED and janela == janelaV:
            janelaV.close()

        # Selecionar Produto(Vender)
        if eventos == 'tiposProdutos':
            eV = SePrV(tabelas, valores, janela, tEP)
            # Feito

        # Carrinho(Vender)
        if eventos == 'continuarVCompra':
            if valores['tiposProdutos'] != '':
                if not valores['quantidadeAdicionadaV'] == "":
                    try:
                        if int(valores['quantidadeAdicionadaV']) >= 0:
                            if eV == 1:
                                vTV, tP_VP, pAV, tEP, janelaRP, pRE = CarVenda(tabelas, valores, janela, pAV, vTV,
                                                                               tP_VP,
                                                                               iDv, tEP)
                            else:
                                messagebox.showwarning("Erro ao Adicionar ao Carrinho",
                                                       'Estoque Vazio')
                        else:
                            messagebox.showwarning("Erro ao Adicionar ao Carrinho",
                                                   'Valor abaixo de 0 não é aceito')
                    except ValueError as ve:
                        messagebox.showwarning("Erro ao Adicionar ao Carrinho",
                                               'O campo Quantidade apenas aceita Números')
                else:
                    messagebox.showwarning("Erro ao Adicionar ao Carrinho",
                                           'Valor inválido no campo "Quantidade"')
            else:
                messagebox.showwarning("Erro ao Adicionar ao Carrinho",
                                       'Selecione um produto para adicionar')

        # Excluir Elemento Table(Vender)
        if eventos == 'excluirTBEstoqueV':
            data_selected = [pAV[row] for row in valores['tV_produtos']]
            if data_selected == []:
                messagebox.showwarning("Impossível Deletar Dado",
                                       'Precisa Selecionar o Dado na Tabela antes de Deletar')
            else:
                vTV, tP_VP, pAV, tEP = ExcV(tabelas, pAV, janela, valores, vTV, tP_VP, tEP, data_selected)

        # Finalizar(Venda)
        if eventos == "FinalizarVenda":
            if pAV != []:
                janelaV2 = janelaVender2(vTV)
                janelaV.hide()
            else:
                messagebox.showwarning("Erro ao Finalizar",
                                       "Não há produtos a vender para poder Finalizar")

        # Voltar(Vender)
        if eventos == 'voltarV':
            pAV = []
            vTV = 0
            tEP = tabelas[6].copy()
            tP_VP = tabelas[2].copy()
            janelaV.hide()
            janelaP.un_hide()

    # VENDER 2
    if janela == janelaV2:
        # Voltar(Vender2)
        if eventos == 'voltarV2':
            janelaV2.hide()
            janelaV.un_hide()

        #Fechar Guia
        if sg.WINDOW_CLOSED:
            janelaV2.close()

        # Finalizar Parte 2
        if eventos == 'concluirV':
            if valores['comboPag'] != '':
                tabelas = FinalizarVpt2(valores, tP_VP, tabelas, path, data_em_texto, iDv, tEP)
                iDv += 1
                pAV = []
                vTV = 0
                janelaV2.close()
                janelaV.close()
            else:
                messagebox.showwarning("Erro ao Finalizar",
                                       "Selecione o Método de Pagamento")

        # Atualizar Desconto (Finalizar Pt2)
        if eventos == 'desconto':
            AtualizarDesconto(valores, janela, vTV)
            # Finalizado

    # Repor Estoque
    if janela == janelaRP:
        # Voltar Repor Estoque
        if eventos == 'voltarRP':
            janelaRP.close()
            janelaV.un_hide()

        if eventos == 'selecRP':
            if valores['comboRepor'] == '':
                messagebox.showwarning("Erro ao Repor",
                                       'Selecione um produto para repor outro produto')
            else:
                if valores['retiradoRE'] == "" or valores['adicionarRE'] == "":
                    messagebox.showwarning("Erro ao Repor",
                                           'Adicione um número nos campos')
                else:
                    try:
                        if not int(valores['retiradoRE']) >= 0 and not int(valores['adicionarRE']) >= 0:
                            messagebox.showwarning("Erro ao Repor",
                                                   'Valor abaixo de 0 nos campos')
                        else:
                            prov = valores['comboRepor'].split('-')
                            n_condicao = (tEP['Produto'] == prov[0]) & (tEP['Marca'] == prov[1]) & \
                                         (tEP['Método'] == prov[2])
                            iDX = tEP.loc[n_condicao, :].index[0]
                            valorRepATirar = int(tEP.at[iDX, 'Quantidade'])
                            valorRepTirar = int(valores['retiradoRE'])
                            tirado = valorRepATirar - valorRepTirar
                            tEP.at[iDX, 'Quantidade'] = tirado
                            n_condicao = (tEP['Produto'] == pRE[1]) & (tEP['Marca'] == pRE[2]) & \
                                         (tEP['Método'] == pRE[3])
                            iDX = tEP.loc[n_condicao, :].index[0]
                            valorRepATirar = int(tEP.at[iDX, 'Quantidade'])
                            valorRepTirar = int(valores['adicionarRE'])
                            tirado = valorRepATirar + valorRepTirar
                            tEP.at[iDX, 'Quantidade'] = tirado
                            janelaRP.close()
                    except ValueError as ve:
                        messagebox.showwarning("Erro ao Repor",
                                               'Os campos apenas aceitam Números')

    # Histórico
    if janela == janelaH:

        # Fechar Histórico
        if eventos == sg.WINDOW_CLOSED and janela == janelaH:
            janelaH.hide()

        # Voltar(Histórico)
        if eventos == 'voltarH':
            janelaH.hide()
            janelaP.un_hide()

        # Voltar(Histórico 2)
        if eventos == 'voltarH2':
            janelaH.close()
            janelaH = janelaHistorico(vEH, cEH)

        # Buscar (Histórico)
        if eventos == 'bPesquisar':
            listarBusca(tabelas, valores['inputIDH'], valores['inputQI'], valores['inputDT'], valores['inputVT'],
                        janela)

        # Selecionar Table(Histórico)
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
            if id_ExcluirV == None:  # Compra
                metodo, tabelas = ExcluirCompraVenda(tabelas, valores, 4, id_ExcluirC, janela, path)
            else:  # Venda
                metodo, tabelas = ExcluirCompraVenda(tabelas, valores, 2, id_ExcluirV, janela, path)
            tEP = tabelas[6].copy
            janelaH.close()
            vEH = listarVC(tabelas[3])
            cEH = listarVC(tabelas[5])
            janelaH = janelaHistorico2(tabelas, metodo, array[0])

    # Estatística
    if janela == janelaE:
        # Fechar Estatistica
        if eventos == sg.WINDOW_CLOSED and janela == janelaE:
            janelaE.close()

    # Editar Produto
    if janela == janelaEP:

        # Fechar Editar Produto
        if eventos == sg.WINDOW_CLOSED and janela == janelaEP:
            janelaEP.close()

        # Mudar Visibilidade Metodo Venda(Cadastro)
        if eventos == 'buttonMetodoVenda':
            vBC = visCad(vBC, janela)
            # Feito

        # Confirmar novo Método de Venda(Cadastro)
        if eventos == 'novoMetodoVenda' and not valores['novoMetodoVendaInput'] == '':
            mdV, mdC, tabelas = NewM(tabelas, valores, janela, path, mdV, mdC)
            # Feito

        # Selecionar Produto(Editar Produto)
        if eventos == '-TBEP-':
            janelaEP.close()
            janelaEP = janelaCadastro(mdV, mdC)
            selProd(tabelas[0], janelaEP, pEd[valores['-TBEP-'][0]])
            idxPCEP = valores['-TBEP-'][0]

        # Voltar(Cadastro- Editar Produto)
        if eventos == 'voltarC' and janela == janelaEP:
            janelaEP.close()
            janelaEP = janelaEditProduto(pEd)

        # Ao finalizar retira um produto e adiciona outro
        if eventos == 'EfetuarCadastro':
            current = valores['metodoVenda']
            current2 = valores['metodoCompra']
            if current != []:
                if current2 != []:
                    if valores["Prod"] == "" or valores["valorMVenda"] == "" or valores['MarcaProduto'] == "" or \
                            valores["valorMCompra"] == "":
                        messagebox.showwarning("Preencha Todos os campos",
                                               'Preencha os campos corretamente')
                    else:
                        try:
                            tabelas = FinalizarEdit(tabelas, idxPCEP, valores, janela, path)
                            janelaEP.close()
                            pCEP = listaProdutos(tabelas[1], 2)
                            janelaEP = janelaEditProduto(pCEP)
                        except ValueError as ve:
                            messagebox.showwarning("Erro ao Cadastrar",
                                                   'O campo Valor do Produto apenas aceita Números')
                else:
                    messagebox.showwarning("Preencha Todos os campos",
                                           'Preencha o campo de Método de Compra')
            else:
                messagebox.showwarning("Preencha Todos os campos",
                                       'Preencha o campo de Método de Venda')


    # Estoque
    if janela == janelaEst:
        #Fechar Estoque
        if eventos == sg.WINDOW_CLOSED and janela == janelaEst:
            janelaEst.hide()

    # CADASTRO
    if janela == janelaC:
        # Mudar Visibilidade Metodo Venda(Cadastro)
        if eventos == 'buttonMetodoVenda':
            vBC = visCad(vBC, janela)
            # Feito

        # Confirmar novo Método de Venda(Cadastro)
        if eventos == 'novoMetodoVenda' and not valores['novoMetodoVendaInput'] == '':
            mdV, mdC, tabelas = NewM(tabelas, valores, janela, path, mdV, mdC)
            # Feito

        # Adicionar Produto Cadastro(Cadastro)
        if eventos == 'EfetuarCadastro':
            current = valores['metodoVenda']
            current2 = valores['metodoCompra']
            if current != []:
                if current2 != []:
                    if valores["Prod"] == "" or valores["valorMVenda"] == "" or valores['MarcaProduto'] == "" or \
                       valores["valorMCompra"] == "":
                        messagebox.showwarning("Preencha Todos os campos",
                                               'Preencha os campos corretamente')
                    else:
                        try:
                            tabelas, pC, tEP = EfCad(tabelas, valores, janela, path, tEP)
                            janelaA['comboProdutos'].Update(values=pC)
                            janelaC.hide()
                        except ValueError as ve:
                            messagebox.showwarning("Erro ao Cadastrar",
                                                   'O campo Valor do Produto apenas aceita Números')
                else:
                    messagebox.showwarning("Preencha Todos os campos",
                                           'Preencha o campo de Método de Compra')
            else:
                messagebox.showwarning("Preencha Todos os campos",
                                       'Preencha o campo de Método de Venda')

        # Fechar Programa(Cadastro)
        if eventos == sg.WINDOW_CLOSED and janela == janelaC:
            janelaC.hide()
            # Feito

        # Voltar(Cadastro)
        if eventos == 'voltarC' and janela == janelaC:
            janelaC.hide()
            janelaA.un_hide()

janela.close()
