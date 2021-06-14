"""
Função principal no projeto. Responsável por instanciar os objetos,
colocar os objetos em cena, chamar os procedimentos e mudança de estaca,
posição e rotação, etc.
"""

import os
import matplotlib.pyplot as plt

from scene import Scene
from camera import Camera
from sceneObject import sceneObject, read_obj, save_obj

# ===============================================================
# ========= Carregando objetos utilizados dentro da Cena ==+=====
# ===============================================================

cubo = sceneObject('./exemplos-3D/coarseTri.cube.obj')
escultura = sceneObject('./exemplos-3D/coarseTri.fertility.full.obj')


# ===============================================================
# ======= Transformações nos objetos para colocar na Cena =======
# ===============================================================

chao = cubo.transform(seq = [
    ('scl', 3, 0.2, 3)
])

parede_dir = cubo.transform(seq = [
    ('scl', 3, 0.2, 2),
    ('rot', -90, 0, 0)
])

parede_esq = cubo.transform(seq = [
    ('scl', 2, 0.2, 3),
    ('rot', 0, 0, 90)
])

escultura = escultura.transform([
    ('mov', 150, 160, 140),
    ('rot', 0, 0, -20),
    ('scl', 0.0085, 0.0085, 0.0085)
])


# ========================================+++++=====================
# ======= Colocando os objetos nas posições corretas na Cena =======
# ========================================+++++===================== 

objetos_da_cena = {
    'escultura':  escultura,
    'parede_dir': parede_dir,
    'parede_esq': parede_esq,
    'chao':       chao
}

cena = Scene(objs = objetos_da_cena)
camera = Camera(pos = (3, 3, 3),
                look_at = (0, 0, 0))

# adiciona uma camera na cena que ja converte todos os objetos para o seu sistema de coordenadas próprio
cena.add_camera(camera)

# salva todos os objetos que esto no sistema de coordenadas da cena em arquivos .obj
cena.to_obj()

camera.snapshot(aspect_ratio = 0.5,
                fov = 120,
                far = 10,
                near = 1)

# salva todos os objetos que esto no sistema de coordenadas da camera em arquivos .obj
camera.to_obj(proj = True)

img = camera.rasterize(res = (800, 600))


# ========================================+++++=====================
# ============== Salvando a imagem gerada pela Cena ================
# ========================================+++++===================== 

fig, axs = plt.subplots()

axs.imshow(img)
fig.savefig('imagem.png')
