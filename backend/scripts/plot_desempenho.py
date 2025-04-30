import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

data = {
    "desempenho": {
        "História": [
            {"data": "2025-04-23", "acertos": 3, "erros": 1},
            {"data": "2025-04-24", "acertos": 4, "erros": 1},
            {"data": "2025-04-24", "acertos": 6, "erros": 1},
            {"data": "2025-04-24", "acertos": 5, "erros": 2},
            {"data": "2025-04-25", "acertos": 2, "erros": 3},
            {"data": "2025-04-25", "acertos": 3, "erros": 1}
        ],
        "Matemática": [
            {"data": "2025-04-25", "acertos": 4, "erros": 1}
        ]
    }
}

# Montar DataFrame
records = []
for materia, entries in data["desempenho"].items():
    for entry in entries:
        records.append({
            "data": datetime.fromisoformat(entry["data"]),
            "materia": materia,
            "acertos": entry["acertos"]
        })

df = pd.DataFrame(records)

# Usa pivot_table para lidar com duplicatas
pivot_df = df.pivot_table(
    index='data',
    columns='materia',
    values='acertos',
    aggfunc='sum'
).fillna(0)

# Plotando
plt.figure()
for materia in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[materia], label=materia)
plt.xlabel("Data")
plt.ylabel("Acertos")
plt.title("Desempenho de Acertos por Matéria ao Longo do Tempo")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

