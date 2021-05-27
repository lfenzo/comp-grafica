import os
import numpy as np

from sceneObject import sceneObject, read_obj
from transformations import Transformer

objeto = sceneObject('./exemplos-3D/coarseTri.cube.obj')

objeto.to_obj('coisa_antes.obj')

objeto.transform(seq = [
    ('mov', 1, 0, 1),
    ('mov', 10, 0, 1),
    ('rot', 45, 0, 0),
])

objeto.to_obj('coisa_depois.obj')
