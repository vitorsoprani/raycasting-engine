# Raycasting Engine — Relatório do Projeto

Motor gráfico de raycasting em Python + Pygame, no estilo dos jogos clássicos como Wolfenstein 3D. O jogador é solto dentro de um labirinto escuro e precisa **encontrar a luz no final do labirinto** para vencer.

> Esse documento pode ser melhor visualizado na [página do github](https://github.com/vitorsoprani/raycasting-engine/tree/game)

## Índice

- [Conceito: o que é Raycasting?](#conceito-o-que-é-raycasting)
- [Como instalar e rodar](#como-instalar-e-rodar)
- [Objetivo do jogo](#objetivo-do-jogo)
- [Comandos](#comandos)
- [Arquitetura do projeto](#arquitetura-do-projeto)
- [Aspectos do Pygame utilizados](#aspectos-do-pygame-utilizados)
- [Referências](#referências)

## Conceito: o que é Raycasting?

Raycasting é uma técnica usada para **simular um ambiente 3D a partir de um mapa 2D**, sem de fato construir e renderizar geometria tridimensional. Foi a base gráfica de jogos como *Wolfenstein 3D*, numa época em que os computadores não tinham poder de processamento suficiente para 3D "de verdade".

A ideia central:

1. **O mapa é uma matriz 2D.** Cada posição da matriz representa uma célula do labirinto: `0` é espaço livre, um valor positivo é parede. Neste projeto, valores negativos marcam posições com significado especial (ex.: o objetivo do jogo).
2. **Para cada coluna de pixels da tela, um raio é lançado** a partir da posição do jogador, dentro do seu campo de visão (FOV). O algoritmo percorre o mapa até encontrar uma parede, calculando a distância percorrida.
3. **Quanto mais perto a parede, mais alta a "fatia" desenhada na tela.** Uma parede próxima ocupa quase toda a altura da tela; uma parede distante vira uma faixa fina. Repetindo isso para todas as colunas, forma-se a ilusão de profundidade.
4. **Sombreamento por distância e por face** dá a sensação de volume: paredes mais distantes ficam mais escuras, e paredes atingidas em faces diferentes (horizontal/vertical) recebem tons diferentes.

No código, isso é implementado pelo algoritmo de *DDA (Digital Differential Analysis)*: em vez de avançar o raio pixel a pixel (lento e impreciso), ele "pula" direto de uma borda de célula do grid para a próxima, o que é muito mais eficiente. Explicações mais detalhadas da matemática do algoritmo podem ser encontradas nas [referências](#referências)

## Como instalar e rodar

### Pré-requisitos

- Python 3.10+
- Pygame

### Instalação

```bash
# Clone o repositório
git clone https://github.com/vitorsoprani/raycasting-engine.git
cd raycasting-engine

# (opcional, mas recomendado) crie um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac

# Instale as dependências
pip install pygame
```

### Executando

```bash
cd src   # pasta onde está o main.py
python main.py
```

> O jogo abre em **tela cheia**. Para sair a qualquer momento, pressione `ESC`.

## Objetivo do jogo

Você acorda dentro de um labirinto escuro e apertado. Usando apenas os corredores visíveis à sua frente, seu objetivo é **encontrar a luz no final do labirinto** — um ponto de saída que se destaca das paredes comuns por brilhar em branco no meio da escuridão vermelha do resto do labirinto.

## Comandos

| Tecla | Ação |
|---|---|
| `W` / `↑` | Andar para frente |
| `S` / `↓` | Andar para trás |
| `A` | Deslocar (strafe) para a esquerda |
| `D` | Deslocar (strafe) para a direita |
| `←` | Girar a câmera para a esquerda |
| `→` | Girar a câmera para a direita |
| Mouse | Olhar ao redor |
| `ESC` | Sair do jogo |

> CHEAT (recomendo que não use :p): `ctrl direto` + m ativam um minimap

## Arquitetura do projeto

O código é organizado em módulos com responsabilidades separadas, cada um representando uma peça do motor:

```
main.py        -> loop principal do jogo, input, inicialização e integração de tudo
player.py      -> classe Player: posição, direção, movimento e colisão
tile_map.py    -> classe Map: representação do labirinto e desenho do minimapa
raycaster.py   -> classes Ray e RayCaster: lançamento de raios e renderização 3D
```

### `main.py`

É o ponto de entrada e o **orquestrador** do jogo. Responsável por:
- Inicializar o Pygame, a janela e os recursos (imagens, sons e música);
- Definir o mapa do labirinto (uma matriz de inteiros) e instanciar `Map`, `Player` e `RayCaster`;
- Rodar o **game loop** principal: captar eventos e teclas pressionadas, atualizar o estado do jogador, disparar a renderização e controlar o framerate;

### `player.py` — classe `Player`

Guarda o estado do jogador (posição `pos` e direção `dir`, ambos como `pygame.Vector2`) e concentra a lógica de movimento:
- `update_dir`: rotaciona o vetor de direção conforme o input angular (teclado/mouse);
- `update_pos`: calcula o vetor de movimento combinando avanço/recuo e strafe lateral, testando colisão eixo a eixo (X e Y separadamente) contra o `tile_map`, o que permite "deslizar" ao longo das paredes em vez de travar;
- Também é responsável por detectar quando o jogador pisa numa célula especial (valor `-1`) e disparar um evento customizado do Pygame (`pygame.USEREVENT`) para avisar o `main.py`.

### `tile_map.py` — classe `Map`

Representa o labirinto como uma matriz 2D de inteiros e oferece:
- `load_from_list`: carrega o mapa a partir de uma matriz fixa;
- `check_pos`: converte uma posição em coordenadas de mundo para índice de célula do grid e devolve o valor daquela célula — usado tanto para colisão quanto para identificar tiles especiais (parede comum, vazio, saída, evento especial);
- `draw`: desenha o minimapa em 2D (usado no modo de depuração/visualização do mapa).

### `raycaster.py` — classes `Ray` e `RayCaster`

O coração do motor gráfico:
- **`Ray`** implementa o algoritmo **DDA** para lançar um único raio a partir de uma posição e direção, avançando célula a célula pelo grid até colidir com uma parede, guardando a distância percorrida e qual face foi atingida (`x` ou `y`);
- **`RayCaster`** gerencia um conjunto de `n_rays` raios distribuídos uniformemente dentro do campo de visão (`fov`) do jogador. Seus principais métodos:
  - `cast_all`: recalcula todos os raios a cada frame a partir da posição/direção atual do jogador;
  - `render_3d`: converte cada raio numa faixa vertical de parede na tela, com altura inversamente proporcional à distância (efeito de perspectiva) e cor dependente da distância e da face atingida — é aqui que a tile de saída (`valor 2`) é destacada em branco;
  - `draw_all`: desenha os raios no minimapa, útil para depuração.

### Por que essa separação?

Cada classe tem uma responsabilidade única: `Map` só sabe sobre o mundo estático, `Player` só sabe sobre estado e movimento do jogador, `RayCaster`/`Ray` só sabem projetar esse mundo em 2D. Isso deixa o `main.py` livre para só coordenar o fluxo do jogo, sem se preocupar com os detalhes de cada sistema — facilitando testar, entender e evoluir cada parte isoladamente.

## Aspectos do Pygame utilizados

O projeto explora vários módulos centrais da biblioteca:

- **Display**: `pygame.display.set_mode` com as flags `FULLSCREEN | SCALED` para abrir o jogo em tela cheia mantendo a resolução interna consistente independente do monitor; `pygame.display.get_surface()` e `pygame.display.update()` para obter a superfície principal e apresentar cada frame renderizado.
- **Eventos (`pygame.event`)**: o loop principal consome a fila de eventos (`pygame.event.get()`) para tratar `QUIT` e `KEYDOWN`. O projeto também usa um **evento customizado** (`pygame.USEREVENT`), postado manualmente com `pygame.event.post()` a partir da classe `Player` quando o jogador pisa numa célula especial — um bom exemplo de como desacoplar lógica de jogo (detecção no `Player`) da reação a ela.
- **Input**: `pygame.key.get_pressed()` para movimento contínuo (segurar tecla), tratamento de tecla combinada (`Ctrl direito + M` para o minimapa) e `pygame.mouse.get_rel()` para capturar o deslocamento relativo do mouse a cada frame, usado tanto para girar a câmera quanto para ajustar o horizonte verticalmente. `pygame.event.set_grab(True)` prende o cursor na janela e `pygame.mouse.set_visible(False)` o esconde, criando a experiência de câmera em primeira pessoa.
- **Áudio (`pygame.mixer`)**: `pygame.mixer.Sound` para efeitos pontuais e `pygame.mixer.music` para a trilha sonora contínua em loop (`loops=-1`), mostrando o uso dos dois sistemas de áudio distintos do Pygame — um para efeitos curtos carregados na memória, outro para streaming de música.
- **Imagens (`pygame.image`)**: `pygame.image.load` para carregar a imagem e `pygame.transform.scale` para redimensioná-la ao tamanho da tela.
- **Desenho primitivo (`pygame.draw`)**: usado tanto na renderização 3D (retângulos coloridos representando as "fatias" de parede) quanto no minimapa 2D (retângulos para as células do mapa, círculo e linha para representar o jogador e sua direção).
- **Surfaces**: uso de uma `Surface` auxiliar (`minimap`) para desenhar o mapa 2D separadamente e depois compor (`blit`) sobre a tela principal, redimensionada com `pygame.transform.scale`.
- **Clock**: `pygame.time.Clock().tick(FRAME_RATE)` para limitar e estabilizar o framerate do jogo em 60 FPS.
- **Vetores (`pygame.Vector2`)**: usados extensivamente para posição e direção do jogador e dos raios, aproveitando operações nativas como `rotate`, `rotate_ip`, `normalize_ip` e produto escalar por vetor — o que simplifica bastante a matemática de movimento e rotação sem precisar implementá-la manualmente.

## Referências

- [Artigo do Lodev sobre Raycasting](https://lodev.org/cgtutor/raycasting.html)
- [Vídeo do javidx9 sobre Raycasting](https://youtu.be/NbSee-XM7WA?si=ZEA5PQuJbJ32UmYd)
