import asyncio
import json
import websockets


async def escuchar_servidor():
  uri = "ws://127.0.0.1:8000/ws"
  print(f">> Conectando a {uri}...")

  try:
    async with websockets.connect(uri) as ws:
      print(">> Conexión establecida. Recibiendo datos de la simulación...\n")

      while True:
        mensaje = await ws.recv()
        datos = json.loads(mensaje)

        # Mensaje de finalización
        if datos.get("type") == "finished":
          print(f"\n>> Simulación terminada en el tick {datos.get('final_tick')}.")
          break

        # Mostrar resumen del tick recibido
        tick = datos.get("tick")
        votantes_activos = len(datos.get("voters", []))
        metricas = datos.get("metrics", {})

        print(
            f"Tick: {tick:03d} | "
            f"Votantes en grid: {votantes_activos:02d} | "
            f"En espera: {metricas.get('waiting_line', 0):02d} | "
            f"Fuera: {metricas.get('voters_out', 0):02d} | "
            f"Urna: {metricas.get('ballot_box', [])}"
        )

        # Muestra el detalle del primer votante activo si existe
        if votantes_activos > 0:
          v = datos["voters"][0]
          print(
              f"   └─ Primer agente [ID {v['id']}]: Pos=({v['x']}, {v['y']}) |"
              f" Estado={v['state']}"
          )

  except ConnectionRefusedError:
    print(">> Error: No se pudo conectar. ¿Olvidaste encender 'server.py'?")
  except websockets.exceptions.ConnectionClosed:
    print(">> El servidor cerró la conexión.")


if __name__ == "__main__":
  asyncio.run(escuchar_servidor())