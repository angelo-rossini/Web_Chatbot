import re
from processing import processing
from functions import google, moedas
from flask_cors import CORS
from flask import Flask, request, render_template

# Função que busca as respostas que melhor se enquadram na pergunta com base na quantidade de palavras chave
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # conta quantas das palavras estão presentes em cada menssagem pré-definida
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # calcula a porcentagem de palavras reconhecidas na menssagem do usuario
    percentage = float(message_certainty) / float(len(recognised_words))

    # checa qual são as palavras requiridas na string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Deve também ter palavras requiridas, ou uma única resposta
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    # simplifica a criação de resposta / adiciona isso ao dicionario
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # respostas ------ (resposta, lista de palavras que podem ser válidas para essa resposta, respostas simples ou se precisa de um termo chave)
    
    response('pesquisa', ['daisy','quem', 'foi'], required_words = ['quem', 'foi'])
    
    response('pesquisa', ['daisy','quem', 'é'], required_words = ['quem', 'é'])
    
    response('pesquisa', ['daisy','o', 'que','é'], required_words = ['o', 'que','é'])
    
    response('pesquisa', ['daisy','você', 'sabe', 'o', 'que', 'é'], required_words = ['o', 'que', 'é'])
    
    response('pesquisa', ['daisy','me', 'diga','o', 'que','é'], required_words = ['o', 'que', 'é'])
    
    response('gatos', ['daisy','me','conta','uma','curiosidade','sobre','gatos'], required_words = ['gatos'])

    response('gatos', ['o','que','você','sabe','sobre','gatos'], required_words = ['gatos'])
    
    response('cachorros', ['daisy','me','conta','uma','curiosidade','sobre','cachorros'], required_words = ['cachorros'])
    
    response('cachorros', ['o','que','você','sabe','sobre','cachorros'], required_words = ['cachorros'])
    
    response('tendencias', ['quais','são','as','tendencias','do','momento'], required_words = ['tendencias'])
    
    response('tendencias', ['quais','foram','os','tópicos','mais','procurados','hoje'])
    
    response('tendencias', ['daisy','no','que','as','pessoas','estão','interessadas','no','momentos'])
    
    response('anime', ['daisy','me','sugere','um','anime','para','assistir'], required_words = ['anime'])
    
    response('anime', ['daisy','me','diga','o','nome','de','um','anime'], required_words = ['anime'])
    
    response('dado', ['roda', 'um', 'para','mim','você', 'pode', 'agora'], required_words = ['roda'])
    
    response('tradução', ['traduz','para','mim'], required_words = ['traduz'])
    
    response('tradução', ['qual','a','tradução','de'], required_words = ['tradução'])
    
    response('tradução', ['traduza', 'para','mim'], required_words = ['traduza'])
    
    response('manga/webtoon', ['daisy','abre','para','mim'])
    
    response('manga/webtoon', ['ler','online'])
    
    response('manga/webtoon', ['daisy','me','abre','um','site','para','ler'])
    
    response('manga/webtoon', ['daisy','abre','para','mim','para','ler','online'])
    
    response('manga/webtoon', ['daisy','abre','para','um','site','para','ler','online'])

    response('ola', ['daisy','como', 'você', 'está', 'vou', 'bem', 'e'])

    response('agradecimento', ['obrigado', 'obrigada', 'valeu', 'pela', 'ajuda'])
    
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    response = processing(best_match, message)

    return response

# Função para conseguir as respostas
def get_response(user_input):
    
    split_menssage = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    for i in range(len(split_menssage)):
        if (split_menssage[i] == 'cotação' or split_menssage[i] == 'cotacao' and split_menssage[i] == 'como'):
            strjson = moedas(split_menssage)
            return(strjson)
        elif (split_menssage[i] == 'pesquisa' or split_menssage[i] == 'qual' or split_menssage[i] == 'como'):
            strjson = google(split_menssage)
            return(strjson)
    else:
        response = check_all_messages(split_menssage)
        return response

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET'])

def home():
    return render_template('index.html')

@app.route("/get", methods = ["POST"])

def chat():

    try:
        data = request.get_json()
        return get_response(data['req'])

    except:
        strjson = "não consegui entender o que deseja, poderia repetir"
        return(strjson)
    
if __name__ == "__main__":
    app.run(debug = True)