# estudoia_app/run_backend.py

import subprocess
import os

# Caminho até a pasta do backend
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)

# Roda o servidor FastAPI (Uvicorn)
subprocess.run(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])
