import numpy as np

# Configuración de simulación
N_VOTERS = 100
N_PARTIES = 5
TICKPERMIN = 0.5 

NOMBRES_PARTIDOS = [
    "MORENA",
    "PAN",
    "PRI",
    "MC",
    "PVEM"
]


#Popularidad inicial / Inercia de voto)
BETA_INTERCEPTS = np.array([
    0.45,   # MORENA: Alta popularidad base / voto duro
   -0.05,   # PAN: Oposición consolidada
   -0.35,   # PRI: Voto de castigo / desgaste de marca
    0.10,   # MC: Crecimiento y presencia mediática
   -0.15    # PVEM: Desempeño condicionado por coaliciones
])

# Matriz de pesos beta: (5 partidos x 4 variables demográficas)
# Columnas del vector z: [Edad (0 a 1), Sexo (F=1, M=0), Nivel_Económico (0 a 1), Discapacidad (1 o 0)]
BETA_WEIGHTS = np.array([
    # [Edad,  Sexo(F), Económico, Discapacidad]
    [  0.8,    0.2,     -1.4,          1.2  ],  # MORENA: Adultos mayores, clases populares, inclusión
    [  0.4,   -0.1,      1.6,         -0.2  ],  # PAN: Clases medias-altas/altas, adultos
    [  0.9,    0.0,     -0.3,          0.1  ],  # PRI: Retención en adultos mayores tradicionales
    [ -1.5,    0.3,      0.5,          0.2  ],  # MC: Fuerte atractivo en jóvenes (18-35 años) y clases medias
    [ -0.4,    0.2,     -0.2,          0.3  ]   # PVEM: Captación joven/urbana y transversal
])













