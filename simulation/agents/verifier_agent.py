from mesa import Agent
from simulation.agents.voter_agent import EstadoVotante
from simulation.agents.states import EstadoFuncionario, EstadoVotante

class FuncionarioCasilla(Agent):
    def __init__(self, model, pos):
      super().__init__(model)
      self.estado:EstadoFuncionario = EstadoFuncionario.IDLE
      self.tiempo_atencion = 0
      self.votante_actual = None  
      self.tipo = "funcionario"

    def step(self):
      if self.estado == EstadoFuncionario.ATENDIENDO:
        self.tiempo_atencion -= 1
            
        if self.tiempo_atencion <= 0:
          self.estado = EstadoFuncionario.IDLE
            
          if self.votante_actual:
            self.votante_actual.estado = EstadoVotante.IR_A_VOTAR
            self.votante_actual = None