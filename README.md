# Snake IA

Agente inteligente que joga sozinho o jogo da cobrinha (*Snake*), usando **busca em largura (BFS)** para planejar o caminho até a fruta e **regras em Prolog** para decidir quais células são válidas.

Projeto desenvolvido para a disciplina de **Inteligência Artificial** do curso de Ciência da Computação da **UFSCar (Universidade Federal de São Carlos)**, como trabalho em grupo (T1).

---

## Sobre o projeto

### Objetivo

O trabalho representa o jogo da cobrinha como um **problema de estados resolvido por um agente inteligente usando busca**. A cobrinha se move em um grid de tamanho configurável, coleta frutas e cresce a cada fruta coletada. A partida termina se ela colidir com as paredes, com obstáculos ou com o próprio corpo.

A cada nova fruta, o agente:

1. identifica a posição da fruta no grid;
2. calcula o caminho mais curto até ela, respeitando as restrições do ambiente;
3. executa o próximo movimento e recalcula a rota;
4. reconhece quando **não existe rota válida** e para a busca, em vez de insistir indefinidamente.

### Utilidade

O projeto serve para:

- demonstrar, de forma visual, como a BFS encontra o caminho de menor número de movimentos quando todos os movimentos têm o mesmo custo;
- mostrar como regras lógicas (Prolog) podem ser integradas a um agente escrito em Python;
- comparar o comportamento do **mesmo agente** em três cenários de dificuldade crescente;
- discutir os limites da abordagem: achar o caminho mais curto até a fruta **não garante** sobreviver até o fim da partida.

### Cenários

O agente é o mesmo nos três cenários; o que muda é o ambiente.

| Cenário | Ambiente | Desafio para a IA |
|---|---|---|
| 1. Snake convencional | Tabuleiro sem obstáculos | Encontrar caminhos até as frutas e evitar colisões |
| 2. Obstáculos fixos | Obstáculos sorteados em 10% a 15% das células (novo sorteio a cada início ou reinício) | Encontrar rotas alternativas |
| 3. Regiões inacessíveis | Fruta no centro de um anel 3x3 de obstáculos, sem rota até ela (exige tabuleiro de pelo menos 7x7) | Identificar que a fruta é inalcançável e encerrar a busca adequadamente |

---

## Tecnologias e bibliotecas

| Componente | Para que serve | Como instalar |
|---|---|---|
| **Python 3.10+** (recomendado 3.12) | Linguagem do projeto | [python.org](https://www.python.org/downloads/) |
| **pygame** (`>=2.5,<3.0`) | Interface gráfica e leitura do teclado | `requirements.txt` |
| **PySwip** (`>=0.3.2,<0.4`) | Ponte entre Python e Prolog | `requirements.txt` |
| **SWI-Prolog** (64 bits) | Motor Prolog que executa as regras de validade das células | Instalação do sistema (veja abaixo) |
| `unittest` | Testes automatizados | Já vem com o Python |

> O **modo manual** (você joga com o teclado) precisa apenas de Python e pygame. O **SWI-Prolog** só é necessário para o agente automático (`--agent bfs`).

---

## Como executar

### 1. Obter o projeto

Entre na pasta do projeto (`snake-ia`) pelo terminal.

### 2. Instalar o SWI-Prolog (apenas para o agente automático)

- **Windows:** baixe o instalador de 64 bits em <https://www.swi-prolog.org/Download.html>. Use uma versão compatível com a arquitetura do seu Python (normalmente, ambos 64 bits). Ao final, confira se a pasta `bin` do SWI-Prolog está no `PATH`.
- **Linux (Ubuntu/Pop!_OS):**
  ```bash
  sudo apt install swi-prolog
  ```
- **macOS (Homebrew):**
  ```bash
  brew install swi-prolog
  ```

Feche e reabra o terminal e confira:

```bash
swipl --version
```

### 3. Criar o ambiente virtual e instalar as dependências

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Use sempre `python -m pip` (em vez de só `pip`) para instalar no mesmo Python que vai rodar o projeto.

### 4. Verificar a ponte com o Prolog (opcional, só para o agente)

```bash
python -c "from pyswip import Prolog; p=Prolog(); p.assertz('teste_ok'); print(list(p.query('teste_ok')))"
```

Deve imprimir uma lista com um resultado verdadeiro (por exemplo, `[{}]`).

### 5. Rodar o jogo

**Modo manual (teclado):**

```bash
python main.py --scenario 1
```

**Agente automático (BFS + Prolog):**

```bash
python main.py --scenario 1 --agent bfs
python main.py --scenario 2 --agent bfs
python main.py --scenario 3 --agent bfs
```

**Com parâmetros personalizados:**

```bash
python main.py --scenario 2 --width 24 --height 18 --cell-size 28 --fps 10 --agent bfs
```

### Parâmetros

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--scenario` | `1` | Cenário: `1`, `2` ou `3` |
| `--width` | `20` | Número de colunas do tabuleiro (mínimo 5) |
| `--height` | `15` | Número de linhas do tabuleiro (mínimo 5) |
| `--cell-size` | `32` | Tamanho de cada célula, em pixels |
| `--fps` | `8` | Velocidade do jogo (quadros por segundo) |
| `--agent` | `manual` | `manual` para teclado ou `bfs` para o agente automático |

### Controles

| Tecla | Ação |
|---|---|
| Setas ou `W` `A` `S` `D` | Mudar a direção (modo manual) |
| `Espaço` | Pausar ou continuar |
| `R` | Reiniciar a partida (no cenário 2, sorteia novos obstáculos) |
| `Esc` | Sair |

No modo manual, a cobrinha anda continuamente; as teclas mudam a direção. No modo agente, o terminal mostra a sequência de movimentos encontrada para cada fruta, em linguagem natural, e informa quando a busca termina sem solução.

### Testes

```bash
python -m unittest discover -s tests -v
```

---

## Como o agente funciona

```
        AMBIENTE (environment.py)
                │  get_state()
                ▼
        AGENTE BFS (agents/bfs_agent.py)
                │
     regras de validade ──► Prolog (logic/snake_rules.pl, via prolog_bridge.py)
                │              devolve as células válidas
                ▼
        BFS (search.py)
                │
       Caminho encontrado?
         │ sim            │ não
         ▼                ▼
   executa o 1º      informa que não há rota
   movimento         e o agente para
         │
         ▼
   atualiza o estado e recalcula a rota
```

- **Estado:** posição da cabeça, corpo da cobrinha, fruta e obstáculos, além das dimensões do grid.
- **Ações:** `UP`, `DOWN`, `LEFT`, `RIGHT`.
- **Busca:** BFS com custo unitário por movimento, o que garante o caminho com menos movimentos no modelo adotado. A ordem fixa dos vizinhos (cima, direita, baixo, esquerda) deixa os resultados determinísticos.
- **Regras em Prolog:** o estado atual é carregado como fatos (`board_size`, `obstacle`, `snake_segment`) e a consulta `valid_position(X, Y)` devolve as células permitidas.
- **Replanejamento:** o agente recalcula a rota a cada movimento, porque o corpo da cobrinha muda de posição.

---

## Estrutura do projeto

```
snake-ia/
├── main.py                 # Inicialização e laço principal
├── environment.py          # Estado, regras, colisões e transições
├── renderer.py             # Desenho e teclas (sem regras de jogo nem IA)
├── scenarios.py            # Configuração dos três cenários
├── search.py               # Busca em largura (BFS)
├── prolog_bridge.py        # Ponte Python ↔ SWI-Prolog (PySwip)
├── agents/
│   └── bfs_agent.py        # Agente que combina regras Prolog e BFS
├── logic/
│   └── snake_rules.pl      # Regras de validade das células em Prolog
├── tests/                  # Testes automatizados
├── results/                # Resultados experimentais (CSVs ignorados pelo Git)
├── docs/                   # Relatório e apresentação
├── requirements.txt
└── .gitignore
```

### Contrato do ambiente para agentes

`SnakeEnvironment.get_state()` devolve um dicionário com `width`, `height`, `snake` (cabeça primeiro), `head`, `food`, `obstacles`, `direction`, `score`, `steps`, `game_over`, `won` e `end_reason`.

Métodos principais:

- `get_state()`: observação atual.
- `valid_moves()`: ações localmente válidas no estado atual.
- `step(action)` / `execute_action(action)`: executa um movimento (`UP`, `DOWN`, `LEFT` ou `RIGHT`).
- `reset()`: reinicia o ambiente.

O agente decide a ação sem depender de `renderer.py`, então a estratégia de busca pode ser trocada sem alterar o ambiente.

---

## Limitações conhecidas

- A BFS usa a **posição da cabeça** como nó do grafo e trata o corpo atual como obstáculo fixo durante cada busca. O agente recalcula depois de cada movimento, mas não simula antecipadamente as posições futuras do corpo.
- Portanto, o agente encontra caminhos mínimos nesse modelo, mas isso **não garante sobrevivência** em todas as configurações. Preencher o tabuleiro inteiro exigiria uma estratégia de sobrevivência de longo prazo.
- Não encontrar caminho até a fruta **não significa** que a partida inteira é impossível: significa apenas que, naquele estado, não existe rota válida até o objetivo atual.
- `valid_moves()` indica validade local; não garante que a partida seja vencível.

---

## Solução de problemas

| Problema | O que fazer |
|---|---|
| `pip install` falha ao compilar o pygame (`Failed to build 'pygame'`) | Use `python -m pip install --upgrade pip setuptools wheel` e tente de novo. Se persistir, use um Python 3.10 a 3.12 no ambiente virtual, ou instale `pygame-ce` no lugar do `pygame` (o código continua com `import pygame`). |
| `pip` instala em um Python e o projeto roda em outro | Use sempre `python -m pip` com o ambiente virtual ativado. |
| `swipl` não é reconhecido | Reinstale o SWI-Prolog e adicione a pasta `bin` ao `PATH`; feche e reabra o terminal. |
| Erro ao importar `pyswip` ou ao carregar a biblioteca do SWI-Prolog | Confira se o SWI-Prolog e o Python têm a mesma arquitetura (ambos 64 bits) e rode o teste da ponte (passo 4). |
| Quero jogar sem instalar o Prolog | Use o modo manual (`python main.py`); o Prolog só é carregado com `--agent bfs`. |

---

## Contexto acadêmico

Trabalho T1 da disciplina de Inteligência Artificial, UFSCar. O foco é a modelagem do problema (PEAS, estados, ações e regras), a implementação de busca em largura, a comparação do agente em três cenários e a discussão das limitações da abordagem.
