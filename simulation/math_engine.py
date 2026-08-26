import numpy as np

def normalizar_vector_votante(edad: int, sexo: str, economico: str, discapacitado: bool) -> np.ndarray:
    # Convierte los datos en del vector en un vector normalizado [0-1]
    # 1. Normalizar edad (18 a 90 años)
    edad_norm = float(np.clip((edad - 17.0) / (90.0 - 18.0), 0.0, 1.0))
    
    # 2. Sexo binario (F=1.0, M=0.0)
    sexo_norm = 1.0 if str(sexo).strip().upper() in ["F", "MUJER", "FEMENINO"] else 0.0
    
    # 3. Nivel socioeconómico
    mapa_econ = {
        "alto": 1.0,
        "medio_alto": 0.75,
        "medio": 0.5,
        "medio_bajo": 0.3,
        "bajo": 0.1
    }
    economico_norm = mapa_econ.get(str(economico).strip().lower(), 0.5)
    
    # 4. Discapacidad (True=1.0, False=0.0)
    disc_norm = 1.0 if bool(discapacitado) else 0.0
    
    return np.array([edad_norm, sexo_norm, economico_norm, disc_norm])


def calculate_utilities(z: np.ndarray, beta_0: np.ndarray, beta_w: np.ndarray) -> np.ndarray:
    #vector de utilidades deterministas para cada partido, es decir la posibilidad de que un votante vote por cada partido
    #usa la sigmoide
    return beta_0 + np.dot(beta_w, z)


def softmax(utilities: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    #uso de la función softmax para convertir las utilidades en probabilidades de voto
    shifted = (utilities / temperature) - np.max(utilities / temperature)
    exp_u = np.exp(shifted)
    return exp_u / np.sum(exp_u)


def sample_vote(probabilities: np.ndarray, rng) -> int:
    #muestreo de un voto basado en las probabilidades calculadas
    opciones = list(range(len(probabilities)))
    return int(rng.choices(opciones, weights=probabilities, k=1)[0])