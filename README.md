# 🗳️ Electoral Simulation Engine

### Multi-Agent Electoral Simulation · Mesa · FastAPI · WebSockets · Unity

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Mesa](https://img.shields.io/badge/Mesa-Multi--Agent-FF6F00?style=for-the-badge)](https://mesa.readthedocs.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Async-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![WebSockets](https://img.shields.io/badge/WebSocket-Real--Time-010101?style=for-the-badge\&logo=websocket\&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![Unity](https://img.shields.io/badge/Unity-3D-000000?style=for-the-badge\&logo=unity\&logoColor=white)](https://unity.com/)
[![NumPy](https://img.shields.io/badge/NumPy-Vectorized-013243?style=for-the-badge\&logo=numpy\&logoColor=white)](https://numpy.org/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=for-the-badge\&logo=pytest\&logoColor=white)](https://pytest.org/)

> **Motor de simulación multiagente para modelar el comportamiento estocástico de una casilla electoral y transmitir su estado en tiempo real hacia una experiencia 3D desarrollada en Unity.**

---

## 🧠 ¿Qué es este proyecto?

**Electoral Simulation Engine** es un sistema de simulación multiagente diseñado para representar el funcionamiento interno de una **casilla electoral** mediante agentes autónomos, modelos probabilísticos y comunicación en tiempo real.

El núcleo de la simulación está desarrollado con **Mesa**, mientras que el procesamiento matemático utiliza **NumPy, Pandas y SciPy**.

La arquitectura está desacoplada mediante una API asíncrona desarrollada con **FastAPI + WebSockets**, permitiendo que un cliente externo —en este caso **Unity**— pueda controlar y visualizar la simulación en tiempo real.

### 🎯 Objetivo

Modelar computacionalmente el flujo de una casilla electoral:

```text
                    🧑 VOTANTE
                        │
                        ▼
              ┌─────────────────┐
              │   VERIFICACIÓN  │
              │       🪪        │
              └────────┬────────┘
                       │
                 ¿Credencial?
                   /        \
                 ❌          ✅
                 │            │
                 ▼            ▼
              RECHAZO       VOTACIÓN
                               │
                               ▼
                       ┌──────────────┐
                       │    URNA 🗳️   │
                       └──────┬───────┘
                              │
                              ▼
                       📊 ACUMULADO
```

---

# 🏗️ Arquitectura

El sistema sigue una arquitectura desacoplada en capas:

```text
┌───────────────────────────────────────────────────────────────┐
│                           UNITY 3D                            │
│                                                               │
│        Visualización · Interacción · Animación · UI           │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               │ WebSocket
                               │ JSON
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                       FASTAPI + UVICORN                       │
│                                                               │
│                     WebSocket /ws                             │
│                                                               │
│              Commands  ◄──────────────►  State               │
│              step/reset                 updates               │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               │ Simulation Control
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                         MESA ENGINE                           │
│                                                               │
│                    PollingStationModel                        │
│                                                               │
│     ┌───────────┐    ┌────────────┐    ┌──────────────┐       │
│     │  Voters   │    │ Verifier   │    │   Officer    │       │
│     │    🧑     │    │    🪪      │    │     👮       │       │
│     └───────────┘    └────────────┘    └──────────────┘       │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                       MATH ENGINE                             │
│                                                               │
│      Sigmoid · Softmax · Bernoulli · Multinomial              │
│                                                               │
│                    NumPy / SciPy                              │
└───────────────────────────────────────────────────────────────┘
```

### 🔌 Comunicación

| Capa           | Tecnología    | Responsabilidad                 |
| -------------- | ------------- | ------------------------------- |
| 🎮 Frontend    | Unity         | Visualización e interacción 3D  |
| 🔄 Transporte  | WebSocket     | Comunicación bidireccional      |
| ⚡ API          | FastAPI       | Gestión asíncrona de conexiones |
| 🚀 Server      | Uvicorn       | Ejecución ASGI                  |
| 🤖 Simulación  | Mesa          | Gestión de agentes y pasos      |
| 📐 Matemáticas | NumPy / SciPy | Modelos probabilísticos         |
| 🧪 Testing     | Pytest        | Validación automatizada         |

---

# 📁 Estructura del Proyecto

```text
electoral-simulation/
│
├── 📄 .gitignore
├── 📄 README.md
├── 📄 requirements.txt
├── 🐍 run_simulation.py
│
├── simulation/
│   ├── __init__.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── voter_agent.py
│   │   ├── verifier_agent.py
│   │   └── officer_agent.py
│   │
│   ├── model.py
│   ├── math_engine.py
│   └── parameters.py
│
├── api/
│   ├── __init__.py
│   ├── app.py
│   └── serializers.py
│
└── tests/
    ├── __init__.py
    ├── test_math.py
    └── test_agents.py
```

---

# 🤖 Sistema Multiagente

El modelo representa una casilla electoral mediante diferentes tipos de agentes.

## 🧑 VoterAgent

Representa a cada votante dentro de la simulación.

Cada agente posee un vector de características:

$$
z_i =
\begin{bmatrix}
\text{Edad}\
\text{Ingreso}\
\text{Ideología}
\end{bmatrix}
\in [0,1]^3
$$

Estas variables intervienen en la toma de decisiones del agente.

### Características

* 🎲 Comportamiento estocástico
* 📊 Vector de atributos sociodemográficos
* 🧮 Evaluación mediante producto punto
* 🧠 Selección de partido mediante Softmax
* 🗳️ Decisión entre votar o abstenerse

---

## 🪪 VerifierAgent

Representa al agente encargado de verificar al elector.

### Responsabilidades

* Validar la identificación.
* Consultar la vigencia del elector.
* Gestionar la entrada a la casilla.
* Administrar la fila preferencial.
* Determinar si el votante puede continuar con el proceso.

```text
Voter
  │
  ▼
Verifier
  │
  ├── ❌ Invalid ID ──► Rejected
  │
  └── ✅ Valid ID ────► Voting Queue
```

---

## 👮 OfficerAgent

Representa al funcionario encargado del proceso electoral.

### Responsabilidades

* Recibir el voto.
* Registrar el partido seleccionado.
* Actualizar los acumulados.
* Gestionar la urna.
* Realizar la totalización final.

```text
        Vote
         │
         ▼
┌─────────────────┐
│ OfficerAgent    │
├─────────────────┤
│ Party A → +1    │
│ Party B → +1    │
│ Party C → +1    │
│ Party D → +1    │
│ Party E → +1    │
└─────────────────┘
         │
         ▼
    Final Count
```

---

# 📐 Motor Matemático

El comportamiento de los agentes se basa en modelos probabilísticos.

## Sigmoide

La función logística se utiliza para transformar una combinación lineal de variables en una probabilidad:

$$
\sigma(x)=\frac{1}{1+e^{-x}}
$$

con:

$$
0 < \sigma(x) < 1
$$

---

## Softmax

La elección partidista se modela mediante una distribución Softmax:

$$
P(Y_i=k)=
\frac{e^{s_k}}
{\sum_{j=1}^{K}e^{s_j}}
$$

donde $s_k$ representa el nivel de afinidad del votante hacia el partido $k$.

Por construcción:

$$
\sum_{k=1}^{K}P(Y_i=k)=1
$$

---

## Bernoulli

La decisión de participar en la elección se modela como un ensayo Bernoulli:

$$
X_i \sim Bernoulli(p_i)
$$

donde:

* $X_i=1$ → el ciudadano participa.
* $X_i=0$ → el ciudadano se abstiene.

---

## Multinomial

La distribución de votos finales puede representarse mediante:

$$
X \sim Multinomial(n,p_1,\ldots,p_K)
$$

donde:

$$
\sum_{k=1}^{K}p_k=1
$$

---

# ⚙️ Configuración del Modelo

La configuración global se centraliza en:

```text
simulation/parameters.py
```

Incluye:

| Parámetro | Descripción                     |
| --------- | ------------------------------- |
| `N`       | Tamaño del padrón simulado      |
| `K`       | Número de partidos              |
| `γ`       | Coeficientes logísticos         |
| `β`       | Matrices de afinidad partidista |

Esto permite modificar los escenarios experimentales sin alterar directamente la lógica de los agentes.

---

# 🌐 API en Tiempo Real

La capa `api/` conecta el motor Mesa con Unity.

## WebSocket

```text
ws://localhost:8000/ws
```

El canal permite comunicación bidireccional:

```text
Unity                         FastAPI
  │                              │
  │─────── {"command":"step"} ──►│
  │                              │
  │◄────── Simulation State ─────│
  │                              │
  │────── {"command":"reset"} ──►│
  │                              │
  │◄────── Initial State ────────│
```

### Comandos principales

| Comando | Acción                |
| ------- | --------------------- |
| `step`  | Avanza la simulación  |
| `reset` | Reinicia el escenario |

El estado de la simulación se transmite como **JSON**, facilitando su consumo desde C# dentro de Unity.

---

# 📡 Endpoints

| Protocolo    | Endpoint | Descripción                       |
| ------------ | -------- | --------------------------------- |
| 🔄 WebSocket | `/ws`    | Canal bidireccional de simulación |
| 🌐 HTTP      | `/docs`  | Swagger UI de FastAPI             |

Servidor local:

```text
http://localhost:8000
```

Documentación interactiva:

```text
http://localhost:8000/docs
```

---

# 🔄 Serialización

El archivo:

```text
api/serializers.py
```

se encarga de transformar los objetos internos de Mesa en estructuras JSON simples.

```text
Mesa Objects
     │
     ▼
Serializer
     │
     ▼
Plain JSON
     │
     ▼
WebSocket
     │
     ▼
Unity / C#
```

Esto evita que Unity tenga que conocer la implementación interna del motor de simulación.

---

# 🧪 Testing

El proyecto incorpora pruebas automatizadas mediante **Pytest**.

### `test_math.py`

Valida propiedades fundamentales del motor matemático:

* Normalización de Softmax.
* Rango de la función sigmoide.
* Consistencia de probabilidades.
* Propiedades de las distribuciones.

### `test_agents.py`

Comprueba transiciones importantes de los agentes:

```text
┌──────────────┐
│    Voter     │
└──────┬───────┘
       │
       ├──► Attendance
       │
       ├──► Abstention
       │
       ├──► Credential Rejection
       │
       └──► Vote Deposit
```

Ejecutar todas las pruebas:

```bash
pytest
```

---

# 📦 Dependencias

```text
Mesa
NumPy
Pandas
SciPy
FastAPI
Uvicorn
WebSockets
OpenPyXL
Pytest
```

Instalación automática:

```bash
pip install -r requirements.txt
```

---

# 🚀 Instalación

## 1. Prerrequisitos

Se recomienda contar con:

* Python **3.14**
* Git
* Unity para la visualización 3D

---

## 2. Clonar el repositorio

```bash
git clone <repository-url>

cd electoral-simulation
```

---

## 3. Crear entorno virtual

### Windows

```powershell
py -3.14 -m venv venv
```

### macOS / Linux

```bash
python3 -m venv venv
```

---

## 4. Activar entorno

### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### CMD

```cmd
.\venv\Scripts\activate.bat
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

# 📥 Instalación de Dependencias

Actualizar `pip`:

```bash
python -m pip install --upgrade pip
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

# ✅ Verificación

Comprobar las principales dependencias:

```bash
python -c "import mesa, fastapi, uvicorn, websockets, numpy, pandas; print('✓ Entorno configurado correctamente.')"
```

Si aparece:

```text
✓ Entorno configurado correctamente.
```

el entorno está listo.

---

# ▶️ Ejecución

## 🖥️ Simulación local

Para ejecutar únicamente el motor Mesa:

```bash
python run_simulation.py
```

Esto permite observar:

* Conteo final.
* Proporciones.
* Resultados de la simulación.
* Intervalos de confianza.

---

## 🌐 Servidor WebSocket

Para iniciar el backend:

```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
```

Servidor:

```text
http://localhost:8000
```

WebSocket:

```text
ws://localhost:8000/ws
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 🎮 Integración con Unity

La arquitectura está diseñada para que Unity funcione como **cliente visual**, mientras Python mantiene el control de la simulación.

```text
┌───────────────────────┐
│       PYTHON          │
│                       │
│   Mesa Simulation     │
│          │            │
│          ▼            │
│       FastAPI         │
│          │            │
│          ▼            │
│      WebSocket        │
└───────────┬───────────┘
            │
            │ JSON
            │
            ▼
┌───────────────────────┐
│        UNITY          │
│                       │
│    C# WebSocket       │
│          │            │
│          ▼            │
│      3D Scene         │
│          │            │
│          ▼            │
│   User Interaction    │
└───────────────────────┘
```

### Responsabilidades

**Python / Mesa**

* Estado de la simulación.
* Agentes.
* Probabilidades.
* Reglas electorales.
* Conteos.
* Estadística.

**Unity**

* Renderizado 3D.
* Animaciones.
* Interfaz.
* Cámara.
* Visualización de agentes.
* Interacción del usuario.

Esta separación permite modificar la representación visual sin modificar el motor matemático.

---

# 📊 Flujo de una Simulación

```text
              START
                │
                ▼
       ┌─────────────────┐
       │ Initialize Mesa │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Create Agents   │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Generate Traits │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Voting Decision │
       └────────┬────────┘
                │
          ┌─────┴─────┐
          │           │
      Abstention     Vote
          │           │
          │           ▼
          │      ┌──────────┐
          │      │ Softmax  │
          │      └────┬─────┘
          │           │
          │           ▼
          │      Party Choice
          │           │
          └─────┬─────┘
                │
                ▼
       ┌─────────────────┐
       │ Update Counters │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Collect Metrics │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Serialize JSON  │
       └────────┬────────┘
                │
                ▼
              UNITY
```

---

# 🧩 Principios de Diseño

El proyecto está construido alrededor de cuatro principios:

### 1. 🔓 Desacoplamiento

Mesa no depende de Unity.

Unity no necesita conocer la implementación interna de Mesa.

La comunicación ocurre mediante JSON + WebSocket.

### 2. ⚡ Comunicación asíncrona

FastAPI y WebSockets permiten transmitir eventos y estados sin depender de polling HTTP tradicional.

### 3. 🧮 Computación vectorizada

Las operaciones matemáticas se implementan utilizando NumPy/SciPy para reducir operaciones iterativas innecesarias.

### 4. 🧪 Testeabilidad

La lógica matemática y los agentes se validan independientemente mediante pruebas automatizadas.

---

# 🛠️ Stack Tecnológico

```text
┌───────────────────────────────────────────┐
│                  STACK                    │
├───────────────────────────────────────────┤
│                                           │
│  🐍 Python 3.14                           │
│  🤖 Mesa                                  │
│  🔢 NumPy / SciPy / Pandas                │
│  ⚡ FastAPI + Uvicorn                      │
│  🔄 WebSockets                             │
│  🎮 Unity + C#                             │
│  🧪 Pytest                                 │
│                                           │
└───────────────────────────────────────────┘
```

---

# 📈 Escenarios Experimentales

El motor puede utilizarse para experimentar con diferentes configuraciones:

```text
N = Número de electores

K = Número de partidos

β = Afinidades partidistas

γ = Coeficientes de participación

p = Probabilidades de voto
```

Modificar estos parámetros permite estudiar cómo cambios en las características de la población afectan el resultado agregado de la elección.

---

# 🔮 Roadmap

* [x] 🤖 Implementación de agentes
* [x] 📐 Motor matemático
* [x] 🧪 Pruebas unitarias
* [x] ⚡ API asíncrona
* [x] 🔄 Comunicación WebSocket
* [ ] 🎮 Cliente Unity
* [ ] 🏙️ Escenario 3D de la casilla
* [ ] 👥 Visualización de agentes en tiempo real
* [ ] 📊 Dashboard estadístico
* [ ] ⏱️ Control temporal de la simulación
* [ ] 💾 Persistencia de escenarios
* [ ] 📈 Comparación entre múltiples simulaciones

---

# 📚 Conceptos involucrados

Este proyecto integra conceptos de:

* Multi-Agent Systems
* Modelado estocástico
* Simulación computacional
* Probabilidad y estadística
* Distribuciones Bernoulli y Multinomial
* Regresión logística
* Softmax
* Computación vectorizada
* Arquitecturas cliente-servidor
* Comunicación WebSocket
* APIs asíncronas
* Visualización 3D
* Testing automatizado

---

# 👨‍💻 Proyecto

**Electoral Simulation Engine**

> Un puente entre **modelado matemático, sistemas multiagente, comunicación en tiempo real y visualización 3D**.

```text
          MATHEMATICS
               │
               ▼
        ┌─────────────┐
        │    MESA     │
        │  Simulation │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   FASTAPI   │
        │  WebSocket  │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │    UNITY    │
        │     3D      │
        └─────────────┘
```

### 🗳️ Simulate. Connect. Visualize.
