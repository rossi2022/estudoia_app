# backend/tests/test_voz.py

from fastapi.testclient import TestClient
from io import BytesIO
from backend.main import app

client = TestClient(app)

def test_envio_audio_sem_conteudo():
    fake_audio = BytesIO(b"")  # Simula um áudio vazio
    response = client.post(
        "/voz/avaliar",
        files={"arquivo_audio": ("audio.wav", fake_audio, "audio/wav")}
    )
    # Aceita 422 (validação) ou 400 (sem conteúdo)
    assert response.status_code in [400, 422]


