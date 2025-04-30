# backend/verificar_rotas.py

import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app  # ✅ Agora deve funcionar

print("\n✅ Rotas disponíveis no FastAPI:\n")
for route in app.routes:
    print(f"🔹 {route.path}")








