import util
import dados
import menu

isRunning = True
dados.carregarPlanilha()

while(isRunning):
    menu.montar()

    opcao = input()

    if(opcao == '99'):
        isRunning = False
        continue

    if(not menu.ehOpcaoValida(opcao)):
        print('Opcao invalida')
        input('Enter para continuar')
        continue

    try:
        menu.obterFuncao(opcao)()
    except util.OperacaoCancelada:
        util.pprint('Operacao cancelada')