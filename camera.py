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
import numpy as np

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
        self.__image = []

        look_at = np.asarray(look_at)
        pos = np.asarray(pos)

        self.__pos = pos
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

    def rasterize(self, res: tuple):
        """
        Realiza o processo de rasterização dos objetos que já estão no "sistema de
        coordenadas da projeção".

        Parametros
        -----------
        `res': resolução da imagem gerada.
        """

        # inicializa a imagem a ser gerada com uma matrix de zeros
        self.__image = np.zeros(res)

        for obj_alias, obj_info in self.__proj_objs.items():

            for i, face in enumerate(obj_info['f']):

                try: # algumas faces não estão no formato (v1, v2, v3). Devem ser ignoradas.

                    vertices = [
                        self.__proj_objs[obj_alias]['v'][face[0]],
                        self.__proj_objs[obj_alias]['v'][face[1]],
                        self.__proj_objs[obj_alias]['v'][face[2]],
                    ]

                    self.__draw_triangle(vertices = vertices)

                except Exception:
                    continue

        return self.__image

    def __draw_triangle(self, vertices: list):
        """
        Utiliza o algortimo baricêntrico para preencher o triangulo.

                    v1(x, y, z)
                         1
                        / \
                       /   \
                      /     \
                     /       \
                    /         \
                   /           \
                  2-------------3
            v2(x, y, z)       v3(x, y, z)

        Verifica se um ponto arbitrário P está dentro do triangulo. Caso
        ele esteja, então o pixel correspondente deve ser pintado chamando
        a função "__draw_pixel()"
        """

        # obtem as dimensões da bouding box do triangulo

                       # vertice 1       vertice 2        vertice 3
        max_x = max(vertices[0][0], vertices[1][0], vertices[2][0])
        max_y = max(vertices[0][1], vertices[1][1], vertices[2][1])

        min_x = min(vertices[0][0], vertices[1][0], vertices[2][0])
        min_y = min(vertices[0][1], vertices[1][1], vertices[2][1])

        # obtendo os vetores "suporte" para o triangulo a partir de v1
        vs1 = np.array( [vertices[1][0] - vertices[0][0], vertices[1][1] - vertices[0][1]] )
        vs2 = np.array( [vertices[2][0] - vertices[0][0], vertices[2][1] - vertices[0][1]] )

        for x in range(int(min_x*100), int(max_x*100)):

            for y in range(int(min_y*100), int(max_y*100 + 1)):

                v = np.array([x - vertices[0][0], y - vertices[0][1]])

                s = np.cross(v, vs2) / np.cross(vs1, vs2)
                t = np.cross(vs1, v) / np.cross(vs1, vs2)

                # verifica se o ponto está dentro do triangulo
                if (s >= 0) and (t >= 0) and (s + t <= 1):
                    self.__draw_pixel(x, y)

    def __draw_pixel(self, x: int, y: int):
        self.__image[x, y] = 1

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
