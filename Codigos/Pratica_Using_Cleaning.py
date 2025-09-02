# importando bibliotecas
import re
import time
import pandas as pd
from collections import defaultdict
from datetime import datetime

# Início
print('hello world')
print('Objetivo é analisar as vendas de sorvete e encotrar o sabor mais vendido')
print('----------'*7,'\n')
time.sleep(3)

# Criando uma lista
sorvetes = pd.read_excel('C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/excel_vendas_sorveteria2.xlsx')
# Chamando o head para ter uma amostra dos dados
print(f"Amostra de dados da sorveteria\n{sorvetes.head()}\n")
print('----------'*7,'\n')
time.sleep(3)
#Definindo o Padrão Regex	
regex = re.compile(
r"(?P<id>\S+)" #ID numperico - explicação: ?P<id>	Cria um grupo. \d+ Um ou mais digitos (0 á 9). \s Um espaço em branco.
r"(?P<codigo>\S+)\s" #Código Numérico - explicação: ?P<codigo> Grupo. \d+ Um ou mais digitos (0 á 9). \s Um espaço em branco.	
r"(?P<data>\d{4}-\d{2}-\d{2})\s" # Data AAAA-MM-DD - Explicação: ?P<data> Grupo. \d{4}-d{2}-\d{2} formato da data, 4 digitos, hífen, 2 dígitos, hífen, 2 digitos, hífen. \s Um espaço em branco.	
r"(?P<sabor>\S+)" # Sabor - Explicação: ?P<sabor> grupo. [\w]+ Um ou mais caracteres de palavras (letras, números, underscore). \s Um espaço em branco.
r"(?P<tamanho>[\w]+)\s" # Tamanho - Explicação: ?P<tamanho> grupo. [\w]+ Um ou mais caracteres de palavras (letras, números, underscore). \s Um espaço em branco.
r"(?P<preco>[\d.]+)\s" # Preço - Explicação: [\d.]+ Um ou mais dígitos ou pontos (para números decimais). \s Um espaço em branco.
r"(?P<pgto>[\w]+)\s" # pgto - Explicação: [\w]+ Um ou mais caracteres de palavras (letras, números, underscore). \s Um espaço em branco.
r"(?P<atendente>\S+)" # Nome da atendente. Igual a de cima.
r"(?P<avaliacao>[\d.]+)" # Avaliação - Explicação: [\d.]+ Um ou mais dígitos ou pontos (números com ponto decimal).
)
print(f"Padrão regex para analisar os dados\n{regex}\n")
print('----------'*7,'\n')
time.sleep(3)
#Definir local para salvar os dados
salvamento = "VendasSorveteriaCompleta.txt"

with open(salvamento,"w", encoding="utf-8") as f:
	for linha in sorvetes:
		f.write(linha + "\n")
print(f"Dados Carregados!\n")
time.sleep(3)
# Iniciando a análise de fato!
VendasSabor = defaultdict(int)

with open(salvamento, "r", encoding="utf-8") as f:
	tit = f.readlines() # Títulos
	for linh in tit[1:]: # Pula a primeira linha dos títulos
		linh = linh.rstrip()
		match = regex.match(linh)
		if match:
			venda = match.groupdict()
			sabor = venda['sabor'].strip()
			
			# contagem para sabor
			VendasSabor[sabor] += 1
		else:
			print(f"erro:{linh}")

# Ordenamos os resultados pela qtd vendida
resultados = sorted(VendasSabor.items(), key=lambda x: x[1], reverse=True)
print(f"Iniciando a análise...\n")
time.sleep(3)
print("Sabores Mais Vendidos (por quantidade):")
for sabor, quantidade in resultados:
	print(f"{sabor}: {quantidade} unidades vendidas")
# Prints




#format_pat= re.compile(
#    r"(?P<host>[\d\.]+)\s"
#    r"(?P<identity>\S*)\s"
#    r"(?P<user>\S*)\s"
#    r"\[(?P<time>.*?)\]\s"
#    r'"(?P<request>.*?)"\s'
#    r"(?P<status>\d+)\s"
#    r"(?P<bytes>\S*)\s"
#    r'"(?P<referer>.*?)"\s'
#    r'"(?P<user_agent>.*?)"\s*'
#)
#print(format_pat,'\n')
#print('Expressão regex para analisar as linhas de log')
#print('----------'*7,'\n')
#time.sleep(5)
#
#logPath = "C:\\Users\\Kawan_BPK\\OneDrive - Biopark Educação\\Área de Trabalho\\LAMIA\\Curso\\Card 10\\Bases\\access_log.txt"
#
#URLCounts = {}
#
#try:
#	with open(logPath,"r") as f:
#		for line in (l.rstrip() for l in f):
#			match = format_pat.match(line)
#			if match:
#				access = match.groupdict()
#				request = access['request']
#				(action, URL, protocol) = request.split()
#				if URLCounts.has_key(URL):
#					URLCounts[URL] = URLCounts[URL] + 1
#				else:
#					URLCounts[URL] = 1
#	
#	results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)
#	
#	for result in results[:20]:
#		print(result + ":" + str(URLCounts[result]))
#	# Aqui temos erro de execução
#except:
#	with open(logPath, "r") as f:
#		for line in (l.rstrip() for l in f):
#			match= format_pat.match(line)
#			if match:
#				access = match.groupdict()
#				request = access['request']
#				fields = request.split()
#				if (len(fields) != 3):
#					print(fields)
#	print("Observamos que temos requisições com campos vazios e um que parece 'lixo'")
#	print('----------'*7)
#time.sleep(5)
#
#URLCounts = {}
#
#with open(logPath, "r") as f:
#	for line in (l.rstrip() for l in f):
#		match= format_pat.match(line)
#		if match:
#			access = match.groupdict()
#			request = access['request']
#			fields = request.split()
#			if (len(fields) == 3):
#				URL = fields[1]
#				if URL in URLCounts:
#					URLCounts[URL] = URLCounts[URL] + 1
#				else:
#					URLCounts[URL] = 1
#
#results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)
#
#for result in results[:20]:
#	print(result + ": " + str(URLCounts[result]))
#
#print("\nAo definirmos as linhas de log = 3, conseguimos ver apenas as requisições válidas e a quantidade de acesso delas, ainda sim encontramos requisições estranhas, como 'xmlrpc.php' com 68494 acessos")
#print('-------------'*7)
#time.sleep(5)
#
#UserAgents = {}
#
#with open(logPath, "r") as f:
#    for line in (l.rstrip() for l in f):
#        match= format_pat.match(line)
#        if match:
#            access = match.groupdict()
#            agent = access['user_agent']
#            if agent in UserAgents:
#                UserAgents[agent] = UserAgents[agent] + 1
#            else:
#                UserAgents[agent] = 1
#
#results = sorted(UserAgents, key=lambda i: int(UserAgents[i]), reverse=True)
#
#for result in results:
#    print(result + ": " + str(UserAgents[result]))
#print('\nAqui filtramos apenas os users agentes e descobrimos vaorios bots acessando o site ')
#print('-------------'*7,'\n')
#time.sleep(5)
#
#URLCounts = {}
#
#with open(logPath, "r") as f:
#    for line in (l.rstrip() for l in f):
#        match= format_pat.match(line)
#        if match:
#            access = match.groupdict()
#            agent = access['user_agent']
#            if (not('bot' in agent or 'spider' in agent or 
#                    'Bot' in agent or 'Spider' in agent or
#                    'W3 Total Cache' in agent or agent =='-')):
#                request = access['request']
#                fields = request.split()
#                if (len(fields) == 3):
#                    (action, URL, protocol) = fields
#                    if (action == 'GET'):
#                        if URL in URLCounts:
#                            URLCounts[URL] = URLCounts[URL] + 1
#                        else:
#                            URLCounts[URL] = 1
#
#results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)
#
#for result in results[:20]:
#    print(result + ": " + str(URLCounts[result]))
#print("Filtramos apenas as requisições 'get'. Aqui descobrimos vários acessos que podemos filtrar")
#print('-------------'*7)
#time.sleep(5)
#
#URLCounts = {}
#
#with open(logPath, "r") as f:
#    for line in (l.rstrip() for l in f):
#        match= format_pat.match(line)
#        if match:
#            access = match.groupdict()
#            agent = access['user_agent']
#            if (not('bot' in agent or 'spider' in agent or 
#                    'Bot' in agent or 'Spider' in agent or
#                    'W3 Total Cache' in agent or agent =='-')):
#                request = access['request']
#                fields = request.split()
#                if (len(fields) == 3):
#                    (action, URL, protocol) = fields
#                    if (URL.endswith("/")):
#                        if (action == 'GET'):
#                            if URL in URLCounts:
#                                URLCounts[URL] = URLCounts[URL] + 1
#                            else:
#                                URLCounts[URL] = 1
#
#results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)
#
#for result in results[:20]:
#    print(result + ": " + str(URLCounts[result]))
#print('Aqui chegamos em um resultado mais satisfatórios dos acessos ao site, mas é importante salietnar que é preciso conehcer os dados que estão sendo analisados para saber como tratar')
#print('-------------'*7)
