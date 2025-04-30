import random
from utils.perguntas_fixas import PERGUNTAS_FIXAS

def gerar_prova_mensal():
    prova = []
    for materia, perguntas in PERGUNTAS_FIXAS.items():
        if perguntas:
            pergunta_aleatoria = random.choice(perguntas)
            prova.append({
                "materia": materia,
                "pergunta": pergunta_aleatoria["pergunta"],
                "nivel": pergunta_aleatoria["nivel"]
            })

    print("🧠 PROVA MENSAL (Simulação):\n")
    for item in prova:
        print(f"📘 {item['materia']} ({item['nivel']}): {item['pergunta']}")

if __name__ == "__main__":
    gerar_prova_mensal()
