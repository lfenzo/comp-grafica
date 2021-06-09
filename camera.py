"""
Implementação da Camera dentro da cena.
"""

import os
import numpy as np

from numpy.linalg import norm
from sceneObject import save_obj
from transformations import Transformer

class Camera:

    def __init__(self, fov, pos, look_at):
        """
        Construtor da Camera.

        Parametros
        ------------
        `pos`: posição da camera (x, y, z) dentro do sistema de coordenadas da Cena.
        `look_at`; ponto (x, y, z) para o qual a camera está "apontada".
        `fov`: field of view da Camera (graus).
        """

        self.__camera_objs = {}

        look_at = np.asarray(look_at)
        pos = np.asarray(pos)

        self.__pos = pos
        self.__view_up = np.array([0, 1, 0])

        self.__n = (look_at - pos) / norm(look_at - pos) + pos
        self.__u = (np.cross(self.__view_up, self.__n)) / norm( (np.cross(self.__view_up, self.__n)) )
        self.__v = np.cross(self.__n, self.__u)

        self.__T = [ [1, 0, 0, -self.__pos[0]],
                     [0, 1, 0, -self.__pos[1]],
                     [0, 0, 1, -self.__pos[2]],
                     [0, 0, 0,              1] ]

        self.__R = [ [self.__u[0], self.__u[1], self.__u[2], 0],
                     [self.__v[0], self.__v[1], self.__v[2], 0],
                     [self.__n[0], self.__n[1], self.__n[2], 0],
                     [          0,           0,           0, 1] ]

        # matriz de tranformação para o ponto de vista da camera
        self.__M = np.matmul(self.__R, self.__T)

    def add_object(self, alias, obj_info):
        """
        Adiciona um objeto da cena na Camera já realizando a troca de sistema de coordeadas.

        Parametros
        ------------
        `alias`: nome que faz referência ao objeto adicionado na camera.
        `obj_info`: arrey com os pontos do objeto ("matrix do objeto").
        """

        vertices_to_transform = [vertex for index, vertex in obj_info['v'].items()]

        transformed_vertices = Transformer().apply(obj_matrix = vertices_to_transform,
                                                    transf_matrix = self.__M)

        transformed_obj_info = {index: vertex for index, vertex in enumerate(transformed_vertices)}

        camera_transformed = obj_info.copy()
        camera_transformed['v'] = transformed_obj_info

        self.__camera_objs[alias] = camera_transformed

    def to_obj(self) -> None:
        """
        Salva todos os objetos que estão dentro do ponto de vista da camera
        em arquivos .obj no formato <camera(alias).obj>
        """

        # apenas para organização dos arquivos salvos pela camera
        if not os.path.exists('camera_objects'):
            os.mkdir('camera_objects')

        for obj_alias, obj_info in self.__camera_objs.items():
            save_obj(filepath = f'camera_objects/scene_{obj_alias}.obj', obj_info = obj_info)
