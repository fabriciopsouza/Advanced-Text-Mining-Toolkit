# src/gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import os

class TextMiningGUI:

    def __init__(self, master):
        self.master = master
        master.title("Advanced Text Mining Toolkit")

        self.input_file = None
        self.output_folder = None

        # Botão para selecionar arquivo de entrada
        self.select_input_button = tk.Button(master, text="Selecionar Arquivo de Entrada", command=self.select_input_file)
        self.select_input_button.pack(pady=10)

        # Botão para selecionar pasta de saída
        self.select_output_button = tk.Button(master, text="Selecionar Pasta de Saída", command=self.select_output_folder)
        self.select_output_button.pack(pady=10)

        # Botão para iniciar a análise
        self.start_button = tk.Button(master, text="Iniciar Análise", command=self.start_analysis)
        self.start_button.pack(pady=20)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(
            title="Selecionar Arquivo",
            filetypes=[
                ("Todos os arquivos", "*.*"),
                ("Arquivos de Texto", "*.txt"),
                ("Documentos do Word", "*.docx"),
                ("PDFs", "*.pdf"),
                ("Excel", "*.xlsx *.xls"),
                ("CSV", "*.csv"),
                ("PowerPoint", "*.pptx"),
                ("HTML", "*.html *.htm")
            ]
        )
        if self.input_file:
            print(f"Arquivo de entrada selecionado: {self.input_file}")
            logging.info(f"Arquivo de entrada selecionado: {self.input_file}")

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory(title="Selecionar Pasta de Saída")
        if self.output_folder:
            print(f"Pasta de saída selecionada: {self.output_folder}")
            logging.info(f"Pasta de saída selecionada: {self.output_folder}")

    def start_analysis(self):
        if not self.input_file or not self.output_folder:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo de entrada e uma pasta de saída.")
            return
        # Fecha a janela GUI e retorna os caminhos selecionados
        self.master.quit()
