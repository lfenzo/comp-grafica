"""
Função principal no projeto. Responsável por instanciar os objetos,
colocar os objetos em cena, chamar os procedimentos e mudança de estaca,
posição e rotação, etc.
"""

import os

from scene import Scene
from camera import Camera
from sceneObject import sceneObject, read_obj, save_obj

# carregando objetos utilizados na cena
cubo = sceneObject('./exemplos-3D/coarseTri.cube.obj')

rosto = sceneObject('./exemplos-3D/coarseTri.egea1.obj')
escultura = sceneObject('./exemplos-3D/coarseTri.fertility.full.obj')


# ===============================================================
# ======= Transformações nos objetos para colocar na Cena =======
# ===============================================================

chao = cubo.transform(seq = [
    ('scl', 2, 0.2, 3),
    ('rot', 0, 0, 90)
])

parede_dir = cubo.transform(seq = [
    ('scl', 3, 0.2, 2),
    ('rot', -90, 0, 0)
])

parede_esq = cubo.transform(seq = [
    ('scl', 3, 0.2, 3)
])

rosto = rosto.transform(seq = [
    ('mov', 0.8, 0.4, -2),
    ('rot', 0, 80, 0),
    ('scl', 0.6, 0.6, 0.6)
])

escultura = escultura.transform([
    ('mov', 150, 160, 100),
    ('rot', 0, 0, -20),
    ('scl', 0.0085, 0.0085, 0.0085)
])

save_obj(filepath = 'chao.obj', obj_info = chao)
save_obj(filepath = 'parede_esq.obj', obj_info = parede_esq)
save_obj(filepath = 'parede_dir.obj', obj_info = parede_dir)
save_obj(filepath = 'escultura.obj', obj_info = escultura)

# ========================================+++++=====================
# ======= Colocando os objetos nas posições corretas na Cena =======
# ========================================+++++===================== 
objetos_da_cena = {
    'escultura':  escultura,
    'rosto':      rosto,
    'parede_dir': parede_dir,
    'parede_esq': parede_esq),
    'chao':       chao
}

cena = Scene(objs = objetos_da_cena)

camera = Camera(fov = 90, pos = (-2, -2, -2), look_at = (0, 0, 0))

cena.add_camera(camera)
cena.convert_camera_coords()

# teste da conversão do sistema de coordenadas para a camera
camera.to_obj('chao')
camera.to_obj('parede_esq')
camera.to_obj('parede_dir')
camera.to_obj('escultura')
camera.to_obj('rosto')
