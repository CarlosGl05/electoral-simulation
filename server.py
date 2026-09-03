import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

from simulation.model import VotationModel

app = FastAPI(title="Servidor de Simulación Electoral Mesa-Unity")


@app.get("/")
def health_check():
  return {"status": "online", "service": "Electoral Simulation Backend"}


@app.websocket("/ws")
async def simulation_websocket(websocket: WebSocket):
  await websocket.accept()
  print("\n>> [FastAPI] Cliente conectado a través del WebSocket.")

  # 1. Instanciar la simulación para la sesión
  modelo = VotationModel(n=50, seed=42)

  tick = 0
  cadencia_segundos = 0.25  # 250 ms por paso (4 ticks/segundo)

  try:
    while True:
      # Avanzar la simulación en Mesa
      modelo.step()

      # Serializar y enviar actualización a Unity
      payload_update = modelo.get_step_data(tick)
      await websocket.send_json(payload_update)

      # Condición de finalización
      if modelo.agentes_fuera >= modelo.total_votantes:
        print(f"\n>> [FastAPI] Simulación completada en el tick {tick}.")
        await websocket.send_json({"type": "finished", "final_tick": tick})
        break

      tick += 1
      await asyncio.sleep(cadencia_segundos)

  except WebSocketDisconnect:
    print(">> [FastAPI] El cliente de Unity cerró la conexión.")
  except Exception as error:
    print(f">> [FastAPI] Excepción no controlada en la transmisión: {error}")


if __name__ == "__main__":
  uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)