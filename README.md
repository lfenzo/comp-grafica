# Projeto Prático 3 -- Processamento Gráfica

O projeto compreende as implementações de:

- Carregar e Salvar objetos tridimensionais na extensão `.obj`;
- Transformações e posicionamento dos objetos no sistema de coordenadas da Cena;
- Adição de uma camera e conversão dos objetos da cena para o seu sistema de coordenadas;
- Adição da projeção em perspectiva;
- Rasterização dos objetos presentes na projeção;

**Nota:** não foi possível concluir a rasterização até a entrega.

## Dependências

O projeto foi desenvolvido com Python (ver 3.7.10) e possui as seguintes dependências:

- numpy;
- numba;
- matplotlib;
- blender;

## Utilização

Para executar as rotinas do projeto basta executar o script "main.py" que instancia e
utiliza os objetos definidos pelos demais scripts. Dentro do script "main.py" podem ser
modificados os parametros da câmera (tando para a localização quando os parametros relativos
a geração da imagem).

## Visualização

Os objetos gerados por meio da matriz de projeção podem ser visualizados por meio do Blender
através da opção "File > Import > Wavefront (.obj)". Os objetos carregados e os objetos
transformados na cena podem ser obtidos dentro das pastas "scene_objects/" e "camera_object/" 
respectivamente.

A cena é composta por 4 objetos sendo eles 3 cubos que foram transformados para serem o chão e
as paredes direita e esquerda da cena; e uma escultura que foi colocada no cubo correspondente
ao "chão". A camera foi posicionada de modo a apontar para a origem da cena (definida como o
encontro entre as paredes e o chão).
