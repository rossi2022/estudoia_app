import http.server
import socketserver
import threading
import webbrowser
import os

PORT = 5500
DIR = os.path.join(os.path.dirname(__file__), "frontend")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

def abrir_navegador():
    url = f"http://127.0.0.1:{PORT}/index.html"
    webbrowser.open(url)

def iniciar_servidor():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servidor rodando em http://127.0.0.1:{PORT}")
        abrir_navegador()
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=iniciar_servidor).start()
