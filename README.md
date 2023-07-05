# Sistema gráfico interativo

Para instalar as dependências: `pip3 install -r requirements.txt`

Para executar: `python3 main.py`

## Interface:
![interface](https://raw.githubusercontent.com/rafaelbcastilhos/sgi/main/interface/interface.png)

## Funcionalidades:
#### Viewport básica:
- Na barra lateral esquerda, na seção de Editor, é necessário selecionar qual objeto deseja criar.
- Caso for um polígono, também é necessário definir a quantidade de vértices (padrão é 3).
- Para desenhar o objeto, é necessário clicar com o botão esquerdo do mouse na posição desejada na viewport.
- - Ponto: Apenas um clique.
- - Linha: Um clique na posição inicial e outro clique na posição final.
- - Poligono: Um clique na posição inicial, e outros Vértices-1 cliques para outros vértices.
#### Edição básica dos objects (Posição, escala e rotação):
- Na barra lateral esquerda, é possível alterar os valores por meio dos botões '+' e '-' para cada eixo.
#### Zoom da viewport:
- Com o botão scroll do mouse, é possível realizar zoom in e zoom out na viewport.
#### Translações:
- Na barra lateral esquerda, é possível alterar os valores dos eixos x e y para realizar translação.
- As alterações somente serão salvas, quando clicado em 'Apply'.
#### Escalonamento:
- Na barra lateral esquerda, é possível alterar os valores dos eixos x e y para realizar escalonamento.
- As alterações somente serão salvas, quando clicado em 'Apply'.
#### Rotação:
- Na barra lateral esquerda, é possível alterar o valor em graus que a rotação deve ser aplicada.
- Para definir o eixo de rotação, deve ser precionado o botão 'Rotation anchor', podendo escolher entre as opções: Mundo, Objeto e Ponto arbitrário. Quando selecionado 'Ponto arbitrário', pode ser definido o ponto nos eixos x e y, que estão localizados logo a baixo do botão.
- As alterações somente serão salvas, quando clicado em 'Apply'.
#### Cores nos objetos:
- Na barra lateral esquerda, foi adicionado um botão para escolher a cor do objeto a ser criado.
- Após selecionar o tipo do objeto, deve ser selecionado a cor (padrão é branco). 
#### Suporte para Sistema de Coordenadas Normalizado:
- Representação dos objetos do mundo para suportar o SCN.
#### Zoom:
- Translação e zoom da window para suportar o SCN.
- Para realizar zoom in e zoom out, é necessário que realize o movimento com o scroll do mouse na região da viewport.
#### Clipagem:
- Duas técnicas (algoritmos de LIANG BARSKY e COHEN SUTHERLAND) para clipagem de pontos, retas e polígonos.
#### Preenchimento:
- Checkbox para suportar polígonos preenchidos, permitindo ao usuário escolher se o polígono é em modelo de arame ou preenchido no momento de sua criação.
#### Atalhos no teclado:
- Q: Rotaciona window para esquerda
- E: Rotaciona window para direita
- W: Move window para cima
- A: Move window para esquerda
- S: Move window para baixo
- D: Move window para direita
- R: Reseta posição da window
- T: Reseta rotação da window
- Y: Reseta escala da window
- C: Zoom in da window
- Z: Zoom out da window
#### Curvas:
- Curva de Bezier e entrada para contagem de pontos e contagem de etapas na barra lateral esquerda.
- Controle para clipping de curvas 2D na barra lateral esquerda.
- B-Splines utilizando Forward Differences e entrada para contagem de pontos e contagem de etapas na barra lateral esquerda.
#### 3D:
- Objeto 3D representa um modelo de arame.
- Projeção em perspectiva.
- Superfícies bicúbicas na barra lateral esquerda.
- Cubo/paralelepípedo 3D na barra lateral esquerda.
#### Arquivos:
- Carregamento de arquivos e salvamento de objetos.