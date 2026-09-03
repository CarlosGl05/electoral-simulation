import asyncio
import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

# Asegura que encuentre la carpeta 'simulation'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from simulation.model import VotationModel
from simulation.parameters import N_VOTERS

app = FastAPI(title="Servidor de Simulación Electoral Mesa-Unity")


@app.get("/")
def health_check():
  return {"status": "online", "service": "Electoral Simulation Backend"}


@app.websocket("/ws")
async def simulation_websocket(websocket: WebSocket):
  await websocket.accept()
  print("\n>> [FastAPI] Cliente conectado a través del WebSocket.")

  # 1. Instanciación idéntica a tu script previo
  modelo = VotationModel(n=N_VOTERS)

  # Estado inicial (tick 0)
  payload_cero = modelo.get_step_data(0)
  await websocket.send_json(payload_cero)
  await asyncio.sleep(0.5)

  tick = 1

  try:
    # 2. Bucle acotado a ticks_totales
    while tick < modelo.ticks_totales:
      modelo.step()

      # En lugar de imprimir a consola, se transmite a Unity
      payload_update = modelo.get_step_data(tick)
      await websocket.send_json(payload_update)

      # Condición anticipada si todos los agentes ya salieron
      if (
          hasattr(modelo, "agentes_fuera")
          and modelo.agentes_fuera >= modelo.total_votantes
      ):
        print(f">> [FastAPI] Salieron todos los votantes en el tick {tick}.")
        break

      await asyncio.sleep(0.25)
      tick += 1

    # 3. Notificación de cierre a Unity e impresión del reporte en la consola del servidor
    print("\n¡Simulación terminada con éxito!")
    await websocket.send_json({"type": "finished", "final_tick": tick})

    if hasattr(modelo, "imprimir_reporte_final"):
      modelo.imprimir_reporte_final()

  except WebSocketDisconnect:
    print(">> [FastAPI] El cliente desconectó el WebSocket.")
  except Exception as error:
    print(f">> [FastAPI] Excepción durante la simulación: {error}")


if __name__ == "__main__":
  uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)