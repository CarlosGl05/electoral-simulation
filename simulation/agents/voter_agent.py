from mesa import Agent
from dataclasses import dataclass
from simulation.agents.states import EstadoFuncionario, EstadoVotante
import random

@dataclass
class VoterData:
    id: int
    edad: int
    sexo: str
    economico: str # Nivel socioeconmico
    discapacitado: bool = False
   

# Rutas base globales
ruta_a_mesa = [(6,0), (5,0), (4, 0)]
ruta_a_casilla = [(3,0), (2,0), (1,0), (1,1), (1,2), (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3), (7,4), (7,5), (6,5), (5,5), (4,5), (3,5), (2,5), (1,5), (1,6), (1,7), (2,7)]
ruta_a_urna = [(3,7), (4,7), (5,7), (6,7)]
ruta_a_rechazado = [(4,0)]
ruta_a_salida = [(6,7), (7,7)]
ruta_a_casilla_pref = [(3,0), (2,0), (1,0), (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (1,7), (2,7)]
    

class Voter(Agent): 
    def __init__(self, model, pos, voter_data: VoterData):
      super().__init__(model)
      self.data = voter_data # Recibe los datos ya instanciados
      self.estado: EstadoVotante = EstadoVotante.INACTIVO
      self.estadoAnterior: EstadoVotante = EstadoVotante.INACTIVO
      
      self.ruta = list(ruta_a_mesa) 
      self.tipo = "votante"
      self.tiempo_votando = 10
      self.tiempo_en_urna = 2
    
    def step(self):
          
      if self.estado == EstadoVotante.INACTIVO:
        # TODO: Cambiar para que considere el vector de caracteristicas
        if random.random() < 0.005: 
          self.estado = EstadoVotante.ESPERANDO
          self.model.cola_de_llegada.append(self)
        return
          
      if self.estado == EstadoVotante.PLATICANDO:
        self.seguir_ruta()
        return
      
      if self.estado == EstadoVotante.IR_A_MESA:
        self.seguir_ruta()
        if len(self.ruta) == 0:
          self.estado = EstadoVotante.ESPERANDO_ATENCION
              
      elif self.estado == EstadoVotante.ESPERANDO_ATENCION:
        self.solicitar_atencion()
        self.ruta = list(ruta_a_casilla)
          
      elif self.estado == EstadoVotante.IR_A_VOTAR:
        self.seguir_ruta()
              
        if len(self.ruta) == 0:
          self.estado = EstadoVotante.VOTANDO
              
      elif self.estado == EstadoVotante.VOTANDO:
      
        self.tiempo_votando -= 1
        if self.tiempo_votando <= 0:
          self.votar()
          self.estado = EstadoVotante.IR_A_URNA
          self.ruta = list(ruta_a_urna)
          
      elif self.estado == EstadoVotante.IR_A_URNA:
        self.seguir_ruta()
        
        if len(self.ruta) == 0:
          self.estado = EstadoVotante.COLOCANDO_VOTO
              
      elif self.estado == EstadoVotante.COLOCANDO_VOTO:
        self.tiempo_en_urna -= 1
        if self.tiempo_en_urna <= 0:
          self.estado = EstadoVotante.IR_A_SALIDA
          self.ruta = list(ruta_a_salida)
          self.model.votos += 1
          
          
      # Falta implementar
      elif self.estado == EstadoVotante.RECHAZADO:
        if len(self.ruta) == 0:
            self.ruta = list(ruta_a_rechazado)
        self.seguir_ruta()
          
      elif self.estado == EstadoVotante.IR_A_SALIDA:  
        if len(self.ruta) == 0 and self.pos == (7,7):
          self.model.agentes_fuera += 1
          self.model.grid.remove_agent(self)
          self.model.agents.remove(self)
          return
              
        self.seguir_ruta()
         
      elif self.estado == EstadoVotante.HUYENDO:
          # Aquí iría la lógica si sale corriendo
          pass
    
      print("Estado: ", self.estado)
    
    def seguir_ruta(self):
      if len(self.ruta) > 0:
        siguiente_paso = self.ruta[0] 
        
        if siguiente_paso == self.pos:
            self.ruta.pop(0)
            return
        
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
        print(f"Votante {self.data.id} solicitando atencion")
        
        x, y = self.pos
        coordenada_func = (x, y + 2) 
        
        agentes_enfrente = self.model.grid.get_cell_list_contents([coordenada_func])
        
        for agente in agentes_enfrente:
            if agente.tipo == "funcionario":
                if agente.estado == EstadoFuncionario.IDLE:
                    agente.estado = EstadoFuncionario.ATENDIENDO
                    agente.votante_actual = self
                    agente.tiempo_atencion = 3
                    print(f"Funcionario atendiendo al votante {self.data.id}")
                break
  
    def votar(self):
        pass