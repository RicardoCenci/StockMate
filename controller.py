from util import pprint
from dateutil import parser
import matplotlib.pyplot as plt
import util
import dados

def cadastrarProduto():
    nome = util.getInput('Nome do produto')
    valor = util.inputUntilValid('Valor do produto', util.isNumeric)
  
    dados.saveProduto(0, {
        'id': id,
        'nome': nome,
        'valor': valor,
    })

def consultarProduto():
    idProduto = util.inputUntilValid('ID do produto', dados.isValidProductID)
    produto = dados.obterProdutoPorId(idProduto)

    pprint(f'Produto: {produto["nome"]}')
    pprint(f'Valor: {produto["valor"]}', 1)
    quantidade = dados.obterQuantidadeProduto(produto['id'])
    pprint(f'Quantidade: {quantidade}', 1)

    input('\nContinuar')


def cadastrarMovimentacoes():
  tipoMovimentacao = util.inputUntilValid('Tipo de movimentação (saida/entrada)', dados.isValidMovimentacao)
  idProduto = util.inputUntilValid('ID do produto', dados.isValidProductID)
  qtdMovimentacao = util.inputUntilValid("Quantidade de produtos da movimentação\n", util.isNumeric)

  dados.insertMovimentacao(idProduto, tipoMovimentacao, qtdMovimentacao)

def atualizarProduto():
    idProduto = util.inputUntilValid('ID do produto', dados.isValidProductID)
    produto = dados.obterProdutoPorId(idProduto)
    campos = ['nome', 'valor'];
    campo = input('Qual campo deseja atualizar? ' + f'{"/".join(campos)}')

    if campo not in campos:
        print('Campo invalido')
        return

    valor = input(f'Novo {campo}: ')
    produto[campo] = valor
    dados.saveProduto(produto['id'], produto)

def calcularValorTotal():
    produtos = dados.obterProdutos()
    total = 0
    for produto in produtos:
        qtd = dados.obterQuantidadeProduto(produto['id'])
        total += float(produto['valor']) * qtd
    print(f'Total: R$ {total}')
    input('Continuar')

def exportarEstoque():
    output = input("Nome do arquivo de saida: ")
    produtos = dados.obterProdutos()

    with open(output + '.csv', 'w') as file:
        file.write('id;nome;valor;quantidade\n')
        for produto in produtos:
            qtd = dados.obterQuantidadeProduto(produto['id'])
            file.write(f"{produto['id']};{produto['nome']};{produto['valor']};{qtd}\n")

    print(f'Arquivo {output}.csv gerado com sucesso')
    input('Continuar')

def graficoMovEstoque():
    idProduto = util.inputUntilValid('ID do produto', dados.isValidProductID)

    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    movimentacoes = dados.obterMovimentacoesPorProduto(idProduto)
    for movimentacao in movimentacoes:
        dataMovimentacao = parser.parse(movimentacao['data']) 
        mes = dataMovimentacao.month
        y[mes - 1] += movimentacao['quantidade'] if movimentacao['tipo'] == 'entrada' else -movimentacao['quantidade']

    plt.plot(util.obterMeses(), y)
    plt.xlabel('Mês')
    plt.ylabel('Saldo')
    plt.title('Saldo de movimentação do produto')
    plt.show()

def graficoValorEstoque():
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    produtos = dados.obterProdutos()

    for produto in produtos:
        movimentacoes = dados.obterMovimentacoesPorProduto(produto['id'])

        for movimentacao in movimentacoes:
            dataMovimentacao = parser.parse(movimentacao['data']) 
            mes = dataMovimentacao.month
            quantidade = movimentacao['quantidade'] if movimentacao['tipo'] == 'entrada' else -movimentacao['quantidade'];
            y[mes - 1] += float(produto['valor']) * float(quantidade)

    plt.plot(util.obterMeses(), y)
    plt.xlabel('Mês')
    plt.ylabel('Valor Total')
    plt.title('Valor total do estoque')
    plt.show()

def graficoValorProduto():
    y = []
    x = []
    produtos = dados.obterProdutos()

    for produto in produtos:
        movimentacoes = dados.obterMovimentacoesPorProduto(produto['id'])
        id = produto['id']
        x.append(produto['nome'] + f'({id})')
        y.append(0)
        idxProduto = len(x) - 1

        for movimentacoes in movimentacoes:
            quantidade = movimentacoes['quantidade'] if movimentacoes['tipo'] == 'entrada' else -movimentacoes['quantidade'];
            y[idxProduto] += float(produto['valor']) * float(quantidade)

    plt.bar(x, y)
    plt.xlabel('Produto')
    plt.ylabel('Valor Total')
    plt.title('Valor total do estoque por produto')
    plt.show()

def listarProdutos():
    produtos = dados.obterProdutos()
    for produto in produtos:
        pprint(f'ID: {produto["id"]}')
        pprint(f'Nome: {produto["nome"]}', 1)
        pprint(f'Valor: {produto["valor"]}', 1)
        quantidade = dados.obterQuantidadeProduto(produto['id'])
        pprint(f'Quantidade: {quantidade}', 1)
        print('--------------------------------------------------------')
    input('Continuar')