import os
import sys
import subprocess
import webbrowser
import datetime

# Tentativa de importar pyttsx3, mas substituíremos para evitar erro no ambiente
try:
    import pyttsx3
    tts_available = True
except ImportError:
    tts_available = False

# Alternativa simples para TTS usando 'os.system' com 'say' no MacOS ou 'powershell' no Windows
def falar(texto):
    print(f"Assistente: {texto}")
    if tts_available:
        try:
            engine = pyttsx3.init()
            engine.say(texto)
            engine.runAndWait()
        except Exception as e:
            print("Erro no pyttsx3:", e)
            # fallback básico para Windows
            if sys.platform == 'win32':
                try:
                    subprocess.Popen(f'powershell -c "Add-Type –AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{texto}\');"', shell=True)
                except:
                    print("[Recurso de áudio indisponível]")
            elif sys.platform == 'darwin':
                try:
                    os.system(f'say "{texto}"')
                except:
                    print("[Recurso de áudio indisponível]")
            else:
                print("[Recurso de áudio indisponível]")
    else:
        # fallback simples para Windows e Mac
        if sys.platform == 'win32':
            try:
                subprocess.Popen(f'powershell -c "Add-Type –AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{texto}\');"', shell=True)
            except:
                print("[Recurso de áudio indisponível]")
        elif sys.platform == 'darwin':
            try:
                os.system(f'say "{texto}"')
            except:
                print("[Recurso de áudio indisponível]")
        else:
            print("[Recurso de áudio indisponível]")

def ouvir_comando():
    return input("Digite o comando: ").lower()

def resposta_padrao(pergunta):
    return f"Você perguntou: {pergunta}. Ainda não sei responder isso."

def executar_comando(comando):
    comando = comando.lower()
    if "google" in comando:
        falar("Abrindo o Google.")
        webbrowser.open("https://www.google.com")
    elif "youtube" in comando:
        falar("Abrindo o YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "notícias" in comando:
        falar("Abrindo as notícias.")
        webbrowser.open("https://g1.globo.com")
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
        confirmacao = ouvir_comando()
        if "sim" in confirmacao:
            falar("Desligando o computador.")
            os.system("shutdown /s /t 5")
    elif "encerrar" in comando or "sair" in comando:
        falar("Encerrando a assistente. Até logo!")
        sys.exit()
    else:
        resposta = resposta_padrao(comando)
        falar(resposta)

def iniciar_assistente():
    falar("Olá! Eu sou a Júlia, sua assistente. Pode me perguntar qualquer coisa!")
    while True:
        comando = ouvir_comando()
        if comando:
            executar_comando(comando)

if __name__ == "__main__":
    iniciar_assistente()
