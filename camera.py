"""
Implementação da Camera dentro da cena.
"""

import numpy as np

from numpy.linalg import norm
from transformations import Transformer

class Camera:

    def __init__(self, fov, pos, look_at):

        self.__camera_objs = {}

        look_at = np.asarray(look_at)
        pos = np.asarray(pos)

        self.__pos = pos
        self.__view_up = pos + np.array([0, 1, 0])
        self.__n = (look_at - pos) / norm(look_at - pos) + pos

        self.__u = (np.cross(self.__view_up, self.__n)) / norm( (np.cross(self.__view_up, self.__n)) )
        self.__v = np.cross(self.__n, self.__u)

        # corigir em commit 
        self.__T = [ [1, 0, 0, self.__pos[0]],
                     [0, 1, 0, self.__pos[1]],
                     [0, 0, 1, self.__pos[2]],
                     [0, 0, 0,             1], ]

        self.__R = [ [self.__u[0], self.__u[1], self.__u[2], 0],
                     [self.__v[0], self.__v[1], self.__v[2], 0],
                     [self.__n[0], self.__n[1], self.__n[2], 0],
                     [          0,           0,           0, 1] ]

        self.__M = np.matmul(self.__R, self.__T)

    def add_object(self, alias, obj_info):

        vertices_to_transform = [vertex for index, vertex in obj_info['v'].items()]

        transformed_vertices = Transformer().apply(obj_matrix = vertices_to_transform,
                                                    transf_matrix = self.__M)

        transformed_obj_info = {index: vertex for index, vertex in enumerate(transformed_vertices)}

        obj_info['v'] = transformed_obj_info

        self.__camera_objs[alias] = obj_info


    # apenas para teste
    def to_obj(self, alias) -> None:
        """
        Salva as informações do objeto (vertices, faces, etc) em um arquivo .obj.

        Parametros
        ----------
        `filepath`: nome do arquivo a ser salvo
        """

        with open(f'camera_{alias}.obj', 'w') as obj_file:

            for obj_alias, obj_info in self.__camera_objs.items():

                if obj_alias == alias:

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
