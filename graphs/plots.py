import matplotlib.pyplot as plt

PARTIES = [
    "MORENA",
    "PAN",
    "PRI",
    "MC",
    "PVEM"
]


def plot_age(voters):
    rangos = {
        "18-29": 0,
        "30-44": 0,
        "45-59": 0,
        "60-74": 0,
        "75-90": 0
    }

    for voter in voters:
        edad = voter.data.edad

        if 18 <= edad <= 29:
            rangos["18-29"] += 1
        elif 30 <= edad <= 44:
            rangos["30-44"] += 1
        elif 45 <= edad <= 59:
            rangos["45-59"] += 1
        elif 60 <= edad <= 74:
            rangos["60-74"] += 1
        elif 75 <= edad <= 90:
            rangos["75-90"] += 1

    plt.figure(figsize=(8, 5))
    plt.bar(rangos.keys(), rangos.values())
    plt.title("Cantidad de votantes por edad")
    plt.xlabel("Rango de edad")
    plt.ylabel("Número de votantes")
    plt.tight_layout()
    plt.show()


def plot_gender(voters):
    conteo = {
        "F": 0,
        "M": 0
    }

    for voter in voters:
        conteo[voter.data.sexo] += 1

    plt.figure(figsize=(8, 5))
    plt.bar(conteo.keys(), conteo.values())
    plt.title("Cantidad de votantes por sexo")
    plt.xlabel("Sexo")
    plt.ylabel("Número de votantes")
    plt.tight_layout()
    plt.show()


def plot_economic(voters):
    conteo = {
        "Bajo": 0,
        "Medio": 0,
        "Alto": 0
    }

    for voter in voters:
        conteo[voter.data.economico] += 1

    plt.figure(figsize=(8, 5))
    plt.bar(conteo.keys(), conteo.values())
    plt.title("Cantidad de votantes por nivel económico")
    plt.xlabel("Nivel económico")
    plt.ylabel("Número de votantes")
    plt.tight_layout()
    plt.show()


def plot_disability(voters):
    conteo = {
        "Sin discapacidad": 0,
        "Con discapacidad": 0
    }

    for voter in voters:
        if voter.data.discapacitado:
            conteo["Con discapacidad"] += 1
        else:
            conteo["Sin discapacidad"] += 1

    plt.figure(figsize=(8, 5))
    plt.bar(conteo.keys(), conteo.values())
    plt.title("Cantidad de votantes por discapacidad")
    plt.xlabel("Discapacidad")
    plt.ylabel("Número de votantes")
    plt.tight_layout()
    plt.show()


def plot_results(ballot_box):
    votos = ballot_box.votos.tolist()

    plt.figure(figsize=(8, 5))
    plt.bar(PARTIES, votos)
    plt.title("Resultados de la simulación electoral")
    plt.xlabel("Partido")
    plt.ylabel("Número de votos")
    plt.tight_layout()
    plt.show()