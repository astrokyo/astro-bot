import requests
import tweepy
import random
import schedule
import time

# Chaves da API do Twitter (substitua pelos seus valores!)
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Configuração da API do Twitter
def configurar_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

# Função para buscar horóscopo de um signo usando a API Aztro
def buscar_horoscopo(signo):
    url = "https://aztro.sameerkumar.website/"  # URL da API Aztro
    params = {"sign": signo.lower(), "day": "today"}  # Parâmetros para o signo e data
    try:
        response = requests.post(url, params=params)  # Aztro exige requisição POST
        if response.status_code == 200:
            data = response.json()
            return f"♈ {signo.capitalize()}: {data['description']} 🌟"
        else:
            print(f"Erro ao buscar horóscopo: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao conectar à API: {e}")
        return None

# Função para postar o horóscopo aleatório no Twitter
def postar_horoscopo():
    signos = ["Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
              "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]
    signo_aleatorio = random.choice(signos)  # Seleciona um signo aleatório
    mensagem = buscar_horoscopo(signo_aleatorio)  # Busca a mensagem para o signo selecionado
    if mensagem:
        api = configurar_twitter_api()  # Autentica na API do Twitter
        try:
            api.update_status(mensagem)  # Publica o tweet
            print(f"Horóscopo postado: {mensagem}")
        except Exception as e:
            print(f"Erro ao postar no Twitter: {e}")
    else:
        print("Não foi possível gerar o horóscopo.")

# Agendamento para postar diariamente às 9h
schedule.every().day.at("09:00").do(postar_horoscopo)

# Loop para manter o agendamento ativo
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
