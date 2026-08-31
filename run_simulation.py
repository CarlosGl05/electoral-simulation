import os
import time
import subprocess
from simulation.model import VotationModel
from simulation.parameters import N_VOTERS

if __name__ == "__main__":
  modelo = VotationModel(n=N_VOTERS)
  
  subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
  modelo.imprimir_estado_actual(0)
  time.sleep(0.5)
  
  tick = 1
  
  while tick < modelo.ticks_totales:
    modelo.step()
    
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    modelo.imprimir_estado_actual(tick)
    
    time.sleep(0.25)
    tick += 1
    
  print("\n¡Simulación terminada con éxito!")

modelo.imprimir_reporte_final()