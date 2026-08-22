# Electoral Simulation Engine — Mesa & Unity Architecture

Sistema de simulación multiagente para el modelado de una casilla electoral desarrollado con **Mesa (Python)**, cálculo vectorial con **NumPy/Pandas**, y desacoplado mediante una **API REST (Flask)** para su posterior visualización e interacción 3D en **Unity**.

---

## 📁 Estructura del Repositorio

```text
electoral-simulation/
│
├── .gitignore                  # Exclusión de archivos binarios, venv y temporales
├── README.md                   # Documentación general y guía de instalación
├── requirements.txt            # Lista de dependencias del proyecto
├── run_simulation.py           # Script para ejecución y pruebas locales del modelo Mesa
│
├── simulation/                 # Backend del motor multiagente y lógica matemática
│   ├── __init__.py
│   ├── agents/                 # Definición de agentes individuales
│   │   ├── __init__.py
│   │   ├── voter_agent.py      # Agente Votante (reactivo, estocástico, Softmax)
│   │   ├── verifier_agent.py   # Agente Verificador (validación de ID en fila)
│   │   └── officer_agent.py    # Agente Funcionario de Casilla (recepción y conteo)
│   │
│   ├── model.py                # PollingStationModel (orquestador del entorno Mesa)
│   ├── math_engine.py          # Funciones estadísticas (Sigmoide, Softmax, Bernoulli, Multinomial)
│   └── parameters.py           # Configuración global, constantes (N, K) y matrices de pesos
│
├── api/                        # Capa de comunicación HTTP para visualización
│   ├── __init__.py
│   ├── app.py                  # Servidor Flask y endpoints REST (/step, /state, /reset)
│   └── serializers.py          # Serialización del estado de Mesa a payloads JSON planos
│
└── tests/                      # Pruebas unitarias automatizadas
    ├── __init__.py
    ├── test_math.py            # Validación de consistencia matemática y normalización
    └── test_agents.py          # Pruebas de ciclos de vida y estados de agentes
```

---

# 📚 Descripción de Módulos y Scripts

## 1. Raíz del Proyecto

### `requirements.txt`

Lista de dependencias del proyecto:

* `mesa`
* `numpy`
* `pandas`
* `flask`
* `flask-cors`
* `openpyxl`
* `pytest`

### `run_simulation.py`

Punto de entrada para ejecutar el ciclo de simulación directamente en consola sin levantar el servidor HTTP, imprimiendo tablas de conteo final, proporciones e intervalos de confianza.

---

# 2. Módulo `simulation/`

Módulo correspondiente al **motor multiagente y la lógica matemática** de la simulación.

## `agents/voter_agent.py`

Define la clase `VoterAgent`, correspondiente al agente **Votante**.

El agente cuenta con:

* Vector de atributos sociodemográficos:

$$
z_i =
\begin{bmatrix}
\text{Edad} \
\text{Ingreso} \
\text{Ideología}
\end{bmatrix}
\in [0,1]^3
$$

* Propensión a votar ($p_{T,i}$).
* Evaluación de afinidades mediante producto punto.
* Muestreo categórico del voto mediante **Softmax**.

---

## `agents/verifier_agent.py`

Modela al agente **Verificador**, encargado de:

* Validar la vigencia de la identificación en el padrón electoral a la entrada de la casilla.
* Gestionar la fila preferencial.

---

## `agents/officer_agent.py`

Modela al agente **Funcionario de Casilla**, encargado de:

* La recepción de votos en la urna.
* La actualización en tiempo real del acumulado por partido.
* La totalización final.

---

## `model.py`

Contiene la clase `PollingStationModel`, responsable de:

* Instanciar el espacio de simulación.
* Coordinar el scheduler de Mesa.
* Ejecutar los recolectores de métricas (`DataCollector`).
* Sincronizar los *steps*.

---

## `math_engine.py`

Contiene las funciones estadísticas y probabilísticas vectorizadas:

* Función logística (**Sigmoide**).
* **Softmax**.
* Ensayos de **Bernoulli**.
* Distribución **Multinomial**.

---

## `parameters.py`

Contiene la configuración centralizada del modelo:

* Tamaño de padrón: $N$ = Definido por el usuario.
* Número de partidos: $K$ = Definidos por el usuario.
* Coeficientes logísticos $\boldsymbol{\gamma}$.
* Matrices de pesos de afinidad partidista $\boldsymbol{\beta}$.

---

# 3. Módulo `api/`

Capa encargada de la **comunicación entre Mesa y Unity** mediante HTTP.

## `app.py`

Servidor HTTP construido con **Flask** y soporte para **CORS**.

Expone los siguientes endpoints REST:

| Endpoint | Función                                   |
| -------- | ----------------------------------------- |
| `/reset` | Reinicia la simulación                    |
| `/step`  | Ejecuta un paso de simulación             |
| `/state` | Obtiene el estado actual de la simulación |

---

## `serializers.py`

Contiene las funciones de transformación que mapean:

* Los objetos internos de Mesa.
* Las coordenadas de Mesa.

A estructuras **JSON serializadas y legibles para `UnityWebRequest` en C#**.

---

# 4. Módulo `tests/`

Módulo destinado a las **pruebas unitarias automatizadas** del proyecto.

## `test_math.py`

Pruebas unitarias para validar propiedades matemáticas críticas.

Por ejemplo:

* La suma de probabilidades generadas por Softmax sea idénticamente $1.0$.
* La función sigmoide permanezca acotada en $(0, 1)$.

---

## `test_agents.py`

Pruebas de integración de estados para verificar las transiciones de los agentes:

* Asistencia.
* Abstención.
* Rechazo de credenciales.
* Depósito de votos.

---

# ⚙️ Guía de Configuración del Entorno Virtual

## 1. Prerrequisitos

Antes de comenzar, es necesario contar con:

* **Python 3.12.10** instalado en el sistema.
* **Git** instalado.

---

## 2. Creación del Entorno Virtual (`venv`)

Abre una terminal en la raíz del proyecto y ejecuta:

```bash
py -3.12 -m venv venv
```

---

## 3. Activación del Entorno Virtual

### Windows — PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

> **Nota:** Si PowerShell restringe la ejecución de scripts por directiva de seguridad, ejecuta previamente:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### Windows — Símbolo del sistema (CMD)

```dos
.\venv\Scripts\activate.bat
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

# 📦 4. Instalación de Dependencias

Con el entorno virtual activado, actualiza el gestor de paquetes e instala las librerías listadas en `requirements.txt`.

### Actualizar `pip`

```bash
python -m pip install --upgrade pip
```

### Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

# ✅ Verificación de la Instalación

Comprueba que todas las dependencias críticas se encuentren correctamente enlazadas ejecutando:

### Validar importación de librerías principales

```bash
python -c "import mesa, flask, numpy, pandas; print('Entorno configurado correctamente.')"
```

### Ejecutar el conjunto de pruebas unitarias

```bash
pytest
```

---

## 🚀 Flujo General del Proyecto

La arquitectura del proyecto se organiza en las siguientes capas:

```text
┌───────────────────────────────────────┐
│               Unity                  │
│       Visualización e interacción    │
│                  3D                  │
└───────────────────┬───────────────────┘
                    │
                    │ HTTP / REST
                    ▼
┌───────────────────────────────────────┐
│                Flask                  │
│       /reset   /step   /state         │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────┐
│                Mesa                   │
│         PollingStationModel           │
│                                       │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ Votantes │ │Verificador│ │Oficial│ │
│  └──────────┘ └──────────┘ └────────┘ │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────┐
│           Motor Matemático            │
│                                       │
│  Sigmoide │ Softmax │ Bernoulli       │
│           │ Multinomial               │
└───────────────────────────────────────┘
```

La arquitectura permite mantener desacoplados el **motor de simulación**, la **capa de comunicación HTTP** y la **visualización 3D en Unity**.
