"""Busca em largura (BFS) para encontrar um caminho mínimo no grid."""
from __future__ import annotations
from collections import deque

Position = tuple[int, int]
# A ordem fixa deixa os resultados determinísticos quando há vários caminhos mínimos.
NEIGHBORS: tuple[tuple[str, Position], ...] = (
    ("UP", (0, -1)),
    ("RIGHT", (1, 0)),
    ("DOWN", (0, 1)),
    ("LEFT", (-1, 0)),
)


def breadth_first_search(
    start: Position, goal: Position, allowed_positions: set[Position]
) -> list[str] | None:
    """Retorna ações do caminho mínimo, ou None se não houver caminho.

    Cada movimento tem custo unitário. A lista retornada não inclui a posição
    inicial; contém nomes de ações compatíveis com SnakeEnvironment.step().
    """
    if start == goal:
        return []
    if goal not in allowed_positions:
        return None

    frontier = deque([start])
    came_from: dict[Position, tuple[Position, str] | None] = {start: None}

    while frontier:
        current = frontier.popleft()
        if current == goal:
            break

        for action, (dx, dy) in NEIGHBORS:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor not in allowed_positions or neighbor in came_from:
                continue
            came_from[neighbor] = (current, action)
            frontier.append(neighbor)

    if goal not in came_from:
        return None

    actions: list[str] = []
    current = goal
    while current != start:
        previous, action = came_from[current]  # type: ignore[misc]
        actions.append(action)
        current = previous
    actions.reverse()
    return actions
