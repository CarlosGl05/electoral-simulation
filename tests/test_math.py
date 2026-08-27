import os
import sys
import numpy as np

# Asegura que Python encuentre la carpeta 'simulation'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulation.math_engine import calculate_utilities, softmax, normalizar_vector_votante
from simulation.parameters import BETA_INTERCEPTS, BETA_WEIGHTS, NOMBRES_PARTIDOS

def probar_perfiles():
    print("\n" + "="*20 + " PRUEBA DE PERFILES " + "="*20)
    
    # 1. Perfil Joven, Bajo NSE
    z_joven_bajo = normalizar_vector_votante(edad=19, sexo="M", economico="bajo", discapacitado=False)
    probs_1 = softmax(calculate_utilities(z_joven_bajo, BETA_INTERCEPTS, BETA_WEIGHTS))
    print("\n--- Perfil: 19 años, Nivel Bajo ---")
    for nombre, p in zip(NOMBRES_PARTIDOS, probs_1):
        print(f"  {nombre:<10}: {p*100:5.2f}%")

    # 2. Perfil Adulto, Alto NSE
    z_adulto_alto = normalizar_vector_votante(edad=55, sexo="F", economico="alto", discapacitado=False)
    probs_2 = softmax(calculate_utilities(z_adulto_alto, BETA_INTERCEPTS, BETA_WEIGHTS))
    print("\n--- Perfil: 55 años, Nivel Alto ---")
    for nombre, p in zip(NOMBRES_PARTIDOS, probs_2):
        print(f"  {nombre:<10}: {p*100:5.2f}%")
    print("="*58 + "\n")

if __name__ == "__main__":
    probar_perfiles()