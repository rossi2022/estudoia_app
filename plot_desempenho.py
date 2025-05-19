import json
import os
import codecs
import matplotlib.pyplot as plt

# Determine o diretório do script para salvar os arquivos lá
dir_atual = os.path.dirname(os.path.abspath(__file__))

# Caminhos de entrada e saída
json_path = os.path.join(dir_atual, "desempenho.json")
output1 = os.path.join(dir_atual, "media_por_materia.png")
output2 = os.path.join(dir_atual, "historico_notas.png")

# Carrega o JSON de desempenho com detecção de BOM
with open(json_path, 'rb') as f:
    raw = f.read()
# Detecta BOM UTF-16 LE/BE e decodifica
if raw.startswith(codecs.BOM_UTF16_LE) or raw.startswith(codecs.BOM_UTF16_BE):
    text = raw.decode('utf-16')
else:
    text = raw.decode('utf-8-sig')
# Carrega JSON a partir do texto
data = json.loads(text)

# Extrai o dicionário de desempenho
des = data.get("desempenho", {})
media_por_materia = des.get("media_por_materia", {})
historico_estudos = des.get("historico_estudos", [])

# Filtra placeholders indesejados
if "string" in media_por_materia:
    media_por_materia.pop("string")

# ------------
# Gráfico 1: Média por Matéria
# ------------
fig1 = plt.figure()
plt.bar(media_por_materia.keys(), media_por_materia.values())
plt.title("Média de Nota por Matéria")
plt.xlabel("Matéria")
plt.ylabel("Média de Nota")
plt.xticks(rotation=45)
plt.tight_layout()
fig1.savefig(output1)

# ------------
# Gráfico 2: Histórico de Notas
# ------------
fig2 = plt.figure()
datas = [item.get("data") for item in historico_estudos]
notas = [item.get("nota") for item in historico_estudos]
plt.plot(datas, notas, marker="o")
plt.title("Histórico de Notas")
plt.xlabel("Data")
plt.ylabel("Nota")
plt.xticks(rotation=45)
plt.tight_layout()
fig2.savefig(output2)

print(f"Gráficos gerados: {output1}, {output2}")
