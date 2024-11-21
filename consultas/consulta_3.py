def consultar_eventos_rio(cursor):
    cursor.execute('''
    SELECT e.nome, de.data, de.localizacao, e.tipo
    FROM Eventos e
    JOIN DadosEventos de ON e.id = de.id_evento
    WHERE de.localizacao LIKE '%RJ%' OR de.localizacao LIKE '%Rio de Janeiro%'
    ''')
    eventos = cursor.fetchall()
    for evento in eventos:
        print(f"Nome: {evento[0]}, Data: {evento[1]}, Localização: {evento[2]}, Tipo: {evento[3]}")
