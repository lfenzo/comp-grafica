"""
Implementação da Camera dentro da cena.

As definições de posicionamento da camera são definidas no momento da
instanciação. Também é definida a matriz de mudança de sistema de co-
ordenadas que aplicada a cada objeto novo que é adicionado à camera por
meio da classe Scene.

As definições de projeção (e troca para sistema de coordenadas da projeção)
são definidas a cada chamada do método 'snapshot', neste metodo é possível
utilizar uma mesma camera para tirar fotos com campos de visão diferentes,
diferentes razões de aspecto e limiares de proximidade.
"""

import os
import numba
import numpy as np

from PIL import Image, ImageColor
from numpy.linalg import norm
from sceneObject import save_obj
from transformations import Transformer

class Camera:

    def __init__(self, pos, look_at):
        """
        Construtor da Camera. Cria uma câmera a partir de uma posição inicial, um
        ponto de visão, campo de visão e uma razão de aspecto para a viewport.

        Parametros
        ------------
        `pos`: posição da camera (x, y, z) dentro do sistema de coordenadas da Cena.
        `look_at`; ponto (x, y, z) para o qual a camera está "apontada".
        `fov`: field of view da Camera (graus).
        """

        self.__camera_objs = {}
        self.__proj_objs = {}
        self.__image = None

        look_at = np.asarray(look_at)
        pos = np.asarray(pos)

        self.__pos = pos
        # o vetor view_up deveria ser o mesmo que (0, 1, 0): o eixo y mas nesta situação
        # a imagem gerada fica "de ponta cabeça" enquanto os objetos no blender ficam 
        # com a orientação correta. Para resolver o problema da orintação na geração da
        #imagem é preciso inverter o vetor para (0, -1, 0). Nosso grupo não consegui consertar
        # esse problema, nem ententer porque ele ocorre.
        self.__view_up = np.array([0, 1, 0])

        self.__n = (look_at - pos) / norm(look_at - pos) + pos
        self.__u = (np.cross(self.__view_up, self.__n)) / norm( (np.cross(self.__view_up, self.__n)) )
        self.__v = np.cross(self.__n, self.__u)

        T = [ [1, 0, 0, -self.__pos[0]],
              [0, 1, 0, -self.__pos[1]],
              [0, 0, 1, -self.__pos[2]],
              [0, 0, 0,              1] ]

        R = [ [self.__u[0], self.__u[1], self.__u[2], 0],
              [self.__v[0], self.__v[1], self.__v[2], 0],
              [self.__n[0], self.__n[1], self.__n[2], 0],
              [          0,           0,           0, 1] ]

        # matriz de tranformação de sistema de coordenadas (sistema da cena para o sistema da camera)
        self.__M = np.matmul(R, T)

    def add_object(self, alias, obj_info):
        """
        Adiciona um objeto da cena na Camera já realizando a troca de sistema de coordeadas.

        Parametros
        ------------
        `alias`: nome que faz referência ao objeto adicionado na camera.
        `obj_info`: array com os pontos do objeto ("matrix do objeto").
        """

        vertices_to_transform = [vertex for index, vertex in obj_info['v'].items()]

        transformed_vertices = Transformer().apply(obj_matrix = vertices_to_transform,
                                                    transf_matrix = self.__M)

        transformed_obj_info = {index: vertex for index, vertex in enumerate(transformed_vertices)}

        camera_transformed = obj_info.copy()
        camera_transformed['v'] = transformed_obj_info

        self.__camera_objs[alias] = camera_transformed

    def snapshot(self, fov, aspect_ratio, near, far):
        """
        Tira uma 'foto' de como cena está do ponto de vista da cemera naquele instante.

        Inicialmente coloca os objetos já convertidos para o SC da camera no plano de
        projeção.


        Parametros
        ----------
        `fov`: field of view da Camera (graus).

        `aspect_ratio`: razão de aspecto entre a vertical e horizontal para a camera
                        (caso seja 1 será uma imagem quadrada).

        `near`: Limiar de distancia para o plano de corte. Objetos mais proixmos do
               que 'near' não serão considerados na projeção da camera.

        `far`: Limiar de distancia para o plano de corte. Objetos mais distantes do
               que 'far' não serão considerados na projeção da camera.
        """

        # apenas por questão de legibilidade...
        A = 1 / (aspect_ratio * np.tan(0.5 * fov * np.pi / 180))
        B = 1 / np.tan(0.5 * fov * np.pi / 180)
        C = -(far + near) / (far - near)
        D = -(2 * far * near) / (far - near)

        # definiação da matriz de transformaão para a projeção da camera
        projection_matrix = [ [A,  0,  0,  0],
                              [0,  B,  0,  0],
                              [0,  0,  C,  D],
                              [0,  0, -1,  0] ]

        for obj_alias, obj_info in self.__camera_objs.items():

            vertices_to_transform = [vertex for index, vertex in obj_info['v'].items()]

            transformed_vertices = Transformer().apply(obj_matrix = vertices_to_transform,
                                                       transf_matrix = projection_matrix)

            transformed_obj_info = {index: vertex for index, vertex in enumerate(transformed_vertices)}

            projection_transformed = obj_info.copy()
            projection_transformed['v'] = transformed_obj_info

            self.__proj_objs[obj_alias] = projection_transformed

    def rasterize(self, res: tuple, filepath: str) -> None:
        """
        Realiza o processo de rasterização dos objetos que já estão no "sistema de
        coordenadas da projeção".

        Parametros
        -----------
        `res': resolução da imagem gerada.
        `filepath`: nome do arquivo onde a imagem gerada será salva.
        """

        # inicializa a imagem a ser gerada com uma matrix de zeros
        self.__image = Image.new(mode = 'RGB', size = res)

        colors = ['red', 'white', 'orange', 'pink']

        for (obj_alias, obj_info), c in zip(self.__proj_objs.items(), colors):

            color = ImageColor.getrgb(c)

            for face in obj_info['f']:

                v1 = self.__proj_objs[obj_alias]['v'][ face[0] - 1 ]
                v2 = self.__proj_objs[obj_alias]['v'][ face[1] - 1 ]
                v3 = self.__proj_objs[obj_alias]['v'][ face[2] - 1 ]

                # gambiarra alert!
                # por alguma razão aescala não é mantida e os valores ficam muito pequenos
                # para serem vistos na image.

                # no blender, entretanto, os objetos sao mostrados como deveriam estar
                v1 = list(map(int, v1 * 50 + 200))
                v2 = list(map(int, v2 * 50 + 200))
                v3 = list(map(int, v3 * 50 + 200))

                self.__draw_lines(v1[0], v1[1], v2[0], v2[1], color)
                self.__draw_lines(v1[0], v1[1], v3[0], v3[1], color)
                self.__draw_lines(v2[0], v1[1], v3[0], v2[1], color)

        self.__image.save(filepath)

    def __draw_lines(self, x0, y0, x1, y1, color) -> None:
        """
        Desenha as linhas utilizando as coordenadas X e Y dos pontos passados utilizando
        o algoritmo de Bresenham
        """

        dx = x1 - x0
        dy = y1 - y0

        d = 2 * dy - dx

        inc_e = 2 * dy
        inc_ne = 2 * (dy - dx)

        x = x0
        y = y0

        # evita que os pixels ficam se expelhando na cena 
        if not ((x < 0) and (y < 0)):
            self.__image.putpixel((x, y), color)

        while x < x1:

            if d <= 0:
                d = d + inc_e
                x += 1

            else:
                d = d + inc_ne
                x += 1
                y += 1

            if not ((x < 0) and (y < 0)):
                self.__image.putpixel((x, y), color)

    def to_obj(self, proj: bool) -> None:
        """
        Salva todos os objetos que estão dentro do ponto de vista da camera
        em arquivos .obj no formato <camera(alias).obj>

        Parametros
        ------------
        `proj`: Se True salva a matriz de projeção, False salva apenas os objetos no sistema
                de coordenadas da camera.
        """

        # apenas para organização dos arquivos salvos pela camera
        if not os.path.exists('camera_objects'):
            os.mkdir('camera_objects')

        info = self.__proj_objs if proj == True else self.__camera_objs

        for obj_alias, obj_info in info.items():
            save_obj(filepath = f'camera_objects/camera_{obj_alias}.obj', obj_info = obj_info)
