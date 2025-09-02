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
time.sleep(1)

# Criando uma lista
sorvetes = pd.read_excel('C:/Users/Kawan_BPK/OneDrive - Biopark Educação/Área de Trabalho/LAMIA/Curso/Card 10/Bases/excel_vendas_sorveteria2.xlsx')
sorvetes['Tamanho'] = sorvetes['Tamanho'].str.upper()
# Chamando o head para ter uma amostra dos dados
print(f"Amostra de dados da sorveteria\n{sorvetes.head()}\n")
print('----------'*7,'\n')
time.sleep(3)
#Definindo o Padrão Regex	

regex = re.compile(
    r"^\s*"
    r"(?P<id>\d+)\s"                	#ID numperico - explicação: ?P<id>	Cria um grupo. \d+ Um ou mais digitos (0 á 9). \s Um espaço em branco.
    r"(?P<data>\d{4}-\d{2}-\d{2})\s+" # Data AAAA-MM-DD - Explicação: ?P<data> Grupo. \d{4}-d{2}-\d{2} formato da data, 4 digitos, hífen, 2 dígitos, hífen, 2 digitos, hífen. \s Um espaço em branco.
    r"(?P<sabor>\S+)\s+"             # sabor: sequência sem espaços (ajuste se puder ter espaço)
    r"(?P<tamanho>\w+)\s+"           # tamanho: caracteres de palavra
    r"(?P<preco>\d+(?:[.,]\d+)?)\s+" # preco: inteiro ou decimal com . ou ,
    r"(?P<pgto>\w+)\s+"              # pgto: palavra (mude para \S+ se houver hífen etc.)
    r"(?P<atendente>\S+)\s+"         # atendente: sem espaços (se tiver espaços, ver seção 4)
    r"(?P<avaliacao>\d+(?:[.,]\d+)?)"# avaliacao: número/decimal
    r"\s*$"
)

#r"(?P<sabor>\S+)" # Sabor - Explicação: ?P<sabor> grupo. [\w]+ Um ou mais caracteres de palavras (letras, números, underscore). \s Um espaço em branco.
#)
print(f"Padrão regex para analisar os dados\n{regex}\n")
print('----------'*7,'\n')
time.sleep(1)
#Definir local para salvar os dados
salvamento = "VendasSorveteriaCompleta.txt"

with open(salvamento, "w", encoding="utf-8") as f:
    f.write("id data sabor tamanho preco pgto atendente avaliacao\n")  # cabeçalho p/ pular tit[0]
    for _, row in sorvetes.iterrows():
        id_ = str(row.get("Id", "")).strip()
        data_iso = pd.to_datetime((row.get("Data", "")), dayfirst=True, errors="coerce").strftime("%Y-%m-%d")
        sabor = str(row.get("Sabor", "")).strip()
        tamanho = str(row.get("Tamanho", "")).strip()
        pgto = str(row.get("Pgto", "")).strip()
        atendente = str(row.get("Atendente", "")).strip()

        preco_raw = str(row.get("Preço", row.get("Preco", "")))
        preco = "".join(ch for ch in preco_raw.replace("R$", "").replace(",", ".") if ch.isdigit() or ch == ".")
        avaliacao = str(row.get("Avaliação", row.get("Avaliacao", ""))).strip()

        linha = f"{id_} {data_iso} {sabor} {tamanho} {preco} {pgto} {atendente} {avaliacao}"
        f.write(linha + "\n")
print(f"Dados Carregados!\n")
time.sleep(1)
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

VendasTamanho = defaultdict(int)

with open(salvamento, "r", encoding="utf-8") as f:
	tit = f.readlines() # Títulos
	for linh in tit[1:]: # Pula a primeira linha dos títulos
		linh = linh.rstrip()
		match = regex.match(linh)
		if match:
			venda = match.groupdict()
			tamanho = venda['tamanho'].strip()
			
			# contagem para tamanho
			VendasTamanho[tamanho] += 1
		else:
			print(f"erro:{linh}")



# Ordenamos os resultados pela qtd vendida
resultadosSabor = sorted(VendasSabor.items(), key=lambda x: x[1], reverse=True)
resultadosTamanho = sorted(VendasTamanho.items(), key=lambda x: x[1], reverse=True)
print(f"Iniciando a análise...\n")
time.sleep(1)
def SaboresVendidos():
	print("Sabores Mais Vendidos (por quantidade):")
	for sabor, quantidade in resultadosSabor:
		print(f"{sabor}: {quantidade} unidades vendidas")
	print("============"*10)

def TamanhosVendidos():
	print("Tamanhos Mais Vendidos (por quantidade):")
	for tamanho, quantidade in resultadosTamanho:
		print(f"{tamanho}: {quantidade} unidades vendidas")
	print("============"*10)


SaboresVendidos()
TamanhosVendidos()




