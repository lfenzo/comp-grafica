"""
Classe responsável por realizar as transformações lineares nas coordenadas dos objetos.

Transformações possíveis:
    - 'mov': translador objeto com deslocamentos dx, dy, dz
    - 'rot': rotacionar objeto com rotações rx, ry, rz
    - 'scl': mudar escala do objeto com proporções sx, sy, sz

Formato a ser utilizado em cada item da sequencia de transformações: ( tipe, arg1, arg2, arg3 )

Esta API deve ser transferida sem alterações para as demais classes que fazem uso das
transformações implementadas aqui.
"""

import numpy as np

class Transformer:

    def __init__(self):
        self.__identity = np.array([ [1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, 1] ])

        self.__transf_methods = {
            'mov': self.__move,
            'rot': self.__rotate,
            'scl': self.__scale
        }


    def transform(self, obj_matrix: 'array com pontos tridimensionais', seq: list) -> dict:
        """
        Realiza várias transformações em sequencia no objeto desejado

        Retorna
        --------
        - dicionário de vertices no formato { 1: np.array([x1, y1, z1]), 2: np.array([x2, y2 z2]) ... }
        """

        vertices_to_transform = [vertex for index, vertex in obj_matrix.items()]

        # obtem a primeira matrix de transformaão 4x4.
        first_transf = seq.pop()
        transf_matrix = self.__transf_methods[ first_transf[0] ](self.__identity,
                                                                 first_transf[1], first_transf[2], first_transf[3])

        # realiza as transformações em cadeia começando pela ultima e info para a primeira
        for transf in reversed(seq):
            transf_matrix = self.__transf_methods[ transf[0] ](transf_matrix, transf[1], transf[2], transf[3])

        # aplica a matriz resultante nas coordenadas dos vertices do objeto
        transformed_vertices = self.__apply(vertices_to_transform, transf_matrix)

        # retorna um dicionário no mesmo formato que foi fornecido como parâmetro da função
        return {index: vertex for index, vertex in enumerate(transformed_vertices)}


    def __apply(self, obj_matrix, transf_matrix):

        transformed_coords = []

        for vertex in obj_matrix:
            vertex_matrix = np.concatenate( (vertex, np.array([1])) )
            transformed_coords.append( np.matmul(transf_matrix, vertex_matrix)[:-1] )

        return transformed_coords


    def __move(self, input_matrix, dx, dy, dz):
        """
        Mesmo que transladar (trans ladar, ir para o outro lado)
        """
        transf_matrix = np.array([ [1, 0, 0, dx],
                                   [0, 1, 0, dy],
                                   [0, 0, 1, dz],
                                   [0, 0, 0,  1]])

        return np.matmul(input_matrix, transf_matrix)


    def __rotate(self, input_matrix, rx = 0, ry = 0, rz = 0):
        """
        Aplica uma transformação de Rotação no objeto.
        """

        if rx != 0:
            transf_matrix = np.array([ [1,          0,           0, 0],
                                       [0, np.cos(rx), -np.sin(rx), 0],
                                       [0, np.sin(rx),  np.cos(rx), 0],
                                       [0,          0,           0, 1]])

        elif ry != 0:
            transf_matrix = np.array([ [ np.cos(ry),    0, np.sin(ry), 0],
                                       [          0,    1,          0, 0],
                                       [-np.sin(ry),    0, np.cos(ry), 0],
                                       [          0,    0,          0, 1]])

        elif rz != 0:
            transf_matrix = np.array([ [np.cos(rx), -np.sin(rx), 0, 0],
                                       [np.sin(rx),  np.cos(rx), 0, 0],
                                       [         0,           0, 1, 0],
                                       [         0,           0, 0, 1]])

        return np.matmul(input_matrix, transf_matrix)


    def __scale(self, input_matrix, sx, sy, sz):
        """
        Altera a escala do objeto em relação aos eixos X, Y, e Z.
        """

        transf_matrix = np.array([ [sx,  0,  0,  0],
                                   [ 0, sy,  0,  0],
                                   [ 0,  0, sz,  0],
                                   [ 0,  0,  0,  1]])

        return np.matmul(input_matrix, transf_matrix)

