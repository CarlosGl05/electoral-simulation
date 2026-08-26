from mesa.discrete_space import CellAgent
from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class VoterData:
    id: int
    edad: int
    sexo: str
    economico: str # Nivel socioeconmico
    discapacitado: bool = False
   
class EstadoVotante(Enum):
    IDLE = auto()
    PLATICANDO = auto()
    IR_A_MESA = auto()
    ESPERANDO_ATENCION = auto()
    IR_A_VOTAR = auto()
    VOTANDO = auto()
    IR_A_URNA = auto()
    COLOCANDO_VOTO = auto()
    IR_A_SALIDA =auto()
    RECHAZADO = auto()
    HUYENDO = auto() 
    
# Rutas base globales
ruta_a_mesa = [(0,0), (0,1), (0,2)]
ruta_a_casilla = [(0,2), (0,3), (0,4)]
ruta_a_urna = [(0,5), (0,6), (0,7)]
ruta_a_rechazado = [(0,2), (1,2), (1,3)]
ruta_a_salida = [(0,2), (1,2), (1,3)]
ruta_a_urna_pref = [(0,2), (1,2), (1,3)]
    

class Voter(CellAgent): 
    def __init__(self, model, cell, voter_data: VoterData):
      super().__init__(model)
      self.cell = cell
      self.data = voter_data # Recibe los datos ya instanciados
      self.estado: EstadoVotante = EstadoVotante.IR_A_MESA
      self.estadoAnterior: EstadoVotante = EstadoVotante.IDLE
      
      self.ruta = list(ruta_a_mesa) 
      self.tipo = "votante"
    
    def step(self):
          
      if self.estado == EstadoVotante.PLATICANDO:
        self.seguir_ruta()
        return
      
      if self.estado == EstadoVotante.IR_A_MESA:
        self.seguir_ruta()
        if len(self.ruta) == 0:
          self.solicitar_atencion()
          self.estado = EstadoVotante.ESPERANDO_ATENCION
              
      elif self.estado == EstadoVotante.ESPERANDO_ATENCION:
        pass
          
      elif self.estado == EstadoVotante.IR_A_VOTAR:
    
        if len(self.ruta) == 0:
          self.ruta = list(ruta_a_casilla)
        self.seguir_ruta()
              
        if len(self.ruta) == 0:
          self.estado = EstadoVotante.VOTANDO
          self.votar()
              
      elif self.estado == EstadoVotante.VOTANDO:
        pass  
          
      elif self.estado == EstadoVotante.IR_A_URNA:
        if len(self.ruta) == 0: 
          self.ruta = list(ruta_a_urna)
        self.seguir_ruta()
        
        if len(self.ruta) == 0:
          self.estado = EstadoVotante.COLOCANDO_VOTO
              
      elif self.estado == EstadoVotante.COLOCANDO_VOTO:
        pass
          
      elif self.estado == EstadoVotante.RECHAZADO:
        if len(self.ruta) == 0:
            self.ruta = list(ruta_a_rechazado)
        self.seguir_ruta()
          
      elif self.estado == EstadoVotante.IR_A_SALIDA:
        if len(self.ruta) == 0:
          self.ruta = list(ruta_a_salida)
        self.seguir_ruta()
                
      elif self.estado == EstadoVotante.HUYENDO:
          # Aquí iría la lógica si sale corriendo
          pass
    
    def seguir_ruta(self):
      if len(self.ruta) > 0:
        siguiente_paso = self.ruta[0] 
        
        if self.model.grid.is_cell_empty(siguiente_paso):
          self.model.grid.move_agent(self, siguiente_paso)
          self.ruta.pop(0) 
        
          if self.estado == EstadoVotante.PLATICANDO:
            self.estado = self.estadoAnterior
          
        else:
          vecinos = self.model.grid.get_cell_list_contents([siguiente_paso])
          for agente in vecinos:
            if agente.tipo == "votante":
              if self.estado != EstadoVotante.PLATICANDO:
                self.platicar(agente)
              break

    def platicar(self, vecino):
        self.estadoAnterior = self.estado
        self.estado = EstadoVotante.PLATICANDO
        
        if self.data.economico == vecino.data.economico:
        
            pass
            
        diferencia_edad = abs(self.data.edad - vecino.data.edad)
        if diferencia_edad > 20:
            pass
          
    def solicitar_atencion(self):
        print("Solicitando atencion")
  
    def votar(self):
        # Logica pesada de la decision
        print("Votando")