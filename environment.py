"""Regras do ambiente Snake, independentes da interface e de qualquer agente."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import random

Position = tuple[int, int]  # (coluna, linha)
Direction = tuple[int, int]

DIRECTIONS: dict[str, Direction] = {
    "UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)
}
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
VECTOR_TO_NAME = {v: k for k, v in DIRECTIONS.items()}

@dataclass
class StepResult:
    moved: bool
    ate_food: bool = False
    collision: Optional[str] = None
    won: bool = False

class SnakeEnvironment:
    """Ambiente observável: o agente poderá consultar get_state() e agir via step()."""
    def __init__(self, width: int = 20, height: int = 15,
                 obstacles: Optional[set[Position]] = None,
                 initial_snake: Optional[list[Position]] = None,
                 initial_food: Optional[Position] = None, seed: Optional[int] = None):
        if width < 5 or height < 5:
            raise ValueError("O tabuleiro deve ter pelo menos 5x5.")
        self.width, self.height = width, height
        self.obstacles = set(obstacles or ())
        self._rng = random.Random(seed)
        self._initial_snake = list(initial_snake or [
            (width // 2, height // 2),
            (width // 2 - 1, height // 2),
            (width // 2 - 2, height // 2),
        ])
        self._initial_food = initial_food
        self.reset()

    def reset(self) -> None:
        self.snake = list(self._initial_snake)  # cabeça primeiro
        self.direction = "RIGHT"
        self.food = self._initial_food
        self.score = 0
        self.steps = 0
        self.game_over = False
        self.won = False
        self.end_reason = None
        self._validate_configuration()
        if self.food is None:
            self.food = self._random_free_cell()
        elif self.food in self.snake or self.food in self.obstacles:
            raise ValueError("A fruta inicial não pode ocupar cobra/obstáculo.")
        if self.food is None:
            self.won = self.game_over = True
            self.end_reason = "tabuleiro_sem_celulas_livres"

    def _validate_configuration(self) -> None:
        for p in self.obstacles:
            if not self._inside(p):
                raise ValueError(f"Obstáculo fora do tabuleiro: {p}")
        if len(set(self.snake)) != len(self.snake):
            raise ValueError("A cobrinha inicial não pode ocupar a mesma célula duas vezes.")
        for p in self.snake:
            if not self._inside(p):
                raise ValueError(f"Cobrinha fora do tabuleiro: {p}")
            if p in self.obstacles:
                raise ValueError(f"Obstáculo sobre a cobrinha: {p}")
        if len(self.snake) < 1:
            raise ValueError("A cobrinha precisa ter ao menos um segmento.")

    def _inside(self, p: Position) -> bool:
        x, y = p
        return 0 <= x < self.width and 0 <= y < self.height

    def _random_free_cell(self) -> Optional[Position]:
        occupied = set(self.snake) | self.obstacles
        free = [(x, y) for y in range(self.height) for x in range(self.width)
                if (x, y) not in occupied]
        return self._rng.choice(free) if free else None

    def get_state(self) -> dict:
        """Contrato de integração para os agentes futuros."""
        return {
            "width": self.width,
            "height": self.height,
            "snake": tuple(self.snake),
            "head": self.snake[0],
            "food": self.food,
            "obstacles": frozenset(self.obstacles),
            "direction": self.direction,
            "score": self.score,
            "steps": self.steps,
            "game_over": self.game_over,
            "won": self.won,
            "end_reason": self.end_reason,
        }

    def valid_moves(self) -> list[str]:
        """Ações localmente válidas; não garante que a partida inteira seja vencível."""
        if self.game_over:
            return []
        valid = []
        for name, (dx, dy) in DIRECTIONS.items():
            if len(self.snake) > 1 and name == OPPOSITE[self.direction]:
                continue
            target = (self.snake[0][0] + dx, self.snake[0][1] + dy)
            growing = target == self.food
            body_to_check = self.snake if growing else self.snake[:-1]
            if not self._inside(target) or target in self.obstacles or target in body_to_check:
                continue
            valid.append(name)
        return valid

    def set_direction(self, direction: str) -> bool:
        direction = direction.upper()
        if direction not in DIRECTIONS:
            return False
        if len(self.snake) > 1 and direction == OPPOSITE[self.direction]:
            return False
        self.direction = direction
        return True

    def step(self, direction: Optional[str] = None) -> StepResult:
        if self.game_over:
            return StepResult(False, won=self.won, collision=self.end_reason)
        if direction is not None:
            self.set_direction(direction)
        dx, dy = DIRECTIONS[self.direction]
        head = self.snake[0]
        target = (head[0] + dx, head[1] + dy)
        growing = target == self.food

        if not self._inside(target):
            self.game_over, self.end_reason = True, "parede"
            return StepResult(False, collision="parede")
        if target in self.obstacles:
            self.game_over, self.end_reason = True, "obstaculo"
            return StepResult(False, collision="obstaculo")
        # A cauda sai nesta jogada quando não há crescimento.
        body_to_check = self.snake if growing else self.snake[:-1]
        if target in body_to_check:
            self.game_over, self.end_reason = True, "proprio_corpo"
            return StepResult(False, collision="proprio_corpo")

        self.snake.insert(0, target)
        ate_food = growing
        if ate_food:
            self.score += 1
        else:
            self.snake.pop()
        self.steps += 1

        if ate_food:
            self.food = self._random_free_cell()
            if self.food is None:
                self.won = self.game_over = True
                self.end_reason = "tabuleiro_preenchido"
        return StepResult(True, ate_food=ate_food, won=self.won)

    def execute_action(self, action: str) -> StepResult:
        """Alias explícito para facilitar a integração com o agente."""
        return self.step(action)
