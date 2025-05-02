import os
import sys
import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import datetime
import google.generativeai as genai

# === CONFIGURAÇÃO DA CHAVE DO GEMINI ===
genai.configure(api_key="SUA_CHAVE_GEMINI_AQUI")  # Substitua pela sua chave

# Inicializa o modelo Gemini
modelo = genai.GenerativeModel('gemini-pro')

# Inicializa o mecanismo de voz
en = pyttsx3.init()
voices = en.getProperty('voices')
for voice in voices:
    if 'brazil' in voice.name.lower() or 'português' in voice.name.lower():
        en.setProperty('voice', voice.id)
        break
en.setProperty('rate', 140)
en.setProperty('volume', 1)

def falar(texto):
    print(f"Assistente: {texto}")
    en.say(texto)
    en.runAndWait()

def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language='pt-BR')
        print("Você disse:", comando)
        return comando.lower()
    except sr.UnknownValueError:
        falar("Desculpe, não entendi.")
        return ""
    except sr.RequestError:
        falar("Erro ao conectar com o serviço de voz.")
        return ""

def resposta_gemini(pergunta):
    try:
        resposta = modelo.generate_content(pergunta)
        return resposta.text.strip()
    except Exception as e:
        print("Erro ao acessar o Gemini:", e)
        return "Desculpe, não consegui acessar a inteligência artificial agora."

def executar_comando(comando):
    if "google" in comando:
        falar("Abrindo o Google.")
        webbrowser.open("https://www.google.com")

    elif "youtube" in comando:
        falar("Abrindo o YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "notícias" in comando:
        falar("Abrindo as notícias.")
        webbrowser.open("https://g1.globo.com")

    elif "calculadora" in comando:
        falar("Abrindo a calculadora.")
        subprocess.Popen('calc.exe')

    elif "bloco de notas" in comando:
        falar("Abrindo o Bloco de Notas.")
        subprocess.Popen('notepad.exe')

    elif "hora" in comando:
        agora = datetime.datetime.now().strftime("%H:%M")
        falar(f"Agora são {agora}")

    elif "data" in comando:
        hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        falar(f"Hoje é {hoje}")

    elif "desligar computador" in comando:
        falar("Você quer mesmo desligar o computador? Diga sim para confirmar.")
        if "sim" in ouvir_comando():
            falar("Desligando o computador.")
            os.system("shutdown /s /t 5")

    elif "encerrar" in comando or "sair" in comando:
        falar("Encerrando a assistente. Até logo!")
        sys.exit()

    else:
        # Qualquer outro comando vira pergunta para o Gemini
        resposta = resposta_gemini(comando)
        falar(resposta)

# Início da assistente
falar("Olá! Eu sou a Júlia, sua assistente com inteligência da Google. Pode me perguntar qualquer coisa!")

# Loop principal
while True:
    comando = ouvir_comando()
    if comando:
        executar_comando(comando)
