def consultar_metadados(cursor):
    cursor.execute('''
    SELECT e.nome, m.metadado
    FROM Eventos e
    JOIN Metadados m ON e.id = m.id_evento
    ''')
    metadados = cursor.fetchall()
    for metadado in metadados:
        print(f"Nome: {metadado[0]}, Metadado: {metadado[1]}")
