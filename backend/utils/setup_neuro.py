# backend/utils/setup_neuro.py

# Função para preparar as atividades de neuroeducação
def preparar_atividade_neuroeducacao():
    """
    Configura a atividade de neuroeducação, como carregar dados ou definir parâmetros.
    Esta função pode ser expandida conforme necessário para configurar mais atividades.
    """
    print("Configurando atividades de neuroeducação...")

    # Exemplo de configuração de atividades
    atividades = {
        "sequencia_logica": {
            "descricao": "Complete a sequência lógica com os números faltantes.",
            "exemplos": [
                "2, 4, 6, __, 10",  # Sequência de exemplo
                "1, 3, 5, __, 9",   # Sequência de exemplo
            ]
        },
        "jogo_memoria": {
            "descricao": "Jogo de memória visual. Combine as cartas.",
            "cartas": ["Carta 1", "Carta 2", "Carta 3", "Carta 4"],
        },
        "labirinto_visual": {
            "descricao": "Resolva o labirinto.",
            "imagem": "caminho/para/labirinto.png",  # Imagem do labirinto
        }
    }

    # Armazenar ou configurar as atividades, isso pode ser mais dinâmico, dependendo de como você deseja organizar as atividades
    # Aqui, estamos apenas retornando o dicionário como exemplo
    return atividades

# Função de exemplo para inicializar atividades no banco de dados ou em outro local
def inicializar_atividades_neuroeducacao(db):
    """
    Inicializa atividades de neuroeducação no banco de dados ou em qualquer outra configuração.
    Pode ser chamada para preparar a base de dados ou configurar algum tipo de cache.
    """
    atividades = preparar_atividade_neuroeducacao()

    # Aqui você pode adicionar a lógica de salvar essas atividades no banco de dados
    # Exemplo de salvar no banco, usando o objeto db
    for atividade, dados in atividades.items():
        # Aqui seria necessário um modelo de banco de dados para salvar as atividades
        # Exemplo fictício:
        # db.add(Atividade(nome=atividade, descricao=dados['descricao']))
        print(f"Atividade '{atividade}' configurada com sucesso.")

    db.commit()  # Salvar as alterações no banco de dados

    return True  # Retorna True para indicar que a configuração foi bem-sucedida
