import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.ai_module import gerar_explicacao

pergunta = "Explique o que foi a Revolução Francesa."
resposta = gerar_explicacao(pergunta)
print("🔎 Explicação gerada pela IA:\n")
print(resposta)

