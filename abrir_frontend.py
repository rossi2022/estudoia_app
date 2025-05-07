# abrir_frontend.py
import subprocess
import webbrowser
import time
import os

# Caminho para o diretório raiz do projeto (ajuste se necessário)
diretorio_projeto = os.path.dirname(os.path.abspath(__file__))

# Comando para iniciar o backend com Uvicorn
comando_backend = ["uvicorn", "backend.main:app", "--reload"]

# Função principal
def iniciar_tudo():
    print("Iniciando backend...")
    subprocess.Popen(comando_backend, cwd=diretorio_projeto)
    
    print("Aguardando o backend iniciar...")
    time.sleep(3)  # aguarda o backend estar no ar

    print("Abrindo navegador na rota do frontend...")
    webbrowser.open("http://127.0.0.1:8000")  # ou dashboard se preferir

if __name__ == "__main__":
    iniciar_tudo()

