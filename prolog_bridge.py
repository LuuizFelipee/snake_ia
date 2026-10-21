"""Ponte entre Python e SWI-Prolog usando PySwip."""
from __future__ import annotations

from pathlib import Path
from pyswip import Prolog


class PrologRules:
    """Carrega fatos do estado atual e consulta posições válidas em Prolog."""

    def __init__(self, rules_file: str | Path | None = None):
        self.prolog = Prolog()
        if rules_file is None:
            rules_file = Path(__file__).resolve().parent / "logic" / "snake_rules.pl"
        self.prolog.consult(str(Path(rules_file).resolve()))

    def valid_positions(self, state: dict) -> set[tuple[int, int]]:
        """Retorna todas as células válidas conforme as regras Prolog."""
        # Limpa apenas os fatos dinâmicos deste módulo antes de inserir o estado novo.
        list(self.prolog.query("retractall(board_size(_, _))"))
        list(self.prolog.query("retractall(obstacle(_, _))"))
        list(self.prolog.query("retractall(snake_segment(_, _))"))

        width, height = int(state["width"]), int(state["height"])
        list(self.prolog.query(f"assertz(board_size({width}, {height}))"))

        for x, y in state["obstacles"]:
            list(self.prolog.query(f"assertz(obstacle({int(x)}, {int(y)}))"))

        # Não bloqueamos a cabeça; os demais segmentos ficam como bloqueios
        # estáticos para esta busca. A próxima decisão usará o corpo atualizado.
        for x, y in state["snake"][1:]:
            list(self.prolog.query(f"assertz(snake_segment({int(x)}, {int(y)}))"))

        results = self.prolog.query("valid_position(X, Y)")
        return {(int(row["X"]), int(row["Y"])) for row in results}
