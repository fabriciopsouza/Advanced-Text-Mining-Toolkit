# src/analysis.py

import logging
import re
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize
from utils import load_spacy_model
from textstat import flesch_reading_ease, flesch_kincaid_grade
import pyphen
import dateparser
from gensim import corpora, models
from transformers import pipeline

# Lista de conectores em português e inglês
CONNECTORS = {
    'pt': {
        'aditivos': [
            'e', 'além disso', 'também', 'além do mais', 'mais ainda', 'em adição',
            'ademais', 'aliás', 'bem como', 'ainda assim', 'do mesmo modo', 'igualmente',
            'a fim de', 'com efeito', 'com o intuito de', 'assim', 'desta maneira',
            'dessa forma', 'em virtude de', 'ademais', 'aliás', 'mais ainda',
            'ademais', 'aliás', 'a fim de', 'com efeito', 'com o intuito de',
            'de acordo com', 'de fato', 'de modo que', 'devido a', 'diante disso',
            'em contrapartida', 'em decorrência de', 'em face de', 'em outras palavras',
            'em razão de', 'em relação a', 'em síntese', 'em suma', 'em virtude de',
            'especificamente', 'eventualmente', 'exceto', 'principalmente',
            'para que', 'por extensão', 'por exemplo', 'por fim', 'por conseguinte',
            'por exemplo', 'por extensão', 'por fim', 'por conseguinte', 'por exemplo',
            'por extensão', 'por fim', 'por conseguinte'
        ],
        'adversativos': [
            'mas', 'no entanto', 'contudo', 'todavia', 'porém', 'não obstante',
            'embora', 'ao contrário', 'sendo assim', 'sob esse aspecto',
            'ainda que', 'ao contrário', 'ao passo que', 'apesar de',
            'não obstante', 'embora', 'ao contrário', 'sem embargo'
        ],
        'conclusivos': [
            'portanto', 'assim', 'logo', 'consequentemente', 'como resultado',
            'sendo assim', 'em síntese', 'em suma', 'finalmente', 'para que',
            'por conseguinte', 'por fim', 'em conclusão', 'em síntese',
            'em suma', 'sob esse aspecto', 'sendo assim', 'considerando que',
            'consoante', 'dado que', 'em síntese', 'em suma', 'por conseguinte',
            'finalmente', 'haja vista', 'isto é', 'já que', 'logo',
            'sendo assim', 'sem embargo', 'sob esse aspecto', 'subsequentemente',
            'tal como', 'tanto quanto', 'tendo em vista', 'uma vez que',
            'visto que'
        ]
    },
    'en': {
        'addition': [
            'and', 'also', 'in addition', 'furthermore', 'moreover', 'additionally',
            'besides', 'as well as', 'in fact', 'indeed', 'also', 'as well as',
            'moreover', 'furthermore', 'additionally', 'besides', 'as well as',
            'in fact', 'indeed', 'namely', 'specifically', 'for example', 'for instance',
            'such as', 'in particular', 'to illustrate', 'in other words', 'that is', 'i.e.',
            'e.g.', 'also', 'moreover', 'additionally', 'furthermore', 'besides',
            'as well as', 'in fact', 'indeed', 'similarly', 'likewise', 'equally',
            'comparatively', 'in comparison', 'by comparison', 'similarly', 'likewise',
            'equally', 'comparatively', 'in comparison', 'by comparison'
        ],
        'contrast': [
            'but', 'however', 'nevertheless', 'yet', 'nonetheless', 'though',
            'although', 'even though', 'despite', 'in spite of', 'notwithstanding',
            'regardless', 'conversely', 'on the other hand', 'unlike', 'otherwise',
            'whereas', 'while', 'but', 'however', 'nevertheless', 'yet', 'nonetheless',
            'though', 'although', 'even though', 'despite', 'in spite of', 'notwithstanding',
            'regardless', 'conversely', 'on the other hand', 'unlike', 'otherwise',
            'whereas', 'while', 'though', 'although', 'even though'
        ],
        'conclusion': [
            'therefore', 'thus', 'hence', 'consequently', 'so', 'accordingly',
            'as a result', 'consequently', 'so', 'hence', 'thereafter', 'subsequently',
            'thereafter', 'in conclusion', 'to conclude', 'in summary', 'to summarize',
            'in short', 'overall', 'ultimately', 'all in all', 'to sum up', 'in essence',
            'in conclusion', 'to conclude', 'in summary', 'to summarize', 'in short',
            'overall', 'ultimately', 'all in all', 'to sum up', 'in essence'
        ]
    }
}

def is_inappropriate(word):
    """
    Verifica se uma palavra é ofensiva ou inadequada.
    
    Parâmetros:
        word (str): Palavra a ser verificada.
    
    Retorna:
        bool: True se a palavra for inadequada, False caso contrário.
    """
    # Lista de palavras ofensivas ou inadequadas
    inappropriate_words = {'delicia', 'palavra_ofensiva2', 'palavra_ofensiva3'}  # Adicione outras palavras conforme necessário
    return word.lower() in inappropriate_words

def extract_entities(text, language):
    """
    Extrai entidades nomeadas do texto.
    
    Parâmetros:
        text (str): O texto a ser analisado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        list: Lista de tuplas com entidades e seus tipos.
    """
    try:
        logging.info("Iniciando extração de entidades nomeadas.")
        print("Iniciando extração de entidades nomeadas.")
        nlp = load_spacy_model(language)
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        logging.info(f"Entidades extraídas: {entities}")
        print(f"Entidades extraídas: {entities}")
        return entities
    except Exception as e:
        logging.error(f"Erro na extração de entidades: {str(e)}")
        print(f"Erro na extração de entidades: {str(e)}")
        return []

def extract_pos_tags(text, language):
    """
    Extrai POS tags do texto.
    
    Parâmetros:
        text (str): O texto a ser analisado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        list: Lista de tokens com suas respectivas POS tags.
    """
    try:
        logging.info("Iniciando extração de POS tags.")
        print("Iniciando extração de POS tags.")
        nlp = load_spacy_model(language)
        doc = nlp(text)
        pos_tags = [(token.text, token.pos_) for token in doc]
        logging.info(f"POS tags extraídos: {pos_tags[:10]}...")  # Log parcial
        print(f"POS tags extraídos: {pos_tags[:10]}...")  # Print parcial
        return pos_tags
    except Exception as e:
        logging.error(f"Erro na extração de POS tags: {str(e)}")
        print(f"Erro na extração de POS tags: {str(e)}")
        return []

def dependency_parsing(text, language):
    """
    Realiza análise de dependência no texto.
    
    Parâmetros:
        text (str): O texto a ser analisado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        list: Lista de relações de dependência.
    """
    try:
        logging.info("Iniciando análise de dependência.")
        print("Iniciando análise de dependência.")
        nlp = load_spacy_model(language)
        doc = nlp(text)
        dependencies = [(token.text, token.dep_, token.head.text) for token in doc]
        logging.info(f"Relações de dependência extraídas: {dependencies[:10]}...")  # Log parcial
        print(f"Relações de dependência extraídas: {dependencies[:10]}...")  # Print parcial
        return dependencies
    except Exception as e:
        logging.error(f"Erro na análise de dependência: {str(e)}")
        print(f"Erro na análise de dependência: {str(e)}")
        return []

def keyword_extraction(text, language):
    """
    Extrai palavras-chave do texto.
    
    Parâmetros:
        text (str): O texto a ser analisado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        list: Lista de palavras-chave.
    """
    try:
        logging.info("Iniciando extração de palavras-chave.")
        print("Iniciando extração de palavras-chave.")
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(max_features=20, stop_words='english' if language == 'en' else 'portuguese')
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        keywords = sorted(zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True)
        logging.info(f"Palavras-chave extraídas: {keywords}")
        print(f"Palavras-chave extraídas: {keywords}")
        return keywords
    except Exception as e:
        logging.error(f"Erro na extração de palavras-chave: {str(e)}")
        print(f"Erro na extração de palavras-chave: {str(e)}")
        return []

def extract_relationships(text, language):
    """
    Extrai relações semânticas entre entidades.
    
    Parâmetros:
        text (str): O texto a ser analisado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        list: Lista de relações entre entidades.
    """
    try:
        logging.info("Iniciando extração de relações semânticas.")
        print("Iniciando extração de relações semânticas.")
        nlp = load_spacy_model(language)
        doc = nlp(text)
        relationships = []
        for ent in doc.ents:
            for token in ent.root.head.children:
                if token.dep_ in ('prep', 'agent') and token.head == ent.root:
                    for child in token.children:
                        if child.ent_type_:
                            relationships.append((ent.text, token.text, child.text))
        logging.info(f"Relações extraídas: {relationships[:10]}...")  # Log parcial
        print(f"Relações extraídas: {relationships[:10]}...")  # Print parcial
        return relationships
    except Exception as e:
        logging.error(f"Erro na extração de relações semânticas: {str(e)}")
        print(f"Erro na extração de relações semânticas: {str(e)}")
        return []

def lda_topic_modeling(tokens, language, num_topics=5, passes=10):
    """
    Realiza modelagem de tópicos utilizando LDA.
    
    Parâmetros:
        tokens (list): Lista de tokens pré-processados.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
        num_topics (int): Número de tópicos a serem identificados.
        passes (int): Número de passes pelo corpus durante o treinamento.
    
    Retorna:
        list: Lista de tópicos identificados.
    """
    try:
        logging.info("Iniciando modelagem de tópicos com LDA.")
        print("Iniciando modelagem de tópicos com LDA.")
        from gensim import corpora, models

        dictionary = corpora.Dictionary([tokens])
        corpus = [dictionary.doc2bow(tokens)]
        lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
        topics = lda_model.print_topics(num_words=5)
        logging.info(f"Tópicos extraídos: {topics}")
        print(f"Tópicos extraídos: {topics}")
        return topics
    except Exception as e:
        logging.error(f"Erro na modelagem de tópicos: {str(e)}")
        print(f"Erro na modelagem de tópicos: {str(e)}")
        return []

def sentiment_analysis(text, language):
    """
    Realiza análise de sentimento no texto.
    
    Parâmetros:
        text (str): O texto a ser analisado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        dict: Resultado da análise de sentimento.
    """
    try:
        logging.info("Iniciando análise de sentimento.")
        print("Iniciando análise de sentimento.")
        if language == 'en':
            sentiment_pipeline = pipeline("sentiment-analysis")
        elif language == 'pt':
            sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
        else:
            logging.warning("Idioma não suportado para análise de sentimento.")
            print("Idioma não suportado para análise de sentimento.")
            return {'label': 'neutral', 'score': 0.0}
        
        sentiment = sentiment_pipeline(text[:512])[0]  # Limitar a 512 tokens para evitar erros
        logging.info(f"Resultado da análise de sentimento: {sentiment}")
        print(f"Resultado da análise de sentimento: {sentiment}")
        return sentiment
    except Exception as e:
        logging.error(f"Erro na análise de sentimento: {str(e)}")
        print(f"Erro na análise de sentimento: {str(e)}")
        return {'label': 'neutral', 'score': 0.0}

def analyze_connectors(text, language):
    """
    Analisa e categoriza os conectores presentes no texto.
    
    Parâmetros:
        text (str): O texto a ser analisado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        dict: Dicionário com a contagem de conectores por categoria.
    """
    try:
        logging.info("Iniciando análise de conectores.")
        print("Iniciando análise de conectores.")
        connectors = CONNECTORS.get(language, {})
        if not connectors:
            logging.warning(f"Lista de conectores não definida para o idioma: {language}.")
            print(f"Lista de conectores não definida para o idioma: {language}.")
            return {}

        # Tokenização simples para identificação de conectores
        tokens = word_tokenize(text.lower(), language='english' if language == 'en' else 'portuguese')
        connector_counts = {category: 0 for category in connectors}

        for category, connector_list in connectors.items():
            for connector in connector_list:
                # Para multi-palavras conectores, precisamos verificar a presença no texto
                if ' ' in connector:
                    # Verifica se a sequência de palavras está presente
                    pattern = re.compile(r'\b' + re.escape(connector) + r'\b')
                    matches = pattern.findall(text.lower())
                    connector_counts[category] += len(matches)
                else:
                    connector_counts[category] += tokens.count(connector.lower())

        logging.info("Análise de conectores concluída com sucesso.")
        print("Análise de conectores concluída com sucesso.")
        return connector_counts
    except Exception as e:
        logging.error(f"Erro na análise de conectores: {str(e)}")
        print(f"Erro na análise de conectores: {str(e)}")
        return {}

def spelling_correction(text, language):
    """
    Corrige erros ortográficos no texto fornecido.
    
    Parâmetros:
        text (str): O texto a ser corrigido.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        dict: Dicionário com palavras incorretas e suas sugestões de correção.
    """
    try:
        logging.info("Iniciando correção ortográfica.")
        print("Iniciando correção ortográfica.")
        spell = SpellChecker(language=language)
        words = word_tokenize(text, language='english' if language == 'en' else 'portuguese')
        
        # Lista de stopwords e palavras a serem ignoradas
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english')) if language == 'en' else set(stopwords.words('portuguese'))
        ignore_words = {
            'vibra', 'energia', 'padronização', 'macroprocesso', 'subprocesso', 'norma',
            'procedimento', 'padronizacao', 'gerência', 'diretoria', 'conselho',
            'administração', 'ti', 'digital', 'usuário', 'facilitador', 'suporte',
            'documento'
        }
        
        # Identificar palavras com letras maiúsculas (possíveis nomes próprios)
        proper_nouns = {word for word in words if word[0].isupper()}
        # Combinar palavras a serem ignoradas
        ignore_words.update(proper_nouns)
        
        # Filtrar palavras que não estão na lista de ignoradas e são desconhecidas pelo spellchecker
        misspelled = [
            word for word in words
            if word.lower() not in ignore_words
            and word.isalpha()
            and word.lower() not in stop_words
            and word.lower() in spell.unknown([word])
        ]
        
        misspelled = list(set(misspelled))  # Evitar duplicatas

        corrections = {}
        for word in misspelled:
            # Obter sugestões que tenham uma alta similaridade
            suggestions = spell.candidates(word)
            print(f"Sugestões para '{word}': {suggestions}")  # Debug
            
            # Filtrar sugestões que não sejam ofensivas ou inadequadas
            suggestions = [s for s in suggestions if not is_inappropriate(s)]
            
            # Ordenar sugestões por frequência (mais frequente primeiro)
            suggestions = sorted(suggestions, key=lambda x: spell.word_frequency.frequency(x), reverse=True)
            print(f"Sugestões ordenadas para '{word}': {suggestions}")  # Debug
            
            if suggestions:
                corrections[word] = suggestions[:3]  # Limitar a 3 sugestões
            else:
                corrections[word] = []
        
        logging.info("Correção ortográfica concluída com sucesso.")
        print("Correção ortográfica concluída com sucesso.")
        return corrections
    except Exception as e:
        logging.error(f"Erro na correção ortográfica: {str(e)}")
        print(f"Erro na correção ortográfica: {str(e)}")
        return {}

def readability_scores(text, language):
    """
    Calcula os índices de legibilidade Flesch Reading Ease e Flesch-Kincaid Grade para inglês
    e o Índice de Legibilidade Ajustado para português.
    
    Parâmetros:
        text (str): O texto a ser analisado.
        language (str): O idioma do texto ('en' para inglês, 'pt' para português).
    
    Retorna:
        dict: Contendo os índices de legibilidade calculados.
    """
    try:
        logging.info("Calculando índices de legibilidade.")
        print("Calculando índices de legibilidade.")
        if not text.strip():
            logging.info("Texto vazio fornecido. Retornando índices zerados.")
            print("Texto vazio fornecido. Retornando índices zerados.")
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'fernandez_huerta_adjusted': 0
            }
        
        if language == 'en':
            fre = flesch_reading_ease(text)
            fkg = flesch_kincaid_grade(text)
            logging.info(f"Flesch Reading Ease: {fre}")
            logging.info(f"Flesch-Kincaid Grade: {fkg}")
            print(f"Flesch Reading Ease: {fre} (Quanto maior, mais fácil de ler)")
            print(f"Flesch-Kincaid Grade: {fkg} (Indica o nível escolar necessário)")
            return {
                'flesch_reading_ease': fre,
                'flesch_kincaid_grade': fkg,
                'fernandez_huerta_adjusted': 0  # Não aplicável
            }
        elif language == 'pt':
            stats = text_statistics(text)
            total_words = stats.get('total_words', 0)
            total_sentences = stats.get('total_sentences', 0)
            syllables = count_syllables_pt(text)
            
            if total_sentences == 0 or total_words == 0:
                fernandez_huerta_adjusted = 0
            else:
                # Fórmula Ajustada para Legibilidade em Português:
                # Índice de Legibilidade Ajustado = 207 - 1.015*(Palavras/Sentenças) - 84.6*(Sílabas/Palavras)
                fernandez_huerta_adjusted = 207 - (1.015 * (total_words / total_sentences)) - (84.6 * (syllables / total_words))
            
            logging.info(f"Índice de Legibilidade Ajustado: {fernandez_huerta_adjusted}")
            print(f"Índice de Legibilidade Ajustado: {fernandez_huerta_adjusted:.2f} (Quanto maior, mais fácil de ler)")
            return {
                'flesch_reading_ease': 0,  # Não aplicável
                'flesch_kincaid_grade': 0,  # Não aplicável
                'fernandez_huerta_adjusted': fernandez_huerta_adjusted
            }
        else:
            logging.warning("Idioma não suportado para análise de legibilidade.")
            print("Idioma não suportado para análise de legibilidade.")
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'fernandez_huerta_adjusted': 0
            }

    except Exception as e:
        logging.error(f"Erro ao calcular índices de legibilidade: {str(e)}")
        print(f"Erro ao calcular índices de legibilidade: {str(e)}")
        return {
            'flesch_reading_ease': 0,
            'flesch_kincaid_grade': 0,
            'fernandez_huerta_adjusted': 0
        }
