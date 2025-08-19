# importando bibliotecas
import re
import time

print('hello world')
print('Objetivo é analisar um log de acesso do Apache para descobrir as páginas mais visualizadas em um site')
print('----------'*7,'\n')
time.sleep(5)

format_pat= re.compile(
    r"(?P<host>[\d\.]+)\s"
    r"(?P<identity>\S*)\s"
    r"(?P<user>\S*)\s"
    r"\[(?P<time>.*?)\]\s"
    r'"(?P<request>.*?)"\s'
    r"(?P<status>\d+)\s"
    r"(?P<bytes>\S*)\s"
    r'"(?P<referer>.*?)"\s'
    r'"(?P<user_agent>.*?)"\s*'
)
print(format_pat,'\n')
print('Expressão regex para analisar as linhas de log')
print('----------'*7,'\n')
time.sleep(5)

logPath = "C:\\Users\\Kawan_BPK\\OneDrive - Biopark Educação\\Área de Trabalho\\LAMIA\\Curso\\Card 10\\Bases\\access_log.txt"

URLCounts = {}

try:
	with open(logPath,"r") as f:
		for line in (l.rstrip() for l in f):
			match = format_pat.match(line)
			if match:
				access = match.groupdict()
				request = access['request']
				(action, URL, protocol) = request.split()
				if URLCounts.has_key(URL):
					URLCounts[URL] = URLCounts[URL] + 1
				else:
					URLCounts[URL] = 1
	
	results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)
	
	for result in results[:20]:
		print(result + ":" + str(URLCounts[result]))
	# Aqui temos erro de execução
except:
	with open(logPath, "r") as f:
		for line in (l.rstrip() for l in f):
			match= format_pat.match(line)
			if match:
				access = match.groupdict()
				request = access['request']
				fields = request.split()
				if (len(fields) != 3):
					print(fields)
	print("Observamos que temos requisições com campos vazios e um que parece 'lixo'")
	print('----------'*7)
time.sleep(5)

URLCounts = {}

with open(logPath, "r") as f:
	for line in (l.rstrip() for l in f):
		match= format_pat.match(line)
		if match:
			access = match.groupdict()
			request = access['request']
			fields = request.split()
			if (len(fields) == 3):
				URL = fields[1]
				if URL in URLCounts:
					URLCounts[URL] = URLCounts[URL] + 1
				else:
					URLCounts[URL] = 1

results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)

for result in results[:20]:
	print(result + ": " + str(URLCounts[result]))

print("\nAo definirmos as linhas de log = 3, conseguimos ver apenas as requisições válidas e a quantidade de acesso delas, ainda sim encontramos requisições estranhas, como 'xmlrpc.php' com 68494 acessos")
print('-------------'*7)
time.sleep(5)

UserAgents = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            agent = access['user_agent']
            if agent in UserAgents:
                UserAgents[agent] = UserAgents[agent] + 1
            else:
                UserAgents[agent] = 1

results = sorted(UserAgents, key=lambda i: int(UserAgents[i]), reverse=True)

for result in results:
    print(result + ": " + str(UserAgents[result]))
print('\nAqui filtramos apenas os users agentes e descobrimos vaorios bots acessando o site ')
print('-------------'*7,'\n')
time.sleep(5)

URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            agent = access['user_agent']
            if (not('bot' in agent or 'spider' in agent or 
                    'Bot' in agent or 'Spider' in agent or
                    'W3 Total Cache' in agent or agent =='-')):
                request = access['request']
                fields = request.split()
                if (len(fields) == 3):
                    (action, URL, protocol) = fields
                    if (action == 'GET'):
                        if URL in URLCounts:
                            URLCounts[URL] = URLCounts[URL] + 1
                        else:
                            URLCounts[URL] = 1

results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)

for result in results[:20]:
    print(result + ": " + str(URLCounts[result]))
print("Filtramos apenas as requisições 'get'. Aqui descobrimos vários acessos que podemos filtrar")
print('-------------'*7)
time.sleep(5)

URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match= format_pat.match(line)
        if match:
            access = match.groupdict()
            agent = access['user_agent']
            if (not('bot' in agent or 'spider' in agent or 
                    'Bot' in agent or 'Spider' in agent or
                    'W3 Total Cache' in agent or agent =='-')):
                request = access['request']
                fields = request.split()
                if (len(fields) == 3):
                    (action, URL, protocol) = fields
                    if (URL.endswith("/")):
                        if (action == 'GET'):
                            if URL in URLCounts:
                                URLCounts[URL] = URLCounts[URL] + 1
                            else:
                                URLCounts[URL] = 1

results = sorted(URLCounts, key=lambda i: int(URLCounts[i]), reverse=True)

for result in results[:20]:
    print(result + ": " + str(URLCounts[result]))
print('Aqui chegamos em um resultado mais satisfatórios dos acessos ao site, mas é importante salietnar que é preciso conehcer os dados que estão sendo analisados para saber como tratar')
print('-------------'*7)
