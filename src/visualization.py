# src/visualization.py

import logging
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx

def generate_word_cloud(word_freq, output_path):
    """
    Gera uma nuvem de palavras a partir da frequência das palavras e salva como imagem.
    
    Parâmetros:
        word_freq (dict): Dicionário com frequência de palavras.
        output_path (str): Caminho para salvar a imagem da nuvem de palavras.
    """
    try:
        logging.info("Gerando nuvem de palavras.")
        print("Gerando nuvem de palavras.")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        plt.figure(figsize=(15, 7.5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(output_path, format='png')
        plt.close()
        logging.info(f"Nuvem de palavras salva em: {output_path}")
        print(f"Nuvem de palavras salva em: {output_path}")
    except Exception as e:
        logging.error(f"Erro ao gerar nuvem de palavras: {str(e)}")
        print(f"Erro ao gerar nuvem de palavras: {str(e)}")

def generate_entity_network(entities, output_path):
    """
    Gera uma rede de entidades e salva como imagem.
    
    Parâmetros:
        entities (list): Lista de tuplas com entidades e seus tipos.
        output_path (str): Caminho para salvar a imagem da rede de entidades.
    """
    try:
        logging.info("Gerando rede de entidades.")
        print("Gerando rede de entidades.")
        G = nx.Graph()

        for entity, label in entities:
            G.add_node(entity, label=label)
        
        # Adicionar arestas com base na coocorrência no texto (simplificação)
        # Este exemplo conecta todas as entidades entre si
        for i in range(len(entities)):
            for j in range(i+1, len(entities)):
                G.add_edge(entities[i][0], entities[j][0])

        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G, k=0.5)
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_labels(G, pos, labels, font_size=12)
        plt.axis('off')
        plt.savefig(output_path, format='png')
        plt.close()
        logging.info(f"Rede de entidades salva em: {output_path}")
        print(f"Rede de entidades salva em: {output_path}")
    except Exception as e:
        logging.error(f"Erro ao gerar rede de entidades: {str(e)}")
        print(f"Erro ao gerar rede de entidades: {str(e)}")

def generate_dense_pixel_display(text, output_path):
    """
    Gera uma visualização Dense Pixel Display e salva como imagem.
    
    Parâmetros:
        text (str): O texto a ser visualizado.
        output_path (str): Caminho para salvar a imagem da visualização.
    """
    try:
        logging.info("Gerando Dense Pixel Display.")
        print("Gerando Dense Pixel Display.")
        # Implementação futura
        # Placeholder: Salva uma imagem em branco com texto explicativo
        plt.figure(figsize=(10, 10))
        plt.text(0.5, 0.5, 'Dense Pixel Display (Implementação Futura)', horizontalalignment='center', verticalalignment='center')
        plt.axis('off')
        plt.savefig(output_path, format='png')
        plt.close()
        logging.info(f"Dense Pixel Display salva em: {output_path}")
        print(f"Dense Pixel Display salva em: {output_path}")
    except Exception as e:
        logging.error(f"Erro ao gerar Dense Pixel Display: {str(e)}")
        print(f"Erro ao gerar Dense Pixel Display: {str(e)}")

def generate_topic_visualization(topics, output_path):
    """
    Gera uma visualização de tópicos e salva como imagem.
    
    Parâmetros:
        topics (list): Lista de tópicos identificados.
        output_path (str): Caminho para salvar a imagem da visualização de tópicos.
    """
    try:
        logging.info("Gerando visualização de tópicos.")
        print("Gerando visualização de tópicos.")
        from wordcloud import WordCloud

        # Criação de word clouds para cada tópico
        for idx, topic in enumerate(topics):
            plt.figure(figsize=(8, 6))
            topic_words = dict(re.findall(r'"(.*?)"\s*\+\s*[\d\.]+', topic[1]))
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(topic_words)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Tópico {idx+1}')
            plt.savefig(f"{output_path[:-4]}_topic_{idx+1}.png", format='png')
            plt.close()
            logging.info(f"Visualização do tópico {idx+1} salva em: {output_path[:-4]}_topic_{idx+1}.png")
            print(f"Visualização do tópico {idx+1} salva em: {output_path[:-4]}_topic_{idx+1}.png")
    except Exception as e:
        logging.error(f"Erro ao gerar visualização de tópicos: {str(e)}")
        print(f"Erro ao gerar visualização de tópicos: {str(e)}")

def generate_action_flow(actions, output_path):
    """
    Gera uma visualização do fluxo de ações e salva como imagem.
    
    Parâmetros:
        actions (list): Lista de ações mapeadas.
        output_path (str): Caminho para salvar a imagem da visualização de ações.
    """
    try:
        logging.info("Gerando visualização de fluxo de ações.")
        print("Gerando visualização de fluxo de ações.")
        import networkx as nx

        G = nx.DiGraph()

        for action in actions:
            G.add_node(action['action'], type='action')
            G.add_node(action['responsible'], type='responsible')
            G.add_edge(action['responsible'], action['action'])

        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G, k=0.5)
        action_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == 'action']
        responsible_nodes = [node for node, attr in G.nodes(data=True) if attr['type'] == 'responsible']

        nx.draw_networkx_nodes(G, pos, nodelist=responsible_nodes, node_color='lightgreen', node_size=700, label='Responsáveis')
        nx.draw_networkx_nodes(G, pos, nodelist=action_nodes, node_color='lightblue', node_size=700, label='Ações')
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=12)
        plt.legend(scatterpoints=1)
        plt.axis('off')
        plt.savefig(output_path, format='png')
        plt.close()
        logging.info(f"Fluxo de ações salva em: {output_path}")
        print(f"Fluxo de ações salva em: {output_path}")
    except Exception as e:
        logging.error(f"Erro ao gerar visualização de fluxo de ações: {str(e)}")
        print(f"Erro ao gerar visualização de fluxo de ações: {str(e)}")
