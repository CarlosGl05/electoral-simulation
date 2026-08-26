import mesa
from simulation.agents.object_agent import Objeto
from simulation.agents.verifier_agent import FuncionarioCasilla
from simulation.agents.voter_agent import Voter, VoterData
from simulation.agents.states import EstadoVotante
import random

from mesa.space import SingleGrid

class VotationModel(mesa.Model):
  def __init__(self, n=50, width=8, height=8, seed=None):
    super().__init__(seed=seed)
    self.grid = SingleGrid(width, height, torus=False)
    self.total_votantes = n
    self.votantes_generados = 0 
    self.votos = 0
    self.agentes_fuera = 0
    self.pool_votantes = []
    self.cola_de_llegada = []
    
    mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 3, 1, 0, 1, 4, 1], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 2, 0, 0, 0], 
            [0, 0, 1, 1, 1, 1, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
        ]
    
    self.crear_votantes()
    self.cargar_mapa(mapa)
    
  def crear_votantes(self):
    for i in range(self.total_votantes):
      
      sexo = random.choices(["F", "M"], weights=[0.52, 0.48])[0]
      nivel_random = random.choices(["Bajo", "Medio", "Alto"], weights=[0.50, 0.35, 0.15])[0]    
      edad = int(random.gauss(42, 15))
      edad = max(18, min(edad, 90))
      

      v_data = VoterData(id=i, edad=edad, sexo=sexo, economico=nivel_random)
      votante_dormido = Voter(self, None, v_data) 
      self.pool_votantes.append(votante_dormido)
    
  def cargar_mapa(self, mapa):
    for row_idx, fila in enumerate(mapa):
      y = self.grid.height - 1 - row_idx
      
      for x, valor in enumerate(fila):
        if valor == 1:
          obs = Objeto(self, (x, y), tipo="obstaculo")
          self.grid.place_agent(obs, (x, y))
        elif valor == 2:
          func = FuncionarioCasilla(self, (x, y))
          self.grid.place_agent(func, (x, y))
        elif valor == 3:
          obs = Objeto(self, (x, y), tipo="mampara")
          self.grid.place_agent(obs, (x, y))
        elif valor == 4:
          obs = Objeto(self, (x, y), tipo="urna")
          self.grid.place_agent(obs, (x, y))
  
  def step(self):
    self.agents.do("step")

    if self.votantes_generados < self.total_votantes:
      if len(self.cola_de_llegada) > 0 and self.grid.is_cell_empty((7, 0)):
        votante_activo = self.cola_de_llegada.pop(0)
        votante_activo.estado = EstadoVotante.IR_A_MESA
        
        self.grid.place_agent(votante_activo, (7, 0))
        
        self.votantes_generados += 1

  def imprimir_estado_actual(self, tick):
    print(f"\n{'='*15} TICK {tick} {'='*15}")
    
    print("MAPA:")
    for y in range(self.grid.height - 1, -1, -1):
      fila_texto = ""
      for x in range(self.grid.width):
        celda = self.grid.get_cell_list_contents([(x, y)])
        
        if not celda:
          fila_texto += ".  " 
        else:
          agente = celda[0]
          if agente.tipo == "votante":
            fila_texto += f"V{agente.data.id} "
          elif agente.tipo == "funcionario":
            fila_texto += "F  "
          elif agente.tipo == "mampara":
            fila_texto += "M  "
          elif agente.tipo == "urna":
            fila_texto += "U  "
          elif agente.tipo == "obstaculo":
            fila_texto += "█  " 
      print(fila_texto)

    # --- NUEVA SECCIÓN DE ESTADÍSTICAS ---
    print("\nESTADÍSTICAS GENERALES:")
    print(f"  ➜ Votantes Registrados: {len(self.pool_votantes)}")
    print(f"  ➜ Votantes Esperando: {len(self.cola_de_llegada)}")
    print(f"  ➜ Votantes Generados: {self.votantes_generados} / {self.total_votantes}")
    print(f"  ➜ Votos en la Urna:   {self.votos}")
    print(f"  ➜ Votantes Fuera:     {self.agentes_fuera} / {self.total_votantes}")

    print("\nESTADOS DE LOS AGENTES:")
    for agente in self.agents:
      if agente.tipo == "votante":
        
        # Extraemos los datos del perfil del votante
        sexo = agente.data.sexo
        edad = agente.data.edad
        nivel = agente.data.economico
        
        # Formateamos el perfil para que se vea limpio
        perfil = f"({sexo}, {edad} años, Nivel {nivel})"
        
        # Imprimimos toda la información junta
        print(f"  Votante {agente.data.id} {perfil} en {agente.pos} -> {agente.estado.name}")
        
      elif agente.tipo == "funcionario":
        print(f"  Funcionario en {agente.pos} -> {agente.estado.name}")
    print("="*39)

