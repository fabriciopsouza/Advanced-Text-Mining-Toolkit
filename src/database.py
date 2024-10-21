# src/database.py

import logging
import sqlite3
import os

def store_data_in_database(analysis_results, output_folder):
    """
    Armazena os resultados da análise em um banco de dados SQLite.
    
    Parâmetros:
        analysis_results (dict): Dicionário com os resultados da análise.
        output_folder (str): Pasta onde o banco de dados será salvo.
    
    Retorna:
        None
    """
    try:
        logging.info("Armazenando dados em banco de dados.")
        print("Armazenando dados em banco de dados.")
        db_path = os.path.join(output_folder, 'analysis_results.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Criação de tabelas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_frequency (
                word TEXT PRIMARY KEY,
                frequency INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity TEXT,
                label TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                responsible TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT,
                details TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connectors (
                category TEXT,
                count INTEGER,
                PRIMARY KEY (category)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readability (
                metric TEXT PRIMARY KEY,
                value REAL
            )
        ''')

        # Inserção dos dados de frequência de palavras
        for word, freq in analysis_results.get('word_frequency', {}).items():
            cursor.execute('''
                INSERT OR REPLACE INTO word_frequency (word, frequency)
                VALUES (?, ?)
            ''', (word, freq))
        
        # Inserção de entidades
        for entity, label in analysis_results.get('entities', []):
            cursor.execute('''
                INSERT INTO entities (entity, label)
                VALUES (?, ?)
            ''', (entity, label))
        
        # Inserção de ações
        for action in analysis_results.get('actions', []):
            cursor.execute('''
                INSERT INTO actions (action, responsible)
                VALUES (?, ?)
            ''', (action['action'], action['responsible']))
        
        # Inserção de erros de concordância
        for error in analysis_results.get('verb_agreement_errors', []):
            cursor.execute('''
                INSERT INTO errors (error_type, details)
                VALUES (?, ?)
            ''', ('Concordância Verbal', f"{error['verb']} com {error['subject']}: {error['error']}"))
        
        # Inserção de conectores
        for category, count in analysis_results.get('connectives', {}).items():
            cursor.execute('''
                INSERT OR REPLACE INTO connectors (category, count)
                VALUES (?, ?)
            ''', (category, count))
        
        # Inserção de legibilidade
        for metric, value in analysis_results.get('readability', {}).items():
            cursor.execute('''
                INSERT OR REPLACE INTO readability (metric, value)
                VALUES (?, ?)
            ''', (metric, value))
        
        # Commit e fechamento da conexão
        conn.commit()
        conn.close()
        logging.info(f"Dados armazenados em {db_path}.")
        print(f"Dados armazenados em {db_path}.")
    except Exception as e:
        logging.error(f"Erro ao armazenar dados em banco de dados: {str(e)}")
        print(f"Erro ao armazenar dados em banco de dados: {str(e)}")
