from mesa import Agent
import numpy as np
from simulation.parameters import N_PARTIES, NOMBRES_PARTIDOS

class BallotBox(Agent):
    def __init__(self, model, pos):
        super().__init__(model)
        self.pos = pos
        self.tipo = "urna"
        # Vector de votos por partido: [MORENA, PAN, PRI, MC, PVEM]
        self.votos = np.zeros(N_PARTIES, dtype=int)
        self.total_votos = 0

    def recibir_voto(self, partido_voto: int):
        if partido_voto is not None and 0 <= partido_voto < len(self.votos):
            self.votos[partido_voto] += 1
            self.total_votos += 1
            print(f"[URNA] Voto registrado para: {NOMBRES_PARTIDOS[partido_voto]}")

    def step(self):
        pass