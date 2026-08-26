import os
import time
import subprocess
from simulation.model import VotationModel

if __name__ == "__main__":
  modelo = VotationModel(n=10)
  
  subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
  modelo.imprimir_estado_actual(0)
  time.sleep(0.5)
  
  tick = 1
  
  while modelo.agentes_fuera < modelo.total_votantes:
    modelo.step()
    
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    modelo.imprimir_estado_actual(tick)
    
    time.sleep(0.25)
    tick += 1
    
  print("\n¡Simulación terminada con éxito!")