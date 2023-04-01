# ine5420
### Grupo 7: José Victor Goulart dos Santos (20200412) e Rafael Begnini de Castilhos (20205642)

## Sistema gráfico interativo

Para instalar as dependências: `pip3 install -r requirements.txt`

Para executar: `python3 main.py`

## Trabalho 1.1:
#### Viewport básica
#### Criação e renderização de objects
- Na barra lateral esquerda, na seção de Editor, é necessário selecionar qual objeto deseja criar.
- Caso for um polígono, também é necessário definir a quantidade de vértices (padrão é 3).
- Para desenhar o objeto, é necessário clicar com o botão esquerdo do mouse na posição desejada na viewport.
- - Ponto: Apenas um clique.
- - Linha: Um clique na posição inicial e outro clique na posição final.
- - Poligono: Um clique na posição inicial, e outros Vértices-1 cliques para outros vértices.
#### Edição básica dos objects (Posição, escala e rotação)
- Na barra lateral esquerda, é possível alterar os valores por meio dos botões '+' e '-' para cada eixo.
#### Exibição dos objetos na viewport e displayfile
- Conforme for realizado a criação de objetos, eles serão visualizados na viewport e listados do displayfile.
#### Zoom da viewport
- Com o botão scroll do mouse, é possível realizar zoom in e zoom out na viewport.

## Trabalho 1.2:
#### Translações
- Na barra lateral esquerda, é possível alterar os valores dos eixos x e y para realizar translação.
- As alterações somente serão salvas, quando clicado em 'Apply'.
#### Escalonamento
- Na barra lateral esquerda, é possível alterar os valores dos eixos x e y para realizar escalonamento.
- As alterações somente serão salvas, quando clicado em 'Apply'.
#### Rotação
- Na barra lateral esquerda, é possível alterar o valor em graus que a rotação deve ser aplicada.
- Para definir o eixo de rotação, deve ser precionado o botão 'Rotation anchor', podendo escolher entre as opções: Mundo, Objeto e Ponto arbitrário. Quando selecionado 'Ponto arbitrário', pode ser definido o ponto nos eixos x e y, que estão localizados logo a baixo do botão.
- As alterações somente serão salvas, quando clicado em 'Apply'.
#### Cores nos objetos
- Na barra lateral esquerda, foi adicionado um botão para escolher a cor do objeto a ser criado.
- Após selecionar o tipo do objeto, deve ser selecionado a cor (padrão é branco). 
- Para os polígonos, apenas será pintado as bordas.