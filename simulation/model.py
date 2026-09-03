import mesa
from simulation.agents.object_agent import Objeto
from simulation.agents.verifier_agent import FuncionarioCasilla
from simulation.agents.voter_agent import Voter, VoterData
from simulation.agents.states import EstadoVotante
from simulation.agents.BallotBox_agent import BallotBox
import random
from datetime import datetime, timedelta
from simulation.parameters import NOMBRES_PARTIDOS, TICKPERMIN
from mesa.space import SingleGrid

class VotationModel(mesa.Model):
  def __init__(self, n=50, width=10, height=10, seed=None):
    super().__init__(seed=seed)
    self.grid = SingleGrid(width, height, torus=False)
    self.total_votantes = n
    self.votantes_generados = 0 
    self.votos = 0
    self.agentes_fuera = 0
    self.pool_votantes = []
    self.cola_de_llegada = []
    self.ballot_box = None
    
    # Tiempo
    
    fecha_base = datetime(2024, 6, 2) 
    self.hora_inicio = fecha_base.replace(hour=8, minute=0, second=0)
    self.hora_fin = fecha_base.replace(hour=18, minute=0, second=0)
    
    self.hora_actual = self.hora_inicio
    
    self.minutos_por_tick = TICKPERMIN
    self.current_tick = 0       
    
    minutos_totales = (self.hora_fin - self.hora_inicio).total_seconds() / 60
    self.ticks_totales = int(minutos_totales / self.minutos_por_tick)
    
    mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0 es un lugar vacio
            [0, 0, 3, 1, 0, 1, 4, 1, 0, 0], #1 es es un obstaculo
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 2 es el verificador
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 3 es la mampara
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 4 es la urna
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    
    self.crear_votantes()
    self.cargar_mapa(mapa)
    
  def crear_votantes(self):
    for i in range(self.total_votantes):
      
      sexo = random.choices(["F", "M"], weights=[0.52, 0.48])[0]
      nivel_random = random.choices(["Bajo", "Medio", "Alto"], weights=[0.50, 0.35, 0.15])[0]    
      edad = int(random.gauss(55, 15))
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
          self.ballot_box = BallotBox(self, (x, y))
          self.grid.place_agent(self.ballot_box, (x, y))
  
  def step(self):
    self.agents.do("step")

    if self.votantes_generados < self.total_votantes:
      if len(self.cola_de_llegada) > 0 and self.grid.is_cell_empty((9, 0)):
        votante_activo = self.cola_de_llegada.pop(0)
        votante_activo.estado = EstadoVotante.IR_A_MESA
        
        self.grid.place_agent(votante_activo, (9, 0))
        
        self.votantes_generados += 1
        
    self.hora_actual += timedelta(minutes=self.minutos_por_tick)
    self.current_tick += 1

  def get_step_data(self, tick: int) -> dict:
    """Retorna la posición de todos los votantes activos y métricas acumuladas del paso actual."""
    votantes_data = []
    for agente in self.agents:
      if agente.tipo == "votante" and agente.pos is not None:
        votantes_data.append({
            "id": agente.data.id,
            "x": agente.pos[0],
            "y": agente.pos[1],
            "state": agente.estado.name,
            "sexo": agente.data.sexo,
            "edad": agente.data.edad,
            "discapacitado": getattr(agente.data, "discapacitado", False),
        })

    conteo_urna = (
        self.ballot_box.votos.tolist()
        if self.ballot_box is not None
        else [0] * 5
    )

    return {
        "type": "update",
        "tick": tick,
        "voters": votantes_data,
        "metrics": {
            "waiting_line": len(self.cola_de_llegada),
            "voters_out": self.agentes_fuera,
            "total_voters": self.total_votantes,
            "ballot_box": conteo_urna,
        },
  }


#Funciones para imprimir el estado actual del modelo y un reporte final de resultados en consolo, usadas oara pruebas previas
'''
  def imprimir_estado_actual(self, tick):
    hora_str = self.hora_actual.strftime("%H:%M:%S")
    print(f"\n{'='*15} HORA {hora_str} {'='*15}")
    
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
            fila_texto += f"V{agente.data.edad} "
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
    if self.ballot_box is not None:
      print(f"  ➜ Vector Urna:        {self.ballot_box.votos.tolist()}")
    print(f"  ➜ Votantes Fuera:     {self.agentes_fuera} / {self.total_votantes}")



  def imprimir_reporte_final(self):
    print("\n" + "=" * 18 + " RESULTADOS FINALES " + "=" * 18)
    if not self.ballot_box or self.ballot_box.total_votos == 0:
      print("No se registraron votos en la urna.")
      return

    total = self.ballot_box.total_votos
    print(f"Total de votos emitidos: {total}\n")

    for idx, nombre in enumerate(NOMBRES_PARTIDOS):
      conteo = int(self.ballot_box.votos[idx])
      pct = (conteo / total) * 100
      print(f"{nombre:<12} | {conteo:<6} | {pct:6.2f}%")

    ganador_idx = int(self.ballot_box.votos.argmax())
    print("-" * 36)
    print(
        f"GANADOR: {NOMBRES_PARTIDOS[ganador_idx]} con"
        f" {self.ballot_box.votos[ganador_idx]} votos."
    )
    print("=" * 56 + "\n")
'''