"""Renderização Pygame; sem regras de jogo ou lógica de IA."""
import pygame
from environment import DIRECTIONS

BACKGROUND = (22, 25, 34)
GRID = (49, 55, 68)
SNAKE_HEAD = (116, 220, 138)
SNAKE_BODY = (54, 166, 104)
FOOD = (240, 91, 105)
OBSTACLE = (130, 137, 153)
TEXT = (235, 238, 245)

class SnakeRenderer:
    def __init__(self, width: int, height: int, cell_size: int = 32):
        pygame.init()
        self.width, self.height, self.cell_size = width, height, cell_size
        self.top = 52
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size + self.top))
        pygame.display.set_caption("Snake IA — ambiente base")
        self.font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 19)

    def key_to_direction(self, key):
        mapping = {
            pygame.K_UP: "UP", pygame.K_w: "UP",
            pygame.K_DOWN: "DOWN", pygame.K_s: "DOWN",
            pygame.K_LEFT: "LEFT", pygame.K_a: "LEFT",
            pygame.K_RIGHT: "RIGHT", pygame.K_d: "RIGHT",
        }
        return mapping.get(key)

    def draw(self, env, paused=False):
        cs = self.cell_size
        self.screen.fill(BACKGROUND)
        status = "PAUSADO" if paused else ("VITÓRIA" if env.won else
                 ("FIM DE JOGO" if env.game_over else "JOGANDO"))
        header = self.font.render(
            f"Snake IA   |   Frutas: {env.score}   |   Passos: {env.steps}   |   {status}",
            True, TEXT)
        self.screen.blit(header, (10, 16))
        for y in range(env.height):
            for x in range(env.width):
                rect = pygame.Rect(x * cs, self.top + y * cs, cs, cs)
                pygame.draw.rect(self.screen, GRID, rect, 1)
                p = (x, y)
                if p in env.obstacles:
                    pygame.draw.rect(self.screen, OBSTACLE, rect.inflate(-5, -5), border_radius=4)
                    pygame.draw.line(self.screen, BACKGROUND, rect.topleft, rect.bottomright, 2)
                    pygame.draw.line(self.screen, BACKGROUND, rect.topright, rect.bottomleft, 2)
        if env.food is not None:
            x, y = env.food
            pygame.draw.circle(self.screen, FOOD,
                (x * cs + cs // 2, self.top + y * cs + cs // 2), max(4, cs // 3))
        for i, (x, y) in enumerate(env.snake):
            rect = pygame.Rect(x * cs + 2, self.top + y * cs + 2, cs - 4, cs - 4)
            pygame.draw.rect(self.screen, SNAKE_HEAD if i == 0 else SNAKE_BODY,
                             rect, border_radius=max(3, cs // 5))
        if env.game_over:
            message = "Tabuleiro preenchido!" if env.won else f"Fim: {env.end_reason}"
            surf = self.font.render(message + "  |  R para reiniciar", True, TEXT)
            self.screen.blit(surf, (10, env.height * cs + self.top - 27))
        pygame.display.flip()
