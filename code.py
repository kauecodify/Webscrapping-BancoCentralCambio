# -*- coding: utf-8 -*-
"""
Webscrabbing - ML 
Aplicativo de Cotações com:
- Sistema de login (admin/1234)
- Consulta de dólar e euro via API do BC
- Salvamento em TXT e CSV
"""

import tkinter as tk
from tkinter import ttk, messagebox
from urllib.request import urlopen
import json
from datetime import datetime, timedelta
import csv
import os
import platform
import subprocess
import base64
from PIL import ImageTk, Image
import io

# ------------------------------------------------------------------------------

USUARIO_VALIDO = "admin"
SENHA_VALIDA = "1234"

LOGO_BCB_BASE64 = "bcb.png"

# ------------------------------------------------------------------------------
# Tela de Login
class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistema de Cotações")
        self.root.geometry("400x300")
        self.root.configure(bg="#e6f2ff")
        
        self.carregar_imagem()
        
        self.usuario = tk.StringVar()
        self.senha = tk.StringVar()
        
        self.criar_interface()

# ------------------------------------------------------------------------------

    def carregar_imagem(self):

        try:
            img_data = base64.b64decode(LOGO_BCB_BASE64)
            img = Image.open(io.BytesIO(img_data))
            self.logo_img = ImageTk.PhotoImage(img.resize((150, 150)))
        except:
            self.logo_img = None

# ------------------------------------------------------------------------------

    def criar_interface(self):
        
        """interface de login"""
        main_frame = tk.Frame(self.root, bg="#e6f2ff", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        if self.logo_img:
            logo_label = tk.Label(main_frame, image=self.logo_img, bg="#e6f2ff")
            logo_label.pack(pady=10)
        
        tk.Label(main_frame, text="Sistema de Cotações BCB", 
                font=('Arial', 14, 'bold'), bg="#e6f2ff").pack(pady=10)
        
        login_frame = tk.Frame(main_frame, bg="#e6f2ff")
        login_frame.pack(pady=10)
        
        tk.Label(login_frame, text="Usuário:", bg="#e6f2ff").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Entry(login_frame, textvariable=self.usuario).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="Senha:", bg="#e6f2ff").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Entry(login_frame, textvariable=self.senha, show="*").grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(main_frame, text="Entrar", command=self.verificar_login, 
                bg="#4d94ff", fg="white", width=15).pack(pady=15)

# ------------------------------------------------------------------------------

    def verificar_login(self):
        
        """credenciais do usuário"""
        usuario = self.usuario.get()
        senha = self.senha.get()
        
        if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
            self.root.destroy()
            root = tk.Tk()
            app = AplicativoCotacoes(root)
            root.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

# ------------------------------------------------------------------------------
# Aplicativo Principal
class AplicativoCotacoes:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cotações - BCB")
        self.root.geometry("600x500")
        self.root.configure(bg="#e6f2ff")
        
        # (opacidade)
        try:
            self.root.attributes('-alpha', 0.70)
        except:
            pass
        
        # Variáveis
        self.moeda_selecionada = tk.StringVar(value="dolar")
        self.ultima_atualizacao = tk.StringVar(value="Nunca")
        self.valor_atual = tk.StringVar(value="R$ 0,0000")
        self.valor_anterior = tk.StringVar(value="R$ 0,0000")
        self.variacao = tk.StringVar(value="0,00%")
        self.data_fechamento = tk.StringVar(value="00/00/0000")
        self.data_anterior = tk.StringVar(value="00/00/0000")
        
        # IDs das séries no BCB
        self.series_bcb = {
            "dolar": 10813,  # Dólar comercial
            "euro": 21619    # Euro comercial
        }
        
        self.carregar_imagem()
        
        self.criar_interface()
        
        self.atualizar_dados()

# ------------------------------------------------------------------------------

    def carregar_imagem(self):

        try:
            img_data = base64.b64decode(LOGO_BCB_BASE64)
            img = Image.open(io.BytesIO(img_data))
            self.logo_img = ImageTk.PhotoImage(img.resize((100, 100)))
        except:
            self.logo_img = None

# ------------------------------------------------------------------------------

    def criar_interface(self):
        
        """Cria a interface gráfica principal"""
        main_frame = tk.Frame(self.root, bg="#e6f2ff", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho com logo
        header_frame = tk.Frame(main_frame, bg="#e6f2ff")
        header_frame.pack(fill=tk.X, pady=10)
        
        if self.logo_img:
            logo_label = tk.Label(header_frame, image=self.logo_img, bg="#e6f2ff")
            logo_label.pack(side=tk.LEFT, padx=10)
        
        title_frame = tk.Frame(header_frame, bg="#e6f2ff")
        title_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(title_frame, text="Sistema de Cotações BCB", 
                font=('Arial', 16, 'bold'), bg="#e6f2ff").pack()
        
        # Seletor de moeda
        moeda_frame = tk.Frame(main_frame, bg="#e6f2ff")
        moeda_frame.pack(pady=10)
        
        tk.Label(moeda_frame, text="Moeda:", bg="#e6f2ff").pack(side=tk.LEFT, padx=5)
        
        moeda_options = [("Dólar Comercial", "dolar"), ("Euro Comercial", "euro")]
        for text, mode in moeda_options:
            tk.Radiobutton(moeda_frame, text=text, variable=self.moeda_selecionada, 
                          value=mode, bg="#e6f2ff", command=self.atualizar_dados).pack(side=tk.LEFT, padx=5)
        
        # Informações da cotação
        info_frame = tk.Frame(main_frame, bg="#e6f2ff", padx=10, pady=10)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Atual
        tk.Label(info_frame, text="Último Fechamento:", font=('Arial', 10), bg="#e6f2ff").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Label(info_frame, textvariable=self.data_fechamento, font=('Arial', 10), bg="#e6f2ff").grid(row=0, column=1, sticky=tk.W)
        
        tk.Label(info_frame, text="Valor Atual:", font=('Arial', 10, 'bold'), bg="#e6f2ff").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Label(info_frame, textvariable=self.valor_atual, font=('Arial', 12, 'bold'), bg="#e6f2ff").grid(row=1, column=1, sticky=tk.W)
        
        # Anterior
        tk.Label(info_frame, text="Fechamento Anterior:", font=('Arial', 10), bg="#e6f2ff").grid(row=2, column=0, sticky=tk.W, pady=5)
        tk.Label(info_frame, textvariable=self.data_anterior, font=('Arial', 10), bg="#e6f2ff").grid(row=2, column=1, sticky=tk.W)
        
        tk.Label(info_frame, text="Valor Anterior:", font=('Arial', 10), bg="#e6f2ff").grid(row=3, column=0, sticky=tk.W, pady=5)
        tk.Label(info_frame, textvariable=self.valor_anterior, font=('Arial', 10), bg="#e6f2ff").grid(row=3, column=1, sticky=tk.W)
        
        # Variação
        tk.Label(info_frame, text="Variação:", font=('Arial', 10), bg="#e6f2ff").grid(row=4, column=0, sticky=tk.W, pady=5)
        tk.Label(info_frame, textvariable=self.variacao, font=('Arial', 10), bg="#e6f2ff").grid(row=4, column=1, sticky=tk.W)
        
        # Última atualização
        tk.Label(info_frame, text="Última Atualização:", font=('Arial', 9), bg="#e6f2ff").grid(row=5, column=0, sticky=tk.W, pady=10)
        tk.Label(info_frame, textvariable=self.ultima_atualizacao, font=('Arial', 9), bg="#e6f2ff").grid(row=5, column=1, sticky=tk.W)
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg="#e6f2ff")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Atualizar Dados", command=self.atualizar_dados, 
                 bg="#4d94ff", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Salvar em TXT", command=self.salvar_txt, 
                 bg="#4d94ff", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Salvar em CSV", command=self.salvar_csv, 
                 bg="#4d94ff", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar()
        tk.Label(main_frame, textvariable=self.status_var, fg="blue", bg="#e6f2ff").pack()

# ------------------------------------------------------------------------------

    def obter_dados_api(self, moeda):
        
        """Obtém os dados da API do Banco Central para a moeda selecionada"""
        serie_id = self.series_bcb.get(moeda, 10813)  # Default para dólar
        
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_id}/dados/ultimos/10?formato=json"
        
        try:
            with urlopen(url) as response:
                dados = json.loads(response.read().decode('utf-8'))
            
            # Ordenar por data (mais recente primeiro)
            dados_ordenados = sorted(dados, key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'), reverse=True)
            
            # Pegar os dois últimos dias úteis
            if len(dados_ordenados) >= 2:
                return {
                    'atual': dados_ordenados[0],
                    'anterior': dados_ordenados[1]
                }
            elif len(dados_ordenados) == 1:
                return {
                    'atual': dados_ordenados[0],
                    'anterior': None
                }
            else:
                return None
                
        except Exception as e:
            self.status_var.set(f"Erro ao acessar API: {e}")
            return None

# ------------------------------------------------------------------------------

    def calcular_variacao(self, atual, anterior):
        
        """Calcula a variação percentual"""
        if not anterior or atual == 0:
            return "0,00%"
        
        variacao = ((atual - anterior) / anterior) * 100
        return f"{variacao:.2f}%".replace('.', ',')

# ------------------------------------------------------------------------------

    def atualizar_dados(self):
        
        """Atualiza os dados na interface"""
        moeda = self.moeda_selecionada.get()
        self.status_var.set(f"Atualizando dados do {'dólar' if moeda == 'dolar' else 'euro'}...")
        self.root.update()
        
        dados = self.obter_dados_api(moeda)
        
        if dados and dados['atual']:
            # Formatar valores
            valor_atual = float(dados['atual']['valor'])
            valor_formatado = f"R$ {valor_atual:,.4f}".replace('.', '|').replace(',', '.').replace('|', ',')
            
            self.data_fechamento.set(dados['atual']['data'])
            self.valor_atual.set(valor_formatado)
            
            if dados['anterior']:
                valor_anterior = float(dados['anterior']['valor'])
                valor_anterior_formatado = f"R$ {valor_anterior:,.4f}".replace('.', '|').replace(',', '.').replace('|', ',')
                
                self.data_anterior.set(dados['anterior']['data'])
                self.valor_anterior.set(valor_anterior_formatado)
                self.variacao.set(self.calcular_variacao(valor_atual, valor_anterior))
            
            self.ultima_atualizacao.set(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.status_var.set(f"Dados do {'dólar' if moeda == 'dolar' else 'euro'} atualizados!")
        else:
            self.status_var.set(f"Não foi possível obter os dados do {'dólar' if moeda == 'dolar' else 'euro'}")
            messagebox.showerror("Erro", f"Não foi possível obter os dados do {'dólar' if moeda == 'dolar' else 'euro'}")

# ------------------------------------------------------------------------------

    def salvar_txt(self):
        
        """Salva os dados em um arquivo TXT e exibe o arquivo"""
        moeda = self.moeda_selecionada.get()
        if not self.data_fechamento.get() or self.data_fechamento.get() == "00/00/0000":
            messagebox.showwarning("Aviso", "Nenhum dado disponível para salvar")
            return
        
        try:
            arquivo_txt = f"cotacao_{'dolar' if moeda == 'dolar' else 'euro'}.txt"
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            with open(arquivo_txt, 'w', encoding='utf-8') as f:
                f.write(f"=== COTAÇÃO DO {'DÓLAR' if moeda == 'dolar' else 'EURO'} ===\n\n")
                f.write(f"Data da Consulta: {data_hora}\n")
                f.write(f"Último Fechamento: {self.data_fechamento.get()}\n")
                f.write(f"Valor: {self.valor_atual.get()}\n\n")
                
                f.write("=== COMPARAÇÃO ===\n")
                f.write(f"Fechamento Anterior: {self.data_anterior.get()}\n")
                f.write(f"Valor Anterior: {self.valor_anterior.get()}\n")
                f.write(f"Variação: {self.variacao.get()}\n")
            
            self.status_var.set(f"Dados salvos em {arquivo_txt}")
            self.exibir_arquivo(arquivo_txt)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar arquivo TXT: {e}")
            
# ------------------------------------------------------------------------------

    def salvar_csv(self):
        

        """Salva os dados em um arquivo CSV e exibe o arquivo"""
        moeda = self.moeda_selecionada.get()
        if not self.data_fechamento.get() or self.data_fechamento.get() == "00/00/0000":
            messagebox.showwarning("Aviso", "Nenhum dado disponível para salvar")
            return
        
        try:
            arquivo_csv = f"cotacao_{'dolar' if moeda == 'dolar' else 'euro'}.csv"
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # Verificar se o arquivo já existe para adicionar cabeçalho
            cabecalho = not os.path.exists(arquivo_csv)
            
            with open(arquivo_csv, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                
                if cabecalho:
                    writer.writerow([
                        'Data Consulta', 'Moeda', 'Data Fechamento', 'Valor (R$)', 
                        'Data Anterior', 'Valor Anterior (R$)', 'Variação (%)'
                    ])
                
                writer.writerow([
                    data_hora, 
                    'Dólar' if moeda == 'dolar' else 'Euro',
                    self.data_fechamento.get(), 
                    self.valor_atual.get(),
                    self.data_anterior.get(), 
                    self.valor_anterior.get(), 
                    self.variacao.get()
                ])
            
            self.status_var.set(f"Dados salvos em {arquivo_csv}")
            self.exibir_arquivo(arquivo_csv)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar arquivo CSV: {e}")
    
# ------------------------------------------------------------------------------
    
    def exibir_arquivo(self, caminho_arquivo):
        
        
        """Abre o arquivo no visualizador padrão do sistema"""
        try:
            if platform.system() == 'Windows':
                os.startfile(caminho_arquivo)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', caminho_arquivo])
            else:  # Linux
                subprocess.run(['xdg-open', caminho_arquivo])
        except Exception as e:
            messagebox.showinfo("Arquivo Salvo", f"Arquivo salvo em: {os.path.abspath(caminho_arquivo)}")

# ------------------------------------------------------------------------------
# Inicialização do aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    login = TelaLogin(root)
    root.mainloop()