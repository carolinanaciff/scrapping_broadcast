import requests
import pandas as pd
from bs4 import BeautifulSoup
import openpyxl
import time
import os


# iniciando extração broadcast
try:
    output_excel = pd.read_excel('output.xlsx')
except:
    print('Não conseguiu ler o arquivo')

print('iniciando a request em broadcast')
url = 'http://broadcast.com.br'
result = requests.get(url)
time.sleep(3)
print(f'request finalizada. StatusCode: {result.status_code}')

if result.status_code != 200:
    raise Exception('Request não retornou com sucesso')

soup = BeautifulSoup(result.text, 'html.parser')
tabela = soup.find_all('div', class_ = 'materia')

if tabela == []:
    raise Exception('find noticias retornou vazio')

data = [[], [], [], []]
columns = ['titulo', 'link', 'data_hora', 'materia']

for i in tabela:
    titulo = i.a.get_text()
    link = i.a.get('href')
    url_noticia = url+link

    print(f'Acessando notícia...\nTitulo de notícia: {titulo}\nLink: {url_noticia}')

    result_noticia = requests.get(url_noticia)
    time.sleep(3)
    print(f'request finalizada. StatusCode: {result_noticia.status_code}')

    if result_noticia.status_code != 200:
        continue

    soup_noticia = BeautifulSoup(result_noticia.text, 'html.parser')
    time.sleep(1)
    tabela_noticia = soup_noticia.find('div', class_= 'integra-materia')
    time.sleep(1)

    if tabela_noticia == []:
        raise Exception('find noticia retornou vazio')

    data_hora = soup_noticia.find('div', class_='data_hora')

    if data_hora == []:
       raise Exception('find de data retornou vazio') 
    try:
        data.append([titulo, url_noticia, data_hora.text, tabela_noticia.text])
    except Exception as ex:
        print(ex)
        continue

print('filtrando lista para remover linhas vazias')
lista = list(filter(None, data))
print('convertendo lista em dataframe')
df = pd.DataFrame(lista, columns=columns)
print(len(df))
print(df)
print(' ')
print(len(output_excel))
print(output_excel)

'''
for index, row in df.iterrows():
    resultado = output_excel.loc[output_excel['link'] == row['link']]
    if len(resultado) > 0:
        print('link: '+ row['link'])
        df = df.drop(index=index)
'''
df.merge(output_excel)
print('feito merge do excel anterior com o novo dataframe')
print(len(df))


try:
    print('validando se excel ja existe')
    existe = os.path.isfile('output.xlsx')
    if existe:
        print('arquivo existe, deletando')
        os.remove('output.xlsx')
        print('arquivo deletado')
    
    time.sleep(1)
    print('criando novo arquivo')
    df.to_excel('output.xlsx')
    print('arquivo criado')
    
except Exception as ex:
    print(ex)