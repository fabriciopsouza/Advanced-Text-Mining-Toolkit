# src/preprocessing.py

import re
import logging
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from utils import load_spacy_model

def filter_pos_tags(tokens, language):
    """
    Filtra tokens com base em suas classes gramaticais para evitar incluir preposições, artigos, etc.
    
    Parâmetros:
        tokens (list): Lista de tokens.
        language (str): Idioma do texto ('en' ou 'pt').
    
    Retorna:
        list: Lista de tokens filtrados.
    """
    try:
        logging.info("Filtrando tokens com base nas classes gramaticais.")
        print("Filtrando tokens com base nas classes gramaticais.")
        if language == 'en':
            import nltk
            pos_tags = nltk.pos_tag(tokens)
            # Definir quais POS tags incluir (substantivos, verbos, adjetivos, advérbios)
            allowed_tags = {'NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
                            'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'}
        elif language == 'pt':
            nlp = load_spacy_model(language)
            doc = nlp(' '.join(tokens))
            allowed_tags = {'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV'}
            pos_tags = [(token.text, token.pos_) for token in doc]
        else:
            logging.warning("Idioma não suportado para POS tagging.")
            print("Idioma não suportado para POS tagging.")
            return tokens  # Retorna sem filtrar
        
        # Filtrar tokens com base nas tags permitidas
        filtered_tokens = [word for word, pos in pos_tags if pos in allowed_tags]
        logging.info(f"Tokens após filtragem: {filtered_tokens}")
        print(f"Tokens após filtragem: {filtered_tokens}")
        return filtered_tokens
    except Exception as e:
        logging.error(f"Erro ao filtrar POS tags: {str(e)}")
        print(f"Erro ao filtrar POS tags: {str(e)}")
        return tokens

def preprocess_text(text, language):
    """
    Pré-processa o texto fornecido.

    Parâmetros:
        text (str): O texto a ser pré-processado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).

    Retorna:
        list: Lista de tokens pré-processados.
    """
    try:
        logging.info("Iniciando pré-processamento do texto.")
        print("Iniciando pré-processamento do texto.")
        # Seleção de stopwords com base no idioma
        stop_words = set(stopwords.words('english')) if language == 'en' else set(stopwords.words('portuguese'))
        logging.info(f"Stopwords carregadas para o idioma: {language}.")
        print(f"Stopwords carregadas para o idioma: {language}.")

        # Tokenização e conversão para minúsculas
        tokens = word_tokenize(text.lower(), language='english' if language == 'en' else 'portuguese')
        logging.info("Tokenização realizada com sucesso.")
        print("Tokenização realizada com sucesso.")

        # Remoção de caracteres não alfabéticos
        tokens = [re.sub(r'\W+', '', token) for token in tokens]
        logging.info("Remoção de caracteres não alfabéticos concluída.")
        print("Remoção de caracteres não alfabéticos concluída.")

        # Remoção de tokens que não são puramente alfabéticos
        tokens = [token for token in tokens if token.isalpha()]
        logging.info("Filtragem de tokens não alfabéticos concluída.")
        print("Filtragem de tokens não alfabéticos concluída.")

        # Remoção de stopwords
        tokens = [token for token in tokens if token not in stop_words]
        logging.info("Remoção de stopwords concluída.")
        print("Remoção de stopwords concluída.")

        # Filtrar tokens com base nas classes gramaticais
        tokens = filter_pos_tags(tokens, language)

        # Lematização
        if language == 'en':
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(token) for token in tokens]
            logging.info("Lematização para inglês concluída.")
            print("Lematização para inglês concluída.")
        else:
            # Para português, usando spaCy
            nlp = load_spacy_model(language)
            doc = nlp(' '.join(tokens))
            tokens = [token.lemma_ for token in doc]
            logging.info("Lematização para português concluída.")
            print("Lematização para português concluída.")

        logging.info("Pré-processamento do texto finalizado com sucesso.")
        print("Pré-processamento do texto finalizado com sucesso.")
        return tokens
    except Exception as e:
        logging.error(f"Erro no pré-processamento do texto: {str(e)}")
        print(f"Erro no pré-processamento do texto: {str(e)}")
        return []

def text_statistics(text):
    """
    Calcula estatísticas básicas do texto.

    Parâmetros:
        text (str): O texto a ser analisado.

    Retorna:
        dict: Dicionário contendo as estatísticas calculadas.
    """
    try:
        logging.info("Calculando estatísticas do texto.")
        print("Calculando estatísticas do texto.")
        # Contagem total de caracteres
        total_characters = len(text)
        logging.info(f"Total de caracteres: {total_characters}")
        print(f"Total de caracteres: {total_characters}")

        # Tokenização de palavras e sentenças
        all_tokens = word_tokenize(text)
        words = [word for word in all_tokens if word.isalpha()]  # Filtra apenas palavras alfabéticas
        sentences = nltk.sent_tokenize(text)
        paragraphs = [p for p in text.split('\n') if p.strip() != '']

        # Contagem total de palavras
        total_words = len(words)
        logging.info(f"Total de palavras: {total_words}")
        print(f"Total de palavras: {total_words}")

        # Número total de sentenças
        total_sentences = len(sentences)
        logging.info(f"Total de sentenças: {total_sentences}")
        print(f"Total de sentenças: {total_sentences}")

        # Estatísticas de sentenças por parágrafo
        sentences_per_paragraph = [len(nltk.sent_tokenize(p)) for p in paragraphs if p.strip()]
        min_sentences_paragraph = min(sentences_per_paragraph) if sentences_per_paragraph else 0
        max_sentences_paragraph = max(sentences_per_paragraph) if sentences_per_paragraph else 0
        avg_sentences_paragraph = sum(sentences_per_paragraph) / len(sentences_per_paragraph) if sentences_per_paragraph else 0
        logging.info(f"Sentenças por parágrafo: min={min_sentences_paragraph}, max={max_sentences_paragraph}, avg={avg_sentences_paragraph:.2f}")
        print(f"Sentenças por parágrafo: min={min_sentences_paragraph}, max={max_sentences_paragraph}, avg={avg_sentences_paragraph:.2f}")

        # Número de palavras por sentença
        words_per_sentence = [len([word for word in word_tokenize(s) if word.isalpha()]) for s in sentences]
        avg_words_sentence = sum(words_per_sentence) / len(words_per_sentence) if words_per_sentence else 0
        logging.info(f"Média de palavras por sentença: {avg_words_sentence:.2f}")
        print(f"Média de palavras por sentença: {avg_words_sentence:.2f}")

        logging.info("Estatísticas do texto calculadas com sucesso.")
        print("Estatísticas do texto calculadas com sucesso.")
        return {
            'total_characters': total_characters,
            'total_words': total_words,
            'total_sentences': total_sentences,
            'min_sentences_paragraph': min_sentences_paragraph,
            'max_sentences_paragraph': max_sentences_paragraph,
            'avg_sentences_paragraph': avg_sentences_paragraph,
            'avg_words_sentence': avg_words_sentence
        }
    except Exception as e:
        logging.error(f"Erro nas estatísticas de texto: {str(e)}")
        print(f"Erro nas estatísticas de texto: {str(e)}")
        return {}

def count_syllables_pt(text):
    """
    Conta o número de sílabas em um texto em português.

    Parâmetros:
        text (str): O texto a ser analisado.

    Retorna:
        int: Número total de sílabas.
    """
    try:
        logging.info("Contando sílabas no texto em português.")
        print("Contando sílabas no texto em português.")
        import pyphen
        from nltk.tokenize import word_tokenize
        dic = pyphen.Pyphen(lang='pt_BR')
        words = word_tokenize(text, language='portuguese')
        syllables = 0
        for word in words:
            if word.isalpha():
                syllables += len(dic.inserted(word).split('-'))
        logging.info(f"Total de sílabas: {syllables}")
        print(f"Total de sílabas: {syllables}")
        return syllables
    except Exception as e:
        logging.error(f"Erro ao contar sílabas em português: {str(e)}")
        print(f"Erro ao contar sílabas em português: {str(e)}")
        return 0
