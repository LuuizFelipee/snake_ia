"""Agente que combina BFS em Python com regras de validade em SWI-Prolog."""
from __future__ import annotations
from prolog_bridge import PrologRules
from search import breadth_first_search


class BFSAgent:
    def __init__(self, rules: PrologRules | None = None):
        self.rules = rules or PrologRules()
        self.last_path: list[str] | None = None
        self.last_status = "não executado"

    def find_path(self, state: dict) -> list[str] | None:
        """Planeja a rota atual até a fruta; None significa sem rota encontrada."""
        if state["food"] is None:
            self.last_path = []
            self.last_status = "sem fruta (tabuleiro concluído)"
            return []

        allowed = self.rules.valid_positions(state)
        start = tuple(state["head"])
        goal = tuple(state["food"])
        self.last_path = breadth_first_search(start, goal, allowed)
        self.last_status = "rota encontrada" if self.last_path is not None else "nenhuma rota encontrada"
        return self.last_path

    def choose_action(self, state: dict) -> str | None:
        """Retorna o próximo movimento ou None se não houver rota."""
        path = self.find_path(state)
        return path[0] if path else None
