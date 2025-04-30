from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_estudo_guiado_pergunta():
    resp = client.get(
        "/estudo/guiado/pergunta",
        params={"materia": "Matemática", "topico": "Trigonometria"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "pergunta" in data
    assert isinstance(data["pergunta"], str)
    assert "dicas" in data and isinstance(data["dicas"], list)
