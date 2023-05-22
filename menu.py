import util
import controller

menuItens = {
    '1': {
        'title' : 'Cadastrar Produto',
        'function': controller.cadastrarProduto
    },
    '2': {
        'title' : 'Consultar Produto',
        'function' : controller.consultarProduto
    },
    "3": {
        'title': "Listar produtos",
        'function': controller.listarProdutos
    },   
    '4': {
        'title' : 'Atualizacao de Produto',
        'function' : controller.atualizarProduto
    },
    '5': {
        'title' : 'Cadastrar Movimentação',
        'function' : controller.cadastrarMovimentacoes
    },
    '6': {
        'title' : 'Calcular valor total do estoque',
        'function' : controller.calcularValorTotal
    },
    '7': {
        'title' : 'Exportar o estado atual do estoque',
        'function' : controller.exportarEstoque
    },
    '8':{
        'title' : 'Grafico de movimentação de estoque do produto',
        'function' : controller.graficoMovEstoque
    },
    "9": {
        'title': "Grafico de valor total do estoque",
        'function': controller.graficoValorEstoque
    },
    "10": {
        'title': "Grafico valor total por produto",
        'function': controller.graficoValorProduto
    }
}


def montar():
    util.clearConsole()
    for key, value in menuItens.items():
        title = value['title']
        print(f'{key}. {title}')

    print('99. Sair')

def obterFuncao(opcao):
    return menuItens[opcao]['function']

def ehOpcaoValida(opcao):
    return opcao in menuItens