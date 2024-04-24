import speech_recognition as sr
import re
import pyttsx3

nome_usuario = ''
ASSISTENTE = 'Luluzinha'
print("Iniciando Assistente Virtual")
while(True):
    mic = sr.Recognizer()

    with sr.Microphone() as source:
        engine = pyttsx3.init()
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.luciana')
        mic.adjust_for_ambient_noise(source)

        try:
            audio = mic.listen(source, timeout=10)
        except sr.WaitTimeoutError:
            print("Tempo esgotado. Você não está falando.")
            break

        try:
            frase = mic.recognize_google(audio, language='pt-BR')

            # print(f"Você falou: {frase}")
            if (re.search(r'\b' + 'ajudar' + r'\b', format(frase), re.IGNORECASE)):
                print("Algo relacionado a ajudar")

            elif (re.search(r'\b' + 'meu nome é ' + r'\b', format(frase), re.IGNORECASE)):
                nome = re.search('meu nome é (.*)',format(frase), re.IGNORECASE)
                nome_usuario = nome.group(1)
                engine.say(f"Olá {nome_usuario} em que posso te ajudar?")
                engine.runAndWait()

            elif (re.search(r'\b' + 'seu\s*nome' + r'\b', format(frase), re.IGNORECASE)):
                engine.say(f"Meu nome é {ASSISTENTE}")
                engine.runAndWait()

            elif (re.search(r'\b' + 'tudo\s*bem\s*com\s*você' + r'\b', format(frase), re.IGNORECASE)):
                engine.say(f"Tudo ótimo, e com você?")
                engine.runAndWait()
        except sr.UnknownValueError:
            print("Algo deu errado!")