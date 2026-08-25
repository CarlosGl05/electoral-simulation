from mesa import CellAgent # O CellAgent dependiendo de tu versión de Mesa
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
ruta_a_mesa = [[0,0], [0,1], [0,2]]
ruta_a_casilla = [[0,2], [0,3], [0,4]]
ruta_a_urna = [[0,5], [0,6], [0,7]]
ruta_a_rechazado = [[0,2], [1,2], [1,3]]
ruta_a_salida = [[0,2], [1,2], [1,3]]
ruta_a_urna_pref = [[0,2], [1,2], [1,3]]
    

class Voter(CellAgent): 
    def __init__(self, model, cell, voter_data: VoterData):
        super().__init__(model)
        self.cell = cell
        self.data = voter_data # Recibe los datos ya instanciados
        self.estado: EstadoVotante = EstadoVotante.IR_A_MESA
        
        # IMPORTANTE: Hacemos una COPIA de la ruta para este agente
        self.ruta = list(ruta_a_mesa) 
        self.tipo = "votante"
    
    def step(self):
        if self.estado == EstadoVotante.IR_A_MESA:
            self.seguir_ruta(self.ruta)
            if len(self.ruta) == 0:
                self.solicitar_atencion()
                self.estado = EstadoVotante.ESPERANDO_ATENCION
                
        elif self.estado == EstadoVotante.ESPERANDO_ATENCION:
            pass
            
        elif self.estado == EstadoVotante.IR_A_VOTAR:
            # Hacemos copia de la nueva ruta
            if len(self.ruta) == 0 and self.pos == (0,2): # Validamos que apenas inicie la fase
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
            
        elif self.estado == EstadoVotante.HUYENDO:
            # Aquí iría la lógica si sale corriendo
            pass
    
    # Nota: self.ruta ya es una variable del agente, no necesitas pasarla como parámetro
    def seguir_ruta(self):
        pass  
  
    def solicitar_atencion(self):
        pass
  
    def votar(self):
        # Logica pesada de la decision
        pass