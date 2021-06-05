"""
Implementação da cena contendo um ou mais objetos
"""

import numpy as np
from camera import Camera

from transformations import Transformer


class Scene:

    def __init__(self, objs, camera = None):
        self.__camera = camera
        self.__objs = objs

    def add_camera(self, camera: Camera):
        self.__camera = camera

    def convert_camera_coords(self):
        """
        Converte todos os vertices do sistema do mundo para o sistema da camera.
        """

        if not self.__camera:
            raise AttributeError('Você não tem uma camera. Adicione uma.')

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
