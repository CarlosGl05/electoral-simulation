from mesa import Agent

class Objeto(Agent):
    def __init__(self, model, pos, tipo = "objeto"):
      super().__init__(model)
      self.tipo = tipo


    def step(self):
      pass