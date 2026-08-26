from mesa.discrete_space import CellAgent
from enum import Enum, auto

class EstadoFuncionario(Enum):
    IDLE = auto()
    ATENDIENDO = auto()

class FuncionarioCasilla(CellAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.estado:EstadoFuncionario = EstadoFuncionario.IDLE
        self.tiempo_atencion = 0
        self.votante_actual = None 

    def step(self):
        if self.estado == "ATENDIENDO":
            self.tiempo_atencion -= 1
            
            if self.tiempo_atencion <= 0:
                self.estado = EstadoFuncionario.ATENDIENDO
            
                if self.votante_actual:
                    self.votante_actual.estado = "YENDO_A_MAMPARA"
                    self.votante_actual = None