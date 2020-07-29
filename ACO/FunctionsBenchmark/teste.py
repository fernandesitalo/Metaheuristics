import shutil
from os import listdir
from os.path import isfile, join, basename



pathOrigem = "/home/italofernandes/mygit/Metaheuristics/ACO/FunctionsBenchmark/Vrp-Set-A"
pathDestino = "/home/italofernandes/mygit/Metaheuristics/ACO/FunctionsBenchmark/sol"



def move(path_origem, path_destino):
    for item in [join(path_origem, f) for f in listdir(path_origem) if isfile(join(path_origem, f)) ]:
        if ".sol" in item:
            shutil.move(item, join(path_destino, basename(item)))
            print('moved "{}" -> "{}"'.format(item, join(path_destino, basename(item))))


if __name__ == '__main__':
    move(pathOrigem, pathDestino)
    # ~ dirs = listdir( pathOrigem )
    # ~ for pasta in dirs:
        # ~ if ".sol" in pasta:
            # ~ pathPasta = pathOrigem + "/" + pasta
            # ~ move(pathPasta,pathDestino)
