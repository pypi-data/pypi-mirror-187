import os
import importlib
from platform import platform


def readRequirements():
    with open("requirements.txt", "r") as file:
        file = file.read()
        requirements = file.split('\n')
    return requirements


def reqcheq(verbose = False):
    requirements = readRequirements()
    for requirement in requirements:
        if verbose:
            print(f'Verificando requerimento: {requirement}')
        names = requirement.split()
        if len(names) > 1:
            install_name, import_name = names[1], names[0]
            try:
                installModule(install_name, import_name)
                if verbose:
                    print(f'Módulo já instalado: {requirement}')
            except Exception as error:
                print(f'Não foi possivel baixar o modulo: {requirement}')
                if verbose:
                    print(f'Erro: {error}')
        else:
            try:
                installModule(requirement, requirement)
                if verbose:
                    print(f'Módulo já instalado: {requirement}')
            except Exception as error:
                print(f'Não foi possivel baixar o modulo: {requirement}')
                if verbose:
                    print(f'Erro: {error}')


def installModule(install_name, import_name):

    system = platform().split('-')[0]

    try:
        module = importlib.import_module(import_name)
        # print(f'Modulo {import_name} ja instalado')
        return True
    except:
        print(f'Modulo nao encontrado: {import_name}')
        print(f'Tentando instalar automaticamente')
        try:
            if not system == 'Linux':
                os.system(f'pip install {install_name}')
            else:
                os.system(f'pip3 install {install_name}')
            print(f'Modulo instalado: {install_name}')
            return True
        except:
            return False

if __name__ == '__main__':
    reqcheq()
