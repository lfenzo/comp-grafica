"""
Implementação da cena contendo um ou mais objetos

A cena é composta de um array de objetos com suas coordenadas já
transformadas para a cena: as transformações dos oobjetos retornam
outros objetos com as dimensoes e posicionamentos modificados.
"""

import os
import numpy as np

from camera import Camera
from sceneObject import save_obj
from transformations import Transformer


class Scene:

    def __init__(self, objs: dict, camera = None):
        self.__camera = camera # a cena terá apenas uma camera
        self.__objs = objs

    def add_camera(self, camera: Camera):
        """
        Adiciona uma camera à cena e já coloca os objetos que estão na cena no
        sistema de coordenadas interno da câmera. Apesar de essa operação ocorrer
        na adição da camera à cena, é a câmera que é responsável por fazer a troca
        de sistema de coordenadas.
        """

        self.__camera = camera

        for obj_alias, obj_info in self.__objs.items():
            self.__camera.add_object(alias = obj_alias, obj_info = obj_info)

    def add_object(self, object_matrix: dict, alias: str):
        """
        Adiciona um objeto (representado por um dicionário: sceneObject::obj_info)
        Objetos devem ser transformados para que fiquem como devem estar na cena.
        """

        self.__objs[alias] = object_matrix

    def remove_object(self, alias: str):
        """
        Remove um objeto que está na cena por meio do seu alias.
        """

        self.__objs.pop(alias)

    def to_obj(self):
        """
        Salva todos os objetos que estão no sistema de coordedadas da
        cena em arquivos .obj no formato <cena_(objeto).obj>.
        """

        # apenas para organização dos arquivos salvos pela cena
        if not os.path.exists('scene_objects'):
            os.mkdir('scene_objects')

        for obj_alias, obj_info in self.__objs.items():
            save_obj(filepath = f'scene_objects/scene_{obj_alias}.obj', obj_info = obj_info)
