# Advanced Text Mining Toolkit

## Descrição

O **Advanced Text Mining Toolkit** é uma ferramenta abrangente para análise avançada de textos. Ele inclui funcionalidades de pré-processamento, análise de entidades, extração de palavras-chave, modelagem de tópicos, análise de sentimento, e muito mais. O toolkit também gera visualizações intuitivas e relatórios detalhados no formato ABNT.

## Funcionalidades

- Pré-processamento de texto (tokenização, remoção de stopwords, lematização)
- Extração de entidades nomeadas
- Extração de palavras-chave
- Modelagem de tópicos com LDA
- Análise de sentimento
- Verificação de concordância verbal
- Detecção de mudanças de pessoa gramatical
- Geração de visualizações (word cloud, rede de entidades, fluxo de ações)
- Armazenamento de resultados em banco de dados SQLite
- Geração de relatórios no formato ABNT

## Estrutura do Projeto

Advanced-Text-Mining-Toolkit/ 
│ ├── data/ 
│ ├── input/ # Arquivos de entrada 
│ ├── output/ # Resultados e logs 
│ └── test_files/ # Arquivos de teste 
│ ├── src/ 
│ ├── init.py 
│ ├── main.py # Script principal 
│ ├── preprocessing.py # Funções de pré-processamento 
│ ├── analysis.py # Funções de análise 
│ ├── visualization.py # Funções de visualização 
│ ├── database.py # Funções de armazenamento em banco de dados 
│ ├── gui.py # Interface gráfica 
│ └── utils.py # Funções utilitárias 
│ ├── tests/ 
│ ├── init.py │ 
├── test_preprocessing.py 
│ ├── test_analysis.py 
│ ├── test_visualization.py 
│ ├── test_database.py 
│ └── test_gui.py 
│ ├── requirements.txt # Lista de dependências 
├── README.md # Documentação do projeto 
└── .gitignore # Arquivos e pastas a serem ignorados pelo Git


## Configuração e Execução

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/Advanced-Text-Mining-Toolkit.git
cd Advanced-Text-Mining-Toolkit

### 2. Configure o Ambiente Virtual

python -m venv env
.\env\Scripts\Activate.ps1

### 3. Instale as Dependências

pip install -r requirements.txt

### 4. Execute o Projeto

python src/main.py

### 5. Testes

Para executar os testes internos, execute:
python src/main.py --test

### 6. Contribuição

Sinta-se à vontade para contribuir com este projeto. Abra issues para reportar bugs ou sugerir melhorias e envie pull requests com suas contribuições.

### 7. Licença

Este projeto está licenciado sob a licença MIT.

Salve o arquivo (`Ctrl + S`).

### **3.3. Diretório `src/`**

Vamos criar e configurar todos os arquivos dentro do diretório `src/`.

#### **3.3.1. `src/__init__.py`**

Este arquivo indica que `src/` é um pacote Python. Já foi criado anteriormente como um arquivo vazio. Pode permanecer vazio ou conter comentários.

Abra `src/__init__.py` no VS Code e adicione:

```python
# src/__init__.py

"""
Advanced Text Mining Toolkit - Módulo Principal
"""
