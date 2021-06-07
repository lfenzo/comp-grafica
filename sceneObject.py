"""
Classe responsável por implementar um objeto em cena, assim como o seu sistema de coordenadas
transformações e salvar o objeto para o disco.
"""

import numpy as np

from transformations import Transformer


def read_obj(filepath) -> dict:
    """
    Le um arquivo .obj e carrega o seu conteúdo para a memória
    """

    obj_info = {}

    with open(filepath, 'r') as obj_file:

        for index, line in enumerate(obj_file.readlines()):

            data_type, *info = line.replace('\n', '').split(' ')
            info = list(map(float, info))

            if data_type not in obj_info.keys():
                obj_info[data_type] = {} if data_type == 'v' else []

            if data_type == 'v': obj_info[data_type][index] = np.array(info)
            else:
                obj_info[data_type].append(info)

    return obj_info

def save_obj(filepath: str, obj_info: dict):
    """
    Salva um objeto em um arquio .obj utilizando apenas os seus dados (obj_info)

    Similar à função sceneObject::to_obj mas sem que seja necessario instanciar um objeto
    """

    with open(filepath, 'w') as obj_file:

        for key in obj_info.keys():
            if key == 'v':
                for vertex in obj_info[key].values():
                    obj_file.write(f'v {vertex[0]} {vertex[1]} {vertex[2]}\n')

            else:
                for item in obj_info[key]:
                    to_write = f'{key}'
                    for i in item:
                        to_write += f' {int(i)}'

                        obj_file.write( f'{to_write}\n' )


class sceneObject:

    def __init__(self, filepath = None, obj_info = None):
        """
        Inicializa um umjeto da cena ou carregando diretamente os dados de
        um arquivo .obj ou recebe as informações de um arquivo .obj que já
        foi carregado.

        Parametros
        ----------
        `filepath`: arquivo .obj a ser carregado para as informações do objeto.
        `obj_info`: dicionário com as informações sobre o objeto (ver read_obj)
        """

        if filepath != None and obj_info == None:
            self.__obj_info = read_obj(filepath)

        elif filepath == None and obj_info != None:
            if isinstance(obj_info, dict):
                self.__obj_info = obj_info
            else:
                raise ValueError(f'O atributo \'obj_info\' deve ser um dicionário. Foi passado: \'{type(obj_info)}\'.')

        else:
            raise ValueError('Ou o atributo \'filepathz\' ou o atributo \'obj_info\' devem ser passados.')

    def transform(self, seq: list) -> dict:
        """
        Recebe uma sequencia de trasformações em uma lista que geram uma matriz de
        transformação a ser aplicada em cada um dos pontos do objeto.

        Não é inplace!

        Parametros
        -------------
        `seq`: sequencia de transformações no formato ('tipo', tx, ty, tz)
        """

        transformed_object = self.__obj_info
        transformed_object['v'] = Transformer().transform(obj_matrix = self.__obj_info['v'],
                                                       seq = seq)
        return transformed_object

    def get_obj_info(self):
        """
        Encapsula a obtanção dos informações sobre o objetol
        """

        return self.__obj_info

    def to_obj(self, filepath) -> None:
        """
        Salva as informações do objeto (vertices, faces, etc) em um arquivo .obj.

        Parametros
        ----------
        `filepath`: nome do arquivo a ser salvo
        """

        with open(filepath, 'w') as obj_file:

            for key in self.__obj_info.keys():
                if key == 'v':
                    for vertex in self.__obj_info[key].values():
                        obj_file.write(f'v {vertex[0]} {vertex[1]} {vertex[2]}\n')

                else:
                    for item in self.__obj_info[key]:
                        to_write = f'{key}'
                        for i in item:
                            to_write += f' {int(i)}'

                        obj_file.write( f'{to_write}\n' )

