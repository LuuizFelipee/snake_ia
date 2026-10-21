"""Ponto de entrada do Snake IA. A interface não contém lógica de agente."""
import argparse
import pygame
from environment import SnakeEnvironment
from scenarios import create_scenario
from renderer import SnakeRenderer

def main():
    parser = argparse.ArgumentParser(description="Snake base para integração com agentes de IA")
    parser.add_argument("--scenario", type=int, choices=(1, 2, 3), default=1)
    parser.add_argument("--width", type=int, default=20, help="Número de colunas")
    parser.add_argument("--height", type=int, default=15, help="Número de linhas")
    parser.add_argument("--cell-size", type=int, default=32)
    parser.add_argument("--fps", type=int, default=8)
    parser.add_argument("--agent", choices=("manual", "bfs"), default="manual",
                        help="manual para teclado ou bfs para agente automático")
    args = parser.parse_args()

    agent = None
    if args.agent == "bfs":
        # Importação condicional: o modo manual continua funcionando sem PySwip.
        from agents.bfs_agent import BFSAgent
        agent = BFSAgent()

    scenario = create_scenario(args.scenario, args.width, args.height)
    env = SnakeEnvironment(args.width, args.height, scenario["obstacles"],
                           initial_snake=scenario["snake"], initial_food=scenario["food"])
    renderer = SnakeRenderer(args.width, args.height, args.cell_size)
    clock = pygame.time.Clock()
    running = True
    paused = False

    print("Snake IA — ambiente e agente")
    print("Controles: setas/WASD movem a cobrinha; espaço pausa; R reinicia; ESC sai.")
    print(f"Modo: {args.agent} | cenário {args.scenario}: {args.width}x{args.height}; "
          f"obstáculos={len(env.obstacles)}")
    agent_stopped = False
    last_reported_food = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # Uma nova tentativa recria o cenário. No cenário 2,
                    # isso sorteia uma distribuição nova de obstáculos.
                    scenario = create_scenario(args.scenario, args.width, args.height)
                    env = SnakeEnvironment(
                        args.width,
                        args.height,
                        scenario["obstacles"],
                        initial_snake=scenario["snake"],
                        initial_food=scenario["food"],
                    )
                    agent_stopped = False
                    last_reported_food = None
                    print(
                        f"Nova tentativa — cenário {args.scenario}: "
                        f"obstáculos={len(env.obstacles)}"
                    )
                else:
                    direction = renderer.key_to_direction(event.key)
                    if direction is not None:
                        env.set_direction(direction)

        if not paused and not env.game_over and not agent_stopped:
            if agent is None:
                env.step()
            else:
                state = env.get_state()
                path = agent.find_path(state)
                if path is None:
                    agent_stopped = True
                    print("Agente: nenhuma rota até a fruta foi encontrada. "
                          "A busca terminou sem solução; pressione R para tentar novamente.")
                elif not path:
                    # A fruta já está na posição da cabeça ou o objetivo já foi concluído.
                    agent_stopped = True
                    print("Agente: não há ações pendentes para o objetivo atual.")
                else:
                    if state["food"] != last_reported_food:
                        names = {"UP": "cima", "DOWN": "baixo", "LEFT": "esquerda", "RIGHT": "direita"}
                        readable_path = " → ".join(names[action] for action in path)
                        print(f"Rota até a fruta {state['food']}: {readable_path} "
                              f"({len(path)} movimentos).")
                        last_reported_food = state["food"]
                    env.step(path[0])
                    if env.game_over:
                        print(f"Partida encerrada: {env.end_reason}; pontuação={env.score}")

        renderer.draw(env, paused)
        clock.tick(args.fps)

    pygame.quit()

if __name__ == "__main__":
    main()
