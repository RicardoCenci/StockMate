
import os
import pandas as pd
from util import isNumeric
import datetime

produtos = []
movimentacoes = []

def ensureDirectoryExists(directory):
  if not os.path.exists(directory):
      os.makedirs(directory)
    
def readOrCreate(fileName, columns):
    try:
        csvHandle = pd.read_csv(fileName)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        criarPlanilhaDefault(fileName, columns)
        return readOrCreate(fileName, columns)
    
    return csvHandle

def carregarPlanilha():
    ensureDirectoryExists('dados')
    produtoDF = readOrCreate('dados/produtos.csv', ['id', 'nome', 'valor'])

    for index, row in produtoDF.iterrows():

        produtos.append(row.to_dict())


    movimentacoesDF = readOrCreate('dados/movimentacoes.csv', ['id', 'idProduto', 'tipo', 'quantidade', 'data'])

    for index, row in movimentacoesDF.iterrows():
        movimentacoes.append(row.to_dict())


def criarPlanilhaDefault(filename, colunas):
     with open(filename, 'w+') as csvFileHandle:
            csvFileHandle.write(','.join(colunas))
            csvFileHandle.close()

def salvarPlanilhaProduto():
    pd.DataFrame(produtos).to_csv('dados/produtos.csv', index='id', columns=['id', 'nome', 'valor'])

def salvarPlanilhaMovimentacoes():
    pd.DataFrame(movimentacoes).to_csv('dados/movimentacoes.csv', index='id', columns=['id', 'idProduto', 'tipo', 'quantidade', 'data'])

def salvarPlanilhas():
  salvarPlanilhaProduto()
  salvarPlanilhaMovimentacoes()


def obterProdutos():
    return produtos

def obterMovimentacoes():
    return movimentacoes

def obterProdutoPorId(id):
    for produto in produtos:
        if(int(produto['id']) == int(id)):
            return produto

    return None

def obterMovimentacaoPorId(id):
    for movimentacao in movimentacoes:
        if(movimentacao['id'] == id):
            return movimentacao

    return None

def obterQuantidadeProduto(id):
    produto = obterProdutoPorId(id)
    if(not produto):
        return 0
    
    movimentacoes = obterMovimentacoesPorProduto(id)
    quantidadeProduto = 0
    for movimentacao in movimentacoes:
        qtd = float(movimentacao['quantidade']) if movimentacao['tipo'] == 'entrada' else -float(movimentacao['quantidade'])
        quantidadeProduto += qtd
    
    return quantidadeProduto

def obterMovimentacoesPorProduto(id):
    movimentacoesProduto = []
    for movimentacao in movimentacoes:
        if(int(movimentacao['idProduto']) == int(id)):
            movimentacoesProduto.append(movimentacao)

    return movimentacoesProduto

def insertMovimentacao(idProduto, tipo, quantidade):
  id = len(movimentacoes) + 1

  movimentacoes.append({
    'id': id,
    "idProduto" : int(idProduto),
    'tipo' : tipo,
    'quantidade': float(quantidade),
    'data' : datetime.datetime.now() 
  })
  salvarPlanilhaMovimentacoes()

def saveProduto(id, produto):
    if isNumeric(id) and id != 0:
        return alterarProduto(id, produto)
    
    id = len(produtos) + 1
    produto['id'] = id
    produto['valor'] = float(produto['valor']) if isNumeric(produto['valor']) else 0
    produtos.append(produto)

    salvarPlanilhaProduto()

def alterarProduto(id, produto):
    produto['id'] = id
    for index, produto in enumerate(produtos):
        if produto['id'] == id:
            produtos[index] = produto
            salvarPlanilhaProduto()
            return produto
    
    return None

def isValidMovimentacao(v):
  return v.lower() in ['saida', 'entrada']


def isValidProductID(id):
    if(not isNumeric(id)):
        return False

    produto = obterProdutoPorId(id)
    return bool(produto)
