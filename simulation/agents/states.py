from enum import Enum, auto


class EstadoFuncionario(Enum):
    IDLE = auto()
    ATENDIENDO = auto()
    
class EstadoVotante(Enum):
    INACTIVO = auto()
    ESPERANDOO = auto()
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
    