"""Configurações dos cenários do Snake IA.

Cenário 2: obstáculos aleatórios a cada criação/reinício, ocupando de 10% a 50%
das células do tabuleiro (sem contar células da cobra e da fruta).
Cenário 3: fruta dentro de uma câmara fechada por obstáculos, sem caminho
geométrico entre a cobra e a fruta.
"""
from __future__ import annotations

import random

Position = tuple[int, int]


def _initial_snake(width: int, height: int) -> list[Position]:
    """Cobra inicial horizontal, com a cabeça primeiro."""
    return [
        (width // 2, height // 2),
        (width // 2 - 1, height // 2),
        (width // 2 - 2, height // 2),
    ]


def _random_obstacles(
    width: int,
    height: int,
    snake: list[Position],
    food: Position,
    rng: random.Random,
) -> set[Position]:
    """Sorteia obstáculos em 10%-50% do tabuleiro, sem sobreposição."""
    total_cells = width * height
    min_count = max(1, (total_cells * 10 + 99) // 100)  # arredonda para cima
    max_count = (total_cells * 15) // 100              # arredonda para baixo

    forbidden = set(snake) | {food}
    available = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in forbidden
    ]
    max_count = min(max_count, len(available))
    if min_count > max_count:
        raise ValueError(
            "Tabuleiro pequeno demais para sortear obstáculos entre 10% e 50%."
        )

    count = rng.randint(min_count, max_count)
    return set(rng.sample(available, count))


def _blocked_food_scenario(
    width: int, height: int, snake: list[Position]
) -> tuple[Position, set[Position]]:
    """Cria uma câmara fechada com a fruta dentro e a cobra do lado de fora."""
    if width < 7 or height < 7:
        raise ValueError(
            "O cenário 3 precisa de um tabuleiro de pelo menos 7x7 "
            "para manter a fruta isolada sem sobrepor a cobra."
        )

    # A câmara 3x3 fica no canto superior direito, longe da cobra central.
    left, top = width - 4, 1
    right, bottom = width - 2, 3
    food = (left + 1, top + 1)

    obstacles: set[Position] = set()
    for x in range(left, right + 1):
        obstacles.add((x, top))
        obstacles.add((x, bottom))
    for y in range(top, bottom + 1):
        obstacles.add((left, y))
        obstacles.add((right, y))

    # Garantia defensiva para dimensões não usuais.
    if food in snake or obstacles.intersection(snake):
        raise ValueError(
            "Não foi possível posicionar a câmara do cenário 3 sem sobrepor a cobra."
        )
    return food, obstacles


def create_scenario(
    number: int,
    width: int,
    height: int,
    seed: int | None = None,
) -> dict:
    """Retorna snake, food e obstacles para o cenário solicitado.

    Passe seed para reproduzir exatamente uma configuração durante testes.
    Sem seed, o sorteio é diferente a cada criação do cenário.
    """
    if width < 5 or height < 5:
        raise ValueError("O tabuleiro deve ter pelo menos 5x5.")

    rng = random.Random(seed)
    snake = _initial_snake(width, height)
    food = (min(width - 2, width // 2 + 4), height // 2)

    if number == 1:
        obstacles: set[Position] = set()
    elif number == 2:
        obstacles = _random_obstacles(width, height, snake, food, rng)
    elif number == 3:
        # Deixa a cobra à esquerda para que a câmara fechada caiba mesmo em 7x7.
        start_x = width // 3
        snake = [
            (start_x, height // 2),
            (start_x - 1, height // 2),
            (start_x - 2, height // 2),
        ]
        food, obstacles = _blocked_food_scenario(width, height, snake)
    else:
        raise ValueError("Cenário deve ser 1, 2 ou 3.")

    return {"snake": snake, "food": food, "obstacles": obstacles}
