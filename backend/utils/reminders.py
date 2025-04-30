from datetime import datetime

def gerar_lembrete_estudo(nome_aluno: str, materia: str, horario: str) -> str:
    return f"Olá, {nome_aluno}! Está na hora de estudar {materia}. Seu horário agendado é às {horario}."

def gerar_lembrete_prova(nome_aluno: str, data_prova: str) -> str:
    return f"{nome_aluno}, lembrete: você tem uma prova marcada para o dia {data_prova}. Prepare-se bem!"

def lembrete_diario(nome_aluno: str) -> str:
    return f"Bom dia, {nome_aluno}! Não se esqueça de estudar um pouco hoje. Seu futuro agradece!"

def mensagem_boas_vindas(nome_aluno: str) -> str:
    return f"Seja bem-vindo, {nome_aluno}! Vamos juntos evoluir no seu aprendizado!"
