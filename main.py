import urllib.request
import sqlite3
import time
import logging

from bs4 import BeautifulSoup
from consultas import consulta_1, consulta_2, consulta_3, consulta_4, consulta_5

logging.basicConfig(filename="scraping_errors.log", level=logging.ERROR)


def extract_event_data(event_div):
    try:
        evento_id = event_div.get('data-bannerid')
        evento_nome = event_div.get('data-name', 'Desconhecido')
        evento_tipo = event_div.get('data-creative', '').split('.')[3] if event_div.get(
            'data-creative') else 'Desconhecido'
        return evento_id, evento_nome, evento_tipo
    except Exception as e:
        logging.error(f"Erro ao extrair dados do evento: {e}")
        return None, None, None


def get_event_details(event_url, headers):
    eventos_extraidos = 0
    eventos_com_erro = 0
    start_time = time.time()

    try:
        req = urllib.request.Request(event_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read()

        soup = BeautifulSoup(html, 'html.parser')
        eventos = []
        event_divs = soup.find_all('a', class_='sympla-card')

        for event_id_counter, event in enumerate(event_divs, start=1):
            evento_id, evento_nome, evento_tipo = extract_event_data(event)

            if evento_id:
                eventos_extraidos += 1
                eventos.append({
                    'id': event_id_counter,
                    'nome': evento_nome,
                    'tipo': evento_tipo
                })
            else:
                eventos_com_erro += 1

        for evento in eventos:
            print(f"ID: {evento['id']}, Nome: {evento['nome']}, Tipo: {evento['tipo']}")

    except urllib.error.HTTPError as e:
        logging.error(f"Erro HTTP ao acessar a URL {event_url}: {e}")
    except urllib.error.URLError as e:
        logging.error(f"Erro de rede (URL) ao acessar a URL {event_url}: {e}")
    except Exception as e:
        logging.error(f"Erro geral durante o scraping da URL {event_url}: {e}")

    end_time = time.time()
    tempo_total = end_time - start_time

    generate_report('Detalhes', eventos_extraidos, eventos_com_erro, tempo_total)

    return eventos


def get_event_data(event_url, headers):
    eventos_extraidos = 0
    eventos_com_erro = 0
    start_time = time.time()  # Marcar o tempo de início

    try:
        req = urllib.request.Request(event_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read()

        soup = BeautifulSoup(html, 'html.parser')
        eventos = []
        event_divs = soup.find_all('a', class_='sympla-card')

        for event_id_counter, event in enumerate(event_divs, start=1):
            evento_id = event.get('data-bannerid')
            evento_nome = event.get('data-name')
            evento_tipo = event.get('data-creative').split('.')[3] if event.get('data-creative') else 'Desconhecido'
            evento_data = event.find('div', class_='qtfy413 qtfy414').text.strip() if event.find('div',
                                                                                                 class_='qtfy413 qtfy414') else 'Desconhecido'
            evento_localizacao = event.find('p', class_='pn67h1a').text.strip() if event.find('p',
                                                                                              class_='pn67h1a') else 'Desconhecido'

            if evento_id:
                eventos_extraidos += 1
                eventos.append({
                    'id': event_id_counter,
                    'nome': evento_nome,
                    'tipo': evento_tipo,
                    'data': evento_data,
                    'localizacao': evento_localizacao
                })
            else:
                eventos_com_erro += 1

        for evento in eventos:
            print(
                f"ID: {evento['id']}, Nome do Evento: {evento['nome']}, Data: {evento['data']}, Localização: {evento['localizacao']}")

    except urllib.error.HTTPError as e:
        logging.error(f"Erro HTTP ao acessar a URL {event_url}: {e}")
    except urllib.error.URLError as e:
        logging.error(f"Erro de rede (URL) ao acessar a URL {event_url}: {e}")
    except Exception as e:
        logging.error(f"Erro geral durante o scraping da URL {event_url}: {e}")

    end_time = time.time()
    tempo_total = end_time - start_time

    generate_report('Dados', eventos_extraidos, eventos_com_erro, tempo_total)

    return eventos


def get_event_metadata(event_url, headers):
    metadados_extraidos = 0
    metadados_com_erro = 0
    start_time = time.time()

    try:
        req = urllib.request.Request(event_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read()

        soup = BeautifulSoup(html, 'html.parser')
        metadados = []
        event_divs = soup.find_all('a', class_='sympla-card')

        for event_id_counter, event in enumerate(event_divs, start=1):
            evento_id = event.get('data-bannerid')
            metadado = event.get('data-creative')

            if evento_id and metadado:
                metadados_extraidos += 1
                metadados.append({
                    'id': event_id_counter,
                    'id_evento': evento_id,
                    'metadado': metadado
                })
            else:
                metadados_com_erro += 1

        for metadata in metadados:
            print(f"ID: {metadata['id']}, Id do Evento: {metadata['id_evento']}, Metadado: {metadata['metadado']}")

    except urllib.error.HTTPError as e:
        logging.error(f"Erro HTTP ao acessar a URL {event_url}: {e}")
    except urllib.error.URLError as e:
        logging.error(f"Erro de rede (URL) ao acessar a URL {event_url}: {e}")
    except Exception as e:
        logging.error(f"Erro geral durante o scraping da URL {event_url}: {e}")

    end_time = time.time()
    tempo_total = end_time - start_time

    generate_report('Metadados', metadados_extraidos, metadados_com_erro, tempo_total)

    return metadados


def generate_report(tipo, eventos_extraidos, eventos_com_erro, tempo_total):
    print("\n--- Relatório Final ---")
    print(f"Tipo de Extração: {tipo}")
    print(f"Total de eventos extraídos: {eventos_extraidos}")
    print(f"Total de eventos com erro: {eventos_com_erro}")
    print(f"Tempo total de execução: {tempo_total:.2f} segundos")

    with open("relatorio_final.txt", "a") as report_file:
        report_file.write(f"Tipo de Extração: {tipo}\n")
        report_file.write(f"Total de eventos extraídos: {eventos_extraidos}\n")
        report_file.write(f"Total de eventos com erro: {eventos_com_erro}\n")
        report_file.write(f"Tempo total de execução: {tempo_total:.2f} segundos\n")
        if eventos_com_erro > 0:
            report_file.write("\nErros encontrados durante o scraping:\n")
            with open("scraping_errors.log", "r") as log_file:
                report_file.write(log_file.read())
        report_file.write("\n--- Fim do Relatório ---\n\n")


def create_tables():
    c.execute('''
    CREATE TABLE IF NOT EXISTS Eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS DadosEventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_evento INTEGER,
        data TEXT NOT NULL,
        localizacao TEXT NOT NULL,
        FOREIGN KEY (id_evento) REFERENCES Eventos(id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Metadados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_evento INTEGER,
        metadado TEXT NOT NULL,
        FOREIGN KEY (id_evento) REFERENCES Eventos(id)
    )
    ''')

    conn.commit()


def insert_data(event_details, event_metadata, event_date_location):
    conn = sqlite3.connect('eventos.db')
    c = conn.cursor()

    try:
        # Inserir dados na tabela Eventos
        for event in event_details:
            nome = event['nome']
            tipo = event['tipo']
            c.execute('''
            INSERT INTO Eventos (nome, tipo) VALUES (?, ?)
            ''', (nome, tipo))
            evento_id = c.lastrowid

        for date_location in event_date_location:
            data = date_location['data']
            localizacao = date_location['localizacao']
            c.execute('''
                INSERT INTO DadosEventos (id_evento, data, localizacao) VALUES (?, ?, ?)
                ''', (evento_id, data, localizacao))

        for metadata in event_metadata:
            metadado = metadata['metadado']
            c.execute('''
                INSERT INTO Metadados (id_evento, metadado) VALUES (?, ?)
                ''', (evento_id, metadado))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def catch_events():
    create_tables()

    URLs = [
        'https://www.sympla.com.br/eventos/gastronomico?c=em-alta&cl=1-gastronomico',
        'https://www.sympla.com.br/eventos/curso-workshop?c=em-alta&cl=8-curso-workshop',
        'https://www.sympla.com.br/eventos/religioso-espiritual?c=em-alta&cl=13-religioso-espiritual'
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }

    for url in URLs:
        print('Link :', url)
        print('Dados do evento: ')
        event_details = get_event_details(url, headers)
        print('Datas do evento: ')
        event_datas = get_event_data(url, headers)
        print('Metadados do evento: ')
        event_metadatas = get_event_metadata(url, headers)

        insert_data(event_details, event_metadatas, event_datas)

if __name__ == "__main__":
    conn = sqlite3.connect('eventos.db')
    c = conn.cursor()
    catch_events()
    print('Bem-vindo ao TP5 - Fundamentos de Dados')
    while True:
        print('''
            1 - Consultar eventos
            2 - Consultar eventos proximos
            3 - Consultar eventos no RJ
            4 - Consultar eventos ao ar livre
            5 - Consultar metadados
        ''')
        response = int(input('Qual consulta que deseja fazer? '))
        match response:
            case (1):
                consulta_1.consultar_eventos(c)
            case (2):
                consulta_2.consultar_eventos_proximos(c)
            case (3):
                consulta_3.consultar_eventos_rio(c)
            case (4):
                consulta_4.consultar_eventos_ao_ar_livre(c)
            case (5):
                consulta_5.consultar_metadados(c)
            case _:
                print('Consulta invalida, selecione uma função valida.')
