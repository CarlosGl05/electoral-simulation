from mesa import Agent
from dataclasses import dataclass
from simulation.agents.states import EstadoFuncionario, EstadoVotante
import random

from simulation.math_engine import normalizar_vector_votante, calculate_utilities, softmax, sample_vote
from simulation.parameters import BETA_INTERCEPTS, BETA_WEIGHTS, NOMBRES_PARTIDOS
import math

@dataclass
class VoterData:
    id: int
    edad: int
    sexo: str
    economico: str # Nivel socioeconmico
    discapacitado: bool = False
    ine_valido: bool = True
   

# Rutas base globales
ruta_a_mesa = [(8,0), (7,0), (6,0), (5,0), (4, 0)]
ruta_a_casilla = [(3,0), (2,0), (1,0), (1,1), (1,2), (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3), (8,3), (9,3), (9,4), (8,4), (7,4), (6,4), (5,4), (4,4), (3,4), (2,4), (1,4), (1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5), (9,5), (9,6), (8,6), (7,6), (6,6), (5,6), (4,6), (3,6), (2,6), (1,6), (1,7), (1,8), (1,9), (2,9)]
ruta_a_urna = [(3,9), (4,9), (5,9), (6,9)]
ruta_a_rechazado = [(4,0)]
ruta_a_salida = [(6,9), (7,9), (8,9), (9,9)]
ruta_a_casilla_pref = [(3,0), (2,0), (1,0), (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (1,9), (2,9)]
    

class Voter(Agent): 
    def __init__(self, model, pos, voter_data: VoterData):
      super().__init__(model)
      self.data = voter_data # Recibe los datos ya instanciados
      self.estado: EstadoVotante = EstadoVotante.INACTIVO
      self.estadoAnterior: EstadoVotante = EstadoVotante.INACTIVO
      
      self.ruta = list(ruta_a_mesa) 
      self.tipo = "votante"
      self.tiempo_votando = 2
      self.tiempo_en_urna = 1

      self.voto_seleccionado: int | None = None
    
    def step(self):
          
      if self.estado == EstadoVotante.INACTIVO:
        prob = self.activacion()
        
        if random.random() < prob: 
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
          self.colocar_voto()
          self.estado = EstadoVotante.IR_A_SALIDA
          self.ruta = list(ruta_a_salida)
          self.model.votos += 1
          
          
      # Falta implementar
      elif self.estado == EstadoVotante.RECHAZADO:
        if len(self.ruta) == 0:
            self.ruta = list(ruta_a_rechazado)
        self.seguir_ruta()
          
      elif self.estado == EstadoVotante.IR_A_SALIDA:  
        if len(self.ruta) == 0 and self.pos == ruta_a_salida[-1]:
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

    def colocar_voto(self):
        
        x, y = self.pos
        coordenada_func = (x, y - 1) 
        
        agentes_enfrente = self.model.grid.get_cell_list_contents([coordenada_func])
        
        for agente in agentes_enfrente:
            if agente.tipo == "urna":
              agente.recibir_voto(self.voto_seleccionado)
              print(f"Votante {self.data.id} colocó su voto en la urna")
            break
          
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
                    agente.tiempo_atencion = 1
                    print(f"Funcionario atendiendo al votante {self.data.id}")
                break
  
    def votar(self):
        z = normalizar_vector_votante(
            edad=self.data.edad,
            sexo=self.data.sexo,
            economico=self.data.economico,
            discapacitado=self.data.discapacitado
        )
        
        # 2. Utilidad, Softmax y Muestreo Categórico
        utilidades = calculate_utilities(z, BETA_INTERCEPTS, BETA_WEIGHTS)
        probabilidades = softmax(utilidades)
        self.voto_seleccionado = sample_vote(probabilidades, rng=self.model.random)
        
    def activacion(self):
      hora_decimal = self.model.hora_actual.hour + self.model.hora_actual.minute / 60.0
        
      if self.data.edad >= 60:
          hora_pico = 9.5   # 9:30 AM (Adultos mayores prefieren la mañana)
          desviacion = 1.5
      elif 30 <= self.data.edad < 60:
          hora_pico = 13.0  # 1:00 PM (Mediodía)
          desviacion = 2.5
      else:
          hora_pico = 16.0  # 4:00 PM (Jóvenes prefieren la tarde)
          desviacion = 2.0

      participacion_esperada = 0.6
           
      C = -math.log(1 - participacion_esperada) 
      ticks_por_hora = 60 / self.model.minutos_por_tick

      factor_escala = C / (2.5066 * desviacion * ticks_por_hora)
      probabilidad = factor_escala * math.exp(-((hora_decimal - hora_pico) ** 2) / (2 * (desviacion ** 2)))
      
      return probabilidad

          