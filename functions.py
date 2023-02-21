import os
from random import randint
import socket
import wikipedia
import requests
from pytrends.request import TrendReq
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
from googlesearch import search
from deep_translator import GoogleTranslator

# Função para conversão de lista em string para as funções de pesquisa

def listToString(s):

    # initialize an empty string
    str1 = " "

    # return string 
    return (str1.join(s))

# Resposta para quando perguntarem como ela está, uma forma de tornar a interação mais humana

def send_hi():
    strjson = {"response":'vou bem', "expression": 'feliz'}
    return strjson

def agradeciment():
    strjson = {"response":'fico feliz em te ajudar', "expression": 'agredecida'}
    return strjson

# Função para busca de mangá/webtoon

def Manga(message):

#Esta pode não ser a melhor opção, mas por falta de ideias, foi optado criar um bag of words com as potencias palavras que mais viram na frase e possuir apenas as mais chave para a necessidade da função.

    split_menssage2 = message.copy()

    bag_of_words = ['daisy','abre','ler', 'online','mim','me','um','site','para','de','manga','o']

    for i in range(len(message)):
        for n in range(len(bag_of_words)):
            if(message[i] == bag_of_words[n]):
                split_menssage2.remove(message[i])

    query = 'ler ' + 'online ' + listToString(split_menssage2)
    for j in search(query, tld = "co.in", num = 1, stop = 1):
        strjson = {"response": j, "expression": 'otaku'}
        return strjson

# Função para busca na wikipedia

def check_on_wikipedia(message):

    split_menssage2 = message.copy()

    bag_of_words = ['daisy','quem','foi', 'é','o','você','sabe','que','me','diga']

    for i in range(len(message)):
        for n in range(len(bag_of_words)):
            if(message[i] == bag_of_words[n]):
                split_menssage2.remove(message[i])

    query = listToString(split_menssage2)

    try:
        wikipedia.set_lang("pt")
        resumo = wikipedia.summary(query , sentences=3)
        strjson = {"response": resumo, "expression": 'pesquisa'}
        return strjson
    except:
        strjson = {"response": "desculpa, mas não foi possivel encontrar sobre {}".format(query), "expression": 'triste'}
        return strjson

# Função que trás uma curiosidade sobre gatos 

def cat_fact():
    try:
        cats = requests.get("https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=2").json()
        resposta = GoogleTranslator(source='auto', target='pt').translate(str(cats[1]['text']))
        strjson = {"response": resposta, "expression": 'neutra'}
        return strjson
    except:
        strjson = {"response": "a api está com excesso de requisições no momento, peço desculpas por isso, tente mais tarde", "expression": 'triste'}
        return strjson

# Função que trás uma curiosidade sobre cachorros

def dog_fact():
    try:
        requisicao_cachorro = requests.get('https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1')
        curiosidade = requisicao_cachorro.json()
        resposta = GoogleTranslator(source='auto', target='pt').translate(str(curiosidade[1]['text']))
        strjson = {"response": resposta, "expression": 'neutra_2'}
        return strjson
    except:
        strjson = {"response": "a api está com excesso de requisições no momento, peço desculpas por isso, tente mais tarde", "expression": 'triste'}
        return strjson

# Função que mostra as 20 palavras chave mais buscadas no momento

def tendencia():

    # Busca pelas 20 palavras chave mais buscadas no momento por meio da biblioteca

    pytrends = TrendReq(hl='en-US', tz=360)
    data = pytrends.trending_searches(pn='brazil')

    # inserção de cada uma delas numa lista

    list = []
    
    for i in range(len(data.values)):
        list.append(data.values[i][0])

    # Criação da resposta como string usando a mesma lógica da função listToString

    response = "As pesquisas com maior número de buscas foram: " + ", ".join(list) + "."

    strjson = {"response": response, "expression": 'tendencia'}
    return strjson

# Função que retorna um anime random

def anime():
    try:
        computer_choice = randint(1, 9000)
        computer_url = 'https://api.jikan.moe/v3/anime/{}/'.format(computer_choice)
        computer_response = requests.get(computer_url)
        a = computer_response.json()['title']
        strjson = {"response": "minha recomendação de anime é {}".format(a), "expression": 'otaku'}
        return strjson
    except:
        strjson = {"response": "a api está com excesso de requisições no momento, peço desculpas por isso, tente mais tarde", "expression": 'triste'}
        return strjson

# Função que mostra a cotação atual das moedas convertida para o BRL

def moedas(codigo):

    codigo = codigo[len(codigo) - 1]

    try:
        if (codigo == 'BTC'):
            b = BtcConverter()
            b = b.get_latest_price('BRL')
            strjson = {"response": "A cotação atual é de R$ {:.3}".format(b), "expression": 'neutra'}
            return strjson
        else:
            c = CurrencyRates()
            strjson = {"response": "A cotação atual é de R$ {:.3}".format(c.convert(codigo, 'BRL', 1)), "expression": 'neutra2'}
            return strjson
    except(KeyError):
            strjson = {"response": "código inserido não é invalido, tente de novo", "expression": 'triste'}
            return strjson
    except:
            strjson = {"response": "a api está com excesso de requisições no momento, peço desculpas por isso, tente mais tarde", "expression": 'triste'}
            return strjson

# Função que retorna um valor random em uma range especifica, útil para rpg

def dado(split_menssage):

    try:
        for i in range(len(split_menssage)):

            if split_menssage[i][:1] == 'd' and split_menssage[i][:1] != 'daisy':
                n = int(split_menssage[i].replace('d', ''))
                break
            
        strjson = {"response": "e o número que sua sorte trouxe foi {}".format(randint(1, n)), "expression": 'maga'}
        return strjson
    except:
        strjson = {"response": "poderia me dizer de novo qual dado deseja que eu rode para você", "expression": 'triste'}
        return strjson
        
# Segunda função de busca de informação, mais abrangente usando a API do google

def google(split_menssage):

    split_menssage2 = split_menssage.copy()

    bag_of_words = ['daisy','pesquisa','para', 'mim']

    for i in range(len(split_menssage)):
        for n in range(len(bag_of_words)):
            if(split_menssage[i] == bag_of_words[n]):
                split_menssage2.remove(split_menssage[i])

    for j in search(listToString(split_menssage2), tld = "co.in", num = 1, stop = 1):
        strjson = {"response": j, "expression": 'pesquisa_2'}
        return strjson
    
# Função de tradução de texto, no momento só traduz de outra língua para o português

def traducao(split_menssage):

    split_menssage2 = split_menssage.copy()

    bag_of_words = ['daisy','traduz','para','mim','qual','a','tradução','de','traduza']

    for i in range(len(split_menssage)):
        for n in range(len(bag_of_words)):
            if(split_menssage[i] == bag_of_words[n]):
                split_menssage2.remove(split_menssage[i])

    resposta = GoogleTranslator(source='auto', target='pt').translate(listToString(split_menssage2))
    strjson = {"response": resposta, "expression": 'pesquisa'}
    return strjson