# src/utils.py

import nltk
import subprocess
import sys
import logging
from importlib import metadata

def download_nltk_packages():
    """
    Baixa os pacotes necessários do NLTK.
    """
    nltk_packages = ['punkt', 'stopwords', 'wordnet', 'vader_lexicon']
    for pkg in nltk_packages:
        try:
            nltk.data.find(f'tokenizers/{pkg}' if pkg == 'punkt' else f'corpora/{pkg}')
        except LookupError:
            print(f"Baixando pacote NLTK: {pkg}")
            nltk.download(pkg)

def load_spacy_model(language):
    """
    Carrega o modelo spaCy correspondente ao idioma. Se não estiver instalado, baixa-o.
    
    Parâmetros:
        language (str): 'en' para inglês, 'pt' para português.
    
    Retorna:
        spacy.lang.*.Language: Modelo spaCy carregado.
    """
    import spacy
    model_name = "pt_core_news_sm" if language == 'pt' else "en_core_web_sm"
    try:
        logging.info(f"Carregando modelo spaCy: {model_name}")
        print(f"Carregando modelo spaCy: {model_name}")
        return spacy.load(model_name)
    except OSError:
        print(f"Baixando o modelo spaCy: {model_name}")
        logging.info(f"Baixando o modelo spaCy: {model_name}")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
        return spacy.load(model_name)
