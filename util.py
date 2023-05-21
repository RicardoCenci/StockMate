import os

def clearConsole():
    os.system('cls');


def isNumeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def verifyValidInput(value, predicate):
    result = predicate(value)
    if(not result):
        print(f'\'{value}\' não é um valor valido\n')
    return result
    
def getInput(message):
    try:
        value = input(message + '\t(CTRL + Z para cancelar)\n')
    except EOFError:
        raise OperacaoCancelada()

    return value

def inputUntilValid(message, predicate):
    value = getInput(message)

    while(not verifyValidInput(value, predicate)):
        value = getInput(message)

    return value


def pprint(message, indent = 0):
    print('\t' * indent + message)


class OperacaoCancelada(Exception):
    def __init__(self, message="Operação cancelada"):
        super().__init__(message)


def obterMeses():
    return [
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out'
        'Nov',
        'Dez',
    ]