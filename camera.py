import numpy as np

from numpy.linalg import norm

class Camera:

    def __init__(self, pos, look_at):

        self.__camera_objs = {}

        look_at = np.asarray(look_at)
        pos = np.asarray(pos)

        self.__pos = pos

        #Definindo um view up arbitrário
        self.__view_up = pos + np.array([0, 1, 0])

        self.__n = (look_at - pos) / norm(look_at - pos) + pos
        self.__u = (np.cross(self.__view_up, self.__n)) / norm( (np.cross(self.__view_up, self.__n)) )
        self.__v = np.cross(self.__n, self.__u)

        self.__T = [ [1, 0, 0, self.__pos[0]],
                     [0, 1, 0, self.__pos[1]],
                     [0, 0, 1, self.__pos[2]],
                     [0, 0, 0,             1], ]

        self.__R = [ [self.__u[0], self.__u[1], self.__u[2], 0],
                     [self.__v[0], self.__v[1], self.__v[2], 0],
                     [self.__n[0], self.__n[1], self.__n[2], 0],
                     [          0,           0,           0, 1] ]

        self.__M = np.matmul(self.__R, self.__T)

    # Falta criar o método para adicionar objetos na visão da câmera - Multiplicar os vértices do obj pela matriz M (self.__M)
    # def add_object():