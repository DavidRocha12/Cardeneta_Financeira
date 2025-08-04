import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from classe_anotacao import Descricao_Valor
import os
import sys
from PIL import Image, ImageTk # Para redimensionar imagem


class App_Contas:

	def __init__(self, tela):
		self.arquivo_ganho = "Ganhos.txt"
		self.arquivo_gasto = "Gastos.txt"

		pasta_arquivos = os.path.join(os.path.expanduser("~"), "Documents", "AppCardeneta")# Retorna o caminho da pasta do usuário atual, expanduser("~") vai selecionar c:\users\seunome\documento\AppCardeneta
		os.makedirs(pasta_arquivos, exist_ok=True)# aqui vai criar a pasta se caso não existir

		self.caminho_arquivo_ganho = os.path.join(pasta_arquivos, self.arquivo_ganho)# montando caminho para pastas e arquivos em python
		self.caminho_arquivo_gasto = os.path.join(pasta_arquivos, self.arquivo_gasto)

		if not os.path.exists(self.caminho_arquivo_ganho):# vai apenas verificar se existe o arquivo se não vai criar.
			with open(self.caminho_arquivo_ganho, "w", encoding="utf-8") as txt:
				pass

		if not os.path.exists(self.caminho_arquivo_gasto):
			with open(self.caminho_arquivo_gasto, "w", encoding="utf-8") as txt_2:
				pass

		self.tela = tela # variável para criar a tela.
		self.tela.title("Cardeneta Financeira")# nomeia o abeçalho da janela
		self.tela.geometry("720x540")# Especifica o tamanho da janela.
		self.tela.configure()# se for necessário modificar algum detalhe da interface, por exemplo cor de fundo ou de letra.

		caminho_imagem = self.caminho_arquivo("foto_fundo.png")
		self.imagem_fundo = Image.open(caminho_imagem)
		ajuste_tela = self.imagem_fundo.resize((720, 540))
		self.mostrar_imagem = ImageTk.PhotoImage(ajuste_tela)

		self.carregando_imagem = tk.Label(self.tela, image=self.mostrar_imagem)
		self.carregando_imagem.place(x=0, y=0, relwidth=1, relheight=1)

		self.tela.bind("<Configure>", self.aumento_tela)

		# Estilo de interface utilizando ttk
		self.interface_moderna = ttk.Style()# chama para personalizar aparência visual dos widgets
		self.interface_moderna.theme_use("clam")# Ativa um dos temas do ttk, esse é um dos temas mais utilizados
		self.interface_moderna.configure("TLabel", background="#F5F5DC", font=("Roboto", 14))# serve para alterar escrita, botões ou campos de entrada, personalisando cores, letras
		self.interface_moderna.configure("TEntry", padding=5)# padding especifica a largura do quadrado da entrada de texto.
		self.interface_moderna.configure("Vermelho.TLabel", foreground="red", font=("Roboto", 14))# Para ter a praticidade de mudar as strings de cor, se estiver usando a função Style, é necessário configurar um Tlabel para cada cor.
		self.interface_moderna.configure("Verde.TLabel", foreground="green", font=("Roboto", 14))
		self.interface_moderna.configure("Azul.TLabel", foreground="blue", font=("Roboto", 14))
		self.interface_moderna.configure("TButton", background="#F5F5DC", font=("Roboto", 12), padding=5)# Adiciona os botões as configurações da interface Stile

		# Utilizando Frame para centralizar os widgets na janela
		centralizando_app = tk.Frame(self.tela, bg="#F5F5DC")
		centralizando_app.pack(pady=15)# Posisiona o frame dentro da janela e pady adiciona pixel de espaçamento vertical, para não ficar colado com outros widgets


		# Nome do Programa:
		ttk.Label(centralizando_app, text="Cardeneta Financeira").grid(row=0, column=1, pady=10)

		# Entrada de dados para receber nomes:
		ttk.Label(centralizando_app, text="Conta:").grid(row=1, column=0, pady=5) # texto para especificar caixa de texto
		self.nome_conta = ttk.Entry(centralizando_app, width=30)#criação da caixa de texto para receber dados de entrada
		self.nome_conta.grid(row=1, column=1, sticky="w", pady=5, padx=5)# especificando linha e coluna e espaçamento entre os widgets.

		# Entrada de dados para receber valores:
		ttk.Label(centralizando_app, text="Valor: R$").grid(row=2, column=0, pady=5)# row - linha, column - coluna, 
		self.valor_conta = ttk.Entry(centralizando_app, width=15) # width - largura
		self.valor_conta.grid(row=2, column=1, padx=5, sticky="w")

		# Criando um frame para o botão:
		botao_frame = tk.Frame(self.tela, bg="#F5F5DC")
		botao_frame.pack(pady=5)

		# Botão para marcar ganhos
		ttk.Button(botao_frame, text="Adicionar Ganhos", command=lambda:self.incluindo_dados(self.caminho_arquivo_ganho, self.saldo_ganho)).grid(row=0, column=0, padx=5)
		ttk.Button(botao_frame, text="Adicionar Gastos", command=lambda:self.incluindo_dados(self.caminho_arquivo_gasto, self.saldo_gasto)).grid(row=0, column=2, padx=5)
		ttk.Button(botao_frame, text="Mostrar Lista Ganhos", command=lambda:self.mostrar_dados(self.caminho_arquivo_ganho)).grid(row=0, column=1, padx=5)
		ttk.Button(botao_frame, text="Mostrar Lista Gastos", command=lambda:self.mostrar_dados(self.caminho_arquivo_gasto)).grid(row=0, column=4, padx=5)

		# Caixa de texto para mostrar listas:
		self.caixa_texto = tk.Text(self.tela, height=10, font=("Consolas", 12), wrap="word", relief="groove")# wrap="word" - quebra por palavra, relief - define o tipo de borda visual para Text, Frame, Label, etc.
		self.caixa_texto.pack(pady=10, padx=10, fill="both", expand=True)# fill-preencher

		# Escrita de valores:
		self.saldo_ganho = ttk.Label(self.tela, text="Valor a Receber: R$ 0.00", style="Verde.TLabel", font=("Roboto", 12, "bold"))# Para chamar a cor configurada é necessário colocar style e o nome dado a cor cadastrada
		self.saldo_ganho.pack(side="left", padx=25, expand=True)

		self.saldo_gasto = ttk.Label(self.tela, text="Valor a Pagar: R$ 0.00", style="Vermelho.TLabel", font=("Roboto", 12, "bold"))
		self.saldo_gasto.pack(side="left", pady=10, expand=True)

		self.saldo_liquido = ttk.Label(self.tela, text=f"Saldo Liquido: R$ 0.00", style="Azul.TLabel", font=("Roboto", 12, "bold"))# mesmo que na função esteja as configurações de cores, é necessário configurar a cor também no TLabe.
		self.saldo_liquido.pack(side="left", padx=25, expand=True)

		# Verificação de arquivos para não ocorrer erros durante a execução:
		if os.path.exists(self.caminho_arquivo_ganho):# verificando se arquivo existe para ler valor
			self.saldo_total(self.caminho_arquivo_ganho, self.saldo_ganho)# mostra o saldo no app.

		if os.path.exists(self.caminho_arquivo_gasto):
			self.saldo_total(self.caminho_arquivo_gasto, self.saldo_gasto)

		if os.path.exists(self.caminho_arquivo_ganho) or os.path.exists(self.caminho_arquivo_gasto):
			self.soma_valores()

	# Adicionando dados de entrada entre app e arquivo
	def incluindo_dados(self, arquivo, saldo):
		nome = self.nome_conta.get()
		try:
			valor = self.valor_conta.get()# é necessário ser chamado dentro da função para ler dados armazenados na memória.
			# se não for chamado aqui dentro os dados irão constar vazios.

			itens = Descricao_Valor(nome, float(valor), arquivo)# chamando classe para ler ou criar o arquivo.
			itens.adicionando_itens()# adicionando itens no arquivo

			self.nome_conta.delete(0, tk.END)# apagando string adicionados na caixa de entrada de dados após clicar o botão.
			self.valor_conta.delete(0, tk.END)

			self.caixa_texto.delete(1.0, tk.END)# apaga strings na caixa de texto a cada item adicionado.
			self.caixa_texto.insert(tk.END, f"{nome:.<50}R$ {float(valor):.2f}\n")# Imprime cada valor adicionado na caixa de texto

			if os.path.exists(self.caminho_arquivo_ganho) or os.path.exists(self.caminho_arquivo_gasto):# verificando se arquivo existe para ler valor
				self.saldo_total(arquivo, saldo)# atualiza o saldo a cada alteração do valor
				self.soma_valores()

		except ValueError:
			self.mensagem_erro("Erro, Digite um valor válido!")
			return# o return interrompe a execução da função neste ponto e não continua executando o restante do código.

	# Função para atualizar saldo no app.
	def saldo_total(self, arquivo, saldo):
		# Essa função foi criada para atualizar e ao abrir o aplicativo visualizar a soma dos valores
		#nome = self.nome_conta.get() 
		#valor = self.valor_conta.get()
		itens = Descricao_Valor("", 0, arquivo)
		itens.itens_lista() # função que faz a leitura do arquivo e guarda tudo em uma lista
		saldo_lista = itens.soma_valor()# função que soma os valores que estão na lista
		if arquivo == self.arquivo_ganho:
			saldo.config(text=f"Valor a Receber: R$ {saldo_lista:.2f}")# atualização do saldo no app
		elif arquivo == self.arquivo_gasto:
			saldo.config(text=f"Valor a Pagar: R$ {saldo_lista:.2f}")
		return saldo_lista # retorno necessário para calcular valores de ganhos e de gastos na função soma_valores.


	def soma_valores(self):
		# soma de valores para mostrar o valor liquido que existe
		ganho = self.saldo_total(self.caminho_arquivo_ganho, self.saldo_ganho)
		gasto = self.saldo_total(self.caminho_arquivo_gasto, self.saldo_gasto)
		valor_liquido = ganho - gasto
		if valor_liquido < 0:
			self.saldo_liquido.config(text=f"Saldo Liquido: R$ {valor_liquido:.2f}", style="Vermelho.TLabel")
		else:
			self.saldo_liquido.config(text=f"Saldo Liquido: R$ {valor_liquido:.2f}", style="Azul.TLabel")
		
	# Função para mostrar dados na caixa de texto:	
	def mostrar_dados(self, arquivo):
		# função para mostrar lista de contas.
		self.caixa_texto.delete(1.0, tk.END)
		itens = Descricao_Valor("", 0, arquivo)
		lista = itens.itens_lista()
		nome_lista = " Lista "
		self. caixa_texto.insert(tk.END, f"{nome_lista:*^70}\n")
		for nome, valor in lista:
			valor = float(valor)
			self.caixa_texto.insert(tk.END, f"{nome:.<58} R$ {valor:.2f}\n")

	# Função que cria uma caixa de erro personalizado:		
	def mensagem_erro(self, msg):
		# Função feito para criar uma tela de mensagem de erro.
		mensagem = tk.Toplevel()
		mensagem.title("Erro")
		mensagem.geometry("400x150")# tamanho personalizado
		mensagem.configure()

		#Carrega e redimenciona a imagem
		imagem_erro = Image.open("alerta.png")#caminho da imagem
		imagem_erro = imagem_erro.resize((50, 50))# redimenciona imagem para deixar do tamanho que deseja
		image_tk = ImageTk.PhotoImage(imagem_erro)

		#Frame para a imagem e texto
		frame_imagem = tk.Frame(mensagem)
		frame_imagem.pack(side="left", padx=60)

		img_label = tk.Label(frame_imagem, image=image_tk)# O Label é criado dentro do frame
		img_label.image = image_tk  # mantém a imagem na memória
		img_label.pack(side="left")# deixa a imagem ao lado esquerdo da tela com o frame


		ttk.Label(frame_imagem, text=msg, font=("Roboto", 12)).pack(pady=15)# Label para a mensagem
		ttk.Button(frame_imagem, text="Fechar", command=mensagem.destroy).pack(pady=15)# Button para fercha o erro


	def aumento_tela(self, event):
		#Essa função foi criada para fazer o redimencionamento da tela, fazendo a imagem se adaptar a ela.
		if event.widget == self.tela:
			imagem = self.imagem_fundo.resize((event.width, event.height))# redimenciona a imagem de fundo ao novo tamanho do widget
			self.mostrar_imagem = ImageTk.PhotoImage(imagem)# converte a imagem para um objeto PhotoImage que é o formato que o Tkinter entende para mostrar imagem.
			self.carregando_imagem.configure(image=self.mostrar_imagem)


	def caminho_arquivo(self, nome_arquivo):
	    if hasattr(sys, '_MEIPASS'):
	        return os.path.join(sys._MEIPASS, nome_arquivo)
	    return os.path.join(os.path.abspath("."), nome_arquivo)

 
tela = tk.Tk()# Criando a janela principal
app = App_Contas(tela)# classe que a interface está construido
tela.mainloop()# .mainloop é necessário para manter o aplicativo aberto
