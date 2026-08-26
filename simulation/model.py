import mesa

from mesa.space import SingleGrid

class VotationModel(mesa.Model):
  def __init__(self, n=50, width=8, height=8, seed=None):
    super().__init__(seed=seed)
    self.grid = SingleGrid(width, height, torus=False)
    
    mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 4, 1, 0, 1, 3, 1], 
            [0, 0, 0, 0, 1, 0, 1, 4], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 2, 0, 0, 0], 
            [0, 0, 1, 1, 1, 1, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
        ]
    
    self.cargar_mapa(mapa)
    
    